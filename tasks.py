"""Kunlik vazifalar, yo'l xarita va profil handlerlari."""

from datetime import date

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from db import get_user, get_done_days, get_last_done_date, mark_done, get_streak
from roadmap import get_task, TOTAL_DAYS

router = Router()


def bajarildi_keyboard(day: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Bajarildi", callback_data=f"done:{day}")]
    ])


@router.message(F.text == "📚 Vazifalar")
async def vazifalar(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Avval ro'yxatdan o'ting: /start")
        return

    done_days = await get_done_days(message.from_user.id)
    last_date = await get_last_done_date(message.from_user.id)

    if len(done_days) >= TOTAL_DAYS:
        await message.answer(
            "🎉 Birinchi haftalik yo'l xaritani to'liq tugatding!\n\n"
            "Yangi vazifalar tez orada qo'shiladi. 🔜"
        )
        return

    if last_date == str(date.today()):
        await message.answer(
            "✅ Bugungi vazifa allaqachon bajarilgan!\n\n"
            "⏰ Ertaga yangi vazifa keladi.\n🔥 Streakni saqlab qol!"
        )
        return

    day = len(done_days) + 1
    title, vaqt, maqsad = get_task(day, user[5], user[6])
    await message.answer(
        f"📚 Bugungi vazifa ({day}/{TOTAL_DAYS}-kun): {title}\n"
        f"⏱ Vaqt: {vaqt}\n"
        f"🎯 Maqsad: {maqsad}\n"
        f"✅ Bajarildi tugmasini bos",
        reply_markup=bajarildi_keyboard(day)
    )


@router.callback_query(F.data.startswith("done:"))
async def task_done(call: CallbackQuery):
    day = int(call.data.split(":")[1])
    done_days = await get_done_days(call.from_user.id)

    if day in done_days:
        await call.answer("Bu vazifa allaqachon bajarilgan!", show_alert=True)
        return

    await mark_done(call.from_user.id, day)
    streak = await get_streak(call.from_user.id)
    await call.message.edit_text(
        f"🎉 Barakalla! {day}-kun vazifasi bajarildi!\n\n"
        f"🔥 Streak: {streak} kun\n"
        f"⏰ Ertaga yangi vazifa kutadi!"
    )
    await call.answer("🎉 +1 kun!")


@router.message(F.text == "🗺️ Yo'l xarita")
async def yol_xarita(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Avval ro'yxatdan o'ting: /start")
        return

    done_days = await get_done_days(message.from_user.id)
    lines = []
    for day in range(1, TOTAL_DAYS + 1):
        title, _, _ = get_task(day, user[5], user[6])
        belgi = "✅" if day in done_days else "⬜"
        lines.append(f"{belgi} {day}-kun: {title}")

    await message.answer(
        "🗺️ Sening yo'l xaritang (1-hafta):\n\n"
        + "\n\n".join(lines)
        + f"\n\n📊 Bajarildi: {len(done_days)}/{TOTAL_DAYS}"
    )


@router.message(F.text == "👤 Profil")
async def profil(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Avval ro'yxatdan o'ting: /start")
        return

    done_days = await get_done_days(message.from_user.id)
    await message.answer(
        f"👤 Profil\n\n"
        f"Ism: {user[2]}\n"
        f"Sinf: {user[3]}\n"
        f"Yo'nalish: {user[5]}\n"
        f"Kasb: {user[6]}\n\n"
        f"🔥 Streak: {user[7]} kun\n"
        f"⭐ Daraja: {user[8]}\n"
        f"📚 Bajarilgan vazifalar: {len(done_days)}/{TOTAL_DAYS}"
    )


@router.message(F.text.in_(["🏆 Reyting", "💎 Premium"]))
async def tez_orada(message: Message):
    await message.answer("🔜 Bu bo'lim tez orada ochiladi!")
