
from aiogram import Router, Bot, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
import re

from db import save_user
from menus import yonalish_keyboard, kasb_keyboard

router = Router()

CHANNEL_ID = "@AI_Maqsad"
INSTAGRAM = "instagram.com/maqsadai"

class Onboarding(StatesGroup):
    ism = State()
    sinf = State()
    ota_raqam = State()
    yonalish = State()
    kasb = State()

async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status not in ["left", "kicked"]
    except:
        return False

def obuna_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanalga o'tish", url=f"https://t.me/AI_Maqsad")],
        [InlineKeyboardButton(text="✅ Obuna bo'ldim", callback_data="check_sub")]
    ])

@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot, state: FSMContext):
    is_subscribed = await check_subscription(bot, message.from_user.id)
    if not is_subscribed:
        await message.answer(
            "👋 Salom! MaqsadAI botiga xush kelibsiz!\n\n"
            "Botdan foydalanish uchun avval kanalimizga obuna bo'ling 👇",
            reply_markup=obuna_keyboard()
        )
        return
    await message.answer(
        "👋 Salom! MaqsadAI ga xush kelibsiz!\n\n"
        f"📲 Bizni kuzating:\n• Telegram: {CHANNEL_ID}\n• Instagram: {INSTAGRAM}\n\n"
        "Keling tanishamiz. Ismingiz nima?",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Onboarding.ism)

@router.callback_query(F.data == "check_sub")
async def check_sub_callback(call: CallbackQuery, bot: Bot, state: FSMContext):
    is_subscribed = await check_subscription(bot, call.from_user.id)
    if not is_subscribed:
        await call.answer("❌ Hali obuna bo'lmadingiz!", show_alert=True)
        return
    await call.message.delete()
    await call.message.answer(
        "✅ Rahmat! Endi botdan foydalanishingiz mumkin.\n\n"
        f"📲 Bizni kuzating:\n• Telegram: {CHANNEL_ID}\n• Instagram: {INSTAGRAM}\n\n"
        "Ismingiz nima?",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Onboarding.ism)

@router.message(Onboarding.ism)
async def get_ism(message: Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer(f"Zo'r ism! 👏\n\nNechichi sinfda o'qiysiz? (masalan: 8, 9, 10, 11)")
    await state.set_state(Onboarding.sinf)

@router.message(Onboarding.sinf)
async def get_sinf(message: Message, state: FSMContext):
    await state.update_data(sinf=message.text)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni ulashish", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer(
        "📱 Ota-onangiz telefon raqami:\n\n"
        "Nega kerak?\n✅ Ota-onangiz progressingizni ko'radi\n"
        "🏆 Sertifikat oladi\n🔔 Yutuqlaringizdan xabar topadi\n\n"
        "Quyidagi tugmani bosing yoki qo'lda kiriting (+998XXXXXXXXX):",
        reply_markup=keyboard
    )
    await state.set_state(Onboarding.ota_raqam)

@router.message(Onboarding.ota_raqam, F.contact)
async def get_raqam_contact(message: Message, state: FSMContext):
    raqam = message.contact.phone_number
    if not raqam.startswith("+"): raqam = "+" + raqam
    await state.update_data(ota_raqam=raqam)
    await message.answer("✅ Raqam saqlandi!\n\nEndi yo'nalishingizni tanlang 👇", reply_markup=yonalish_keyboard())
    await state.set_state(Onboarding.yonalish)

@router.message(Onboarding.ota_raqam, F.text)
async def get_raqam_text(message: Message, state: FSMContext):
    raqam = message.text.strip()
    if not re.match(r'^\+998\d{9}$', raqam):
        await message.answer("❌ Raqam noto'g'ri!\nTo'g'ri format: +998901234567\nQaytadan kiriting:")
        return
    await state.update_data(ota_raqam=raqam)
    await message.answer("✅ Raqam saqlandi!\n\nEndi yo'nalishingizni tanlang 👇", reply_markup=yonalish_keyboard())
    await state.set_state(Onboarding.yonalish)

YONALISHLAR = [
    "💻 Texnologiya", "💼 Biznes", "💰 Moliya", "🎨 Dizayn",
    "📱 Media", "🎭 San'at", "🏗️ Arxitektura", "⚙️ Muhandislik",
    "🧬 Tibbiyot", "🧠 Psixologiya", "🎓 Ta'lim", "⚖️ Huquq",
    "📊 Marketing", "🌍 Xalqaro Aloqalar", "✈️ Turizm", "🏋️ Sport",
    "🚚 Logistika", "🔭 Ilm-fan", "🌱 Qishloq Xo'jaligi", "🛡️ Xavfsizlik"
]

@router.message(Onboarding.yonalish, F.text.in_(YONALISHLAR))
async def get_yonalish(message: Message, state: FSMContext):
    await state.update_data(yonalish=message.text)
    await message.answer(f"Ajoyib tanlov! {message.text}\n\nEndi kasbingizni tanlang 👇", reply_markup=kasb_keyboard(message.text))
    await state.set_state(Onboarding.kasb)

@router.message(Onboarding.kasb)
async def get_kasb(message: Message, state: FSMContext):
    data = await state.get_data()
    await save_user(
        telegram_id=message.from_user.id,
        ism=data["ism"], sinf=data["sinf"],
        ota_raqam=data["ota_raqam"], yonalish=data["yonalish"], kasb=message.text
    )
    await message.answer(
        f"🎉 Tabriklaymiz, {data['ism']}!\n\n"
        f"Sizning yo'l xaritangiz tayyor:\n\n"
        f"👤 Ism: {data['ism']}\n📚 Sinf: {data['sinf']}\n"
        f"🎯 Yo'nalish: {data['yonalish']}\n💼 Kasb: {message.text}\n\n"
        f"Endi har kuni vazifalar keladi!\n🔥 Streak boshlandi!",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
