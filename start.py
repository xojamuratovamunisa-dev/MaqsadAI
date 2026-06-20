import re
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# FSM holatlari
class Onboarding(StatesGroup):
    yonalish = State()
    ota_raqam = State()
    kasb_tanlash = State()
    kasb_tasdiqlash = State()

router = Router()

# --- Start komandasi handleri ---
@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    await state.set_state(Onboarding.yonalish)
    await message.answer("Xush kelibsiz! Yo'nalishni tanlang:")

# --- Telefon raqamni qabul qilish handleri ---
@router.message(Onboarding.ota_raqam, F.text)
async def get_raqam_text(message: Message, state: FSMContext):
    raqam = message.text.strip()
    if not re.match(r'^\+998\d{9}$', raqam):
        await message.answer("❌ Raqam noto'g'ri!")
        return
    await state.update_data(ota_raqam=raqam)
    await _keyin_raqam(message, state)

# --- Kasb orqaga handleri ---
@router.callback_query(F.data == "kasb_orqaga")
async def kasb_orqaga_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.delete()
    await call.message.answer(
        f"Boshqa kasb tanlang 👇",
        reply_markup=kasb_keyboard(data["yonalish"])
    )
    await state.set_state(Onboarding.kasb_tanlash)

# --- Yo'nalish orqaga handleri ---
@router.callback_query(F.data == "yonalish_orqaga", Onboarding.kasb_tasdiqlash)
async def yonalish_orqaga_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Orqaga qaytildi")  # Bu yerga o'z matningizni yozishingiz mumkin
