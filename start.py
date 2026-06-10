from aiogram import Router, Bot, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
import re

from db import save_user
from menus import yonalish_keyboard, kasb_keyboard

router = Router()

CHANNEL_ID = "@AI_Maqsad"

# --- Holatlar ---
class Onboarding(StatesGroup):
    ism = State()
    sinf = State()
    ota_raqam = State()
    yonalish = State()
    kasb = State()

# --- Obunani tekshirish ---
async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status not in ["left", "kicked"]
    except:
        return False

# --- /start ---
@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot, state: FSMContext):
    is_subscribed = await check_subscription(bot, message.from_user.id)

    if not is_subscribed:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✅ Obuna bo'ldim")]
            ],
            resize_keyboard=True
        )
        await message.answer(
            "👋 Salom! MaqsadAI botiga xush kelibsiz!\n\n"
            "Botdan foydalanish uchun avval kanalimizga obuna bo'ling:\n"
            f"👉 {CHANNEL_ID}\n\n"
            "Obuna bo'lgach, quyidagi tugmani bosing 👇",
            reply_markup=keyboard
        )
        return

    await message.answer(
    "📲 Bizning sahifalarimiz:\n"
"• Telegram: @AI_Maqsad\n"
"• Instagram: instagram.com/maqsadai\n\n"
"👋Keling tanishamiz. Ismingiz nima?",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Onboarding.ism)


# --- Obunani tekshirish tugmasi ---
@router.message(F.text == "✅ Obuna bo'ldim")
async def check_sub_button(message: Message, bot: Bot, state: FSMContext):
    is_subscribed = await check_subscription(bot, message.from_user.id)

    if not is_subscribed:
        await message.answer(
            "❌ Siz hali obuna bo'lmadingiz!\n\n"
            f"Iltimos, avval obuna bo'ling: {CHANNEL_ID}\n"
            "Keyin tugmani bosing."
        )
        return

    await message.answer(
        "✅ Rahmat! Endi botdan foydalanishingiz mumkin.\n\n"
        "Ismingiz nima?",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Onboarding.ism)


# --- Ism ---
@router.message(Onboarding.ism)
async def get_ism(message: Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer(
        f"Zo'r ism! 👏\n\n"
        f"Nechichi sinfda o'qiysiz? (masalan: 8, 9, 10, 11)"
    )
    await state.set_state(Onboarding.sinf)


# --- Sinf ---
@router.message(Onboarding.sinf)
async def get_sinf(message: Message, state: FSMContext):
    await state.update_data(sinf=message.text)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni ulashish", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer(
        "📱 Ota-onangiz telefon raqami:\n\n"
        "Nega kerak?\n"
        "✅ Ota-onangiz progressingizni ko'radi\n"
        "🏆 Sertifikat oladi\n"
        "🔔 Yutuqlaringizdan xabar topadi\n\n"
        "Quyidagi tugmani bosing yoki qo'lda kiriting (+998XXXXXXXXX):",
        reply_markup=keyboard
    )
    await state.set_state(Onboarding.ota_raqam)


# --- Ota-ona raqami (kontakt orqali) ---
@router.message(Onboarding.ota_raqam, F.contact)
async def get_raqam_contact(message: Message, state: FSMContext):
    raqam = message.contact.phone_number
    if not raqam.startswith("+"):
        raqam = "+" + raqam
    await state.update_data(ota_raqam=raqam)

    await message.answer(
        "✅ Raqam saqlandi!\n\n"
        "Endi yo'nalishingizni tanlang 👇",
        reply_markup=yonalish_keyboard()
    )
    await state.set_state(Onboarding.yonalish)


# --- Ota-ona raqami (qo'lda) ---
@router.message(Onboarding.ota_raqam, F.text)
async def get_raqam_text(message: Message, state: FSMContext):
    raqam = message.text.strip()
    pattern = r'^\+998\d{9}$'
    if not re.match(pattern, raqam):
        await message.answer(
            "❌ Raqam noto'g'ri formatda!\n"
            "To'g'ri format: +998901234567\n"
            "Qaytadan kiriting:"
        )
        return

    await state.update_data(ota_raqam=raqam)
    await message.answer(
        "✅ Raqam saqlandi!\n\n"
        "Endi yo'nalishingizni tanlang 👇",
        reply_markup=yonalish_keyboard()
    )
    await state.set_state(Onboarding.yonalish)


# --- Yo'nalish ---
YONALISHLAR = ["📐 Texnika", "🧬 Tibbiyot", "⚖️ Huquq", "💼 Biznes", "🎨 Ijodkorlik", "💻 IT"]

@router.message(Onboarding.yonalish, F.text.in_(YONALISHLAR))
async def get_yonalish(message: Message, state: FSMContext):
    await state.update_data(yonalish=message.text)

    await message.answer(
        f"Ajoyib tanlov! {message.text}\n\n"
        "Endi kasbingizni tanlang 👇",
        reply_markup=kasb_keyboard(message.text)
    )
    await state.set_state(Onboarding.kasb)


# --- Kasb ---
@router.message(Onboarding.kasb)
async def get_kasb(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(kasb=message.text)

    await save_user(
        telegram_id=message.from_user.id,
        ism=data["ism"],
        sinf=data["sinf"],
        ota_raqam=data["ota_raqam"],
        yonalish=data["yonalish"],
        kasb=message.text
    )

    await message.answer(
        f"🎉 Tabriklaymiz, {data['ism']}!\n\n"
        f"Sizning yo'l xaritangiz tayyor:\n\n"
        f"👤 Ism: {data['ism']}\n"
        f"📚 Sinf: {data['sinf']}\n"
        f"🎯 Yo'nalish: {data['yonalish']}\n"
        f"💼 Kasb: {message.text}\n\n"
        f"Endi har kuni vazifalar keladi!\n"
        f"🔥 Streak boshlandi — ketma-ket bajaring!",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()
