import asyncio
import gspread
from google.oauth2.service_account import Credentials
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import os

from db import get_user, get_done_days, mark_done, get_all_users, get_streak

router = Router()

# ============================================================
# GOOGLE SHEETS ULANISH
# ============================================================
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")  # .env da saqlang

def get_sheets_client():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    return gspread.authorize(creds)

def get_vazifa(kasb: str, oy: int, kun: int) -> dict | None:
    """Google Sheetsdan vazifa olish"""
    try:
        gc = get_sheets_client()
        sh = gc.open_by_key(SHEET_ID)
        ws = sh.worksheet(f"{oy}-oy")
        rows = ws.get_all_records()
        for row in rows:
            # Kasb nomi emojilar bilan bo'lishi mumkin, shuning uchun in ishlatamiz
            if kasb.lower() in str(row.get("Kasb", "")).lower() and int(row.get("Kun", 0)) == kun:
                return {
                    "yonalish": row.get("Yo'nalish", ""),
                    "kasb": row.get("Kasb", ""),
                    "kun": int(row.get("Kun", kun)),
                    "vazifa": row.get("Vazifa", ""),
                    "vaqt": row.get("Vaqt (daqiqa)", 45),
                    "xp": row.get("XP", 20),
                    "daraja": row.get("Daraja", "bepul"),
                }
        return None
    except Exception as e:
        print(f"Sheets xato: {e}")
        return None

def get_keyingi_7_kun(kasb: str, joriy_oy: int, joriy_kun: int) -> list:
    """Keyingi 7 kunlik vazifalar preview"""
    vazifalar = []
    try:
        gc = get_sheets_client()
        sh = gc.open_by_key(SHEET_ID)

        kun = joriy_kun + 1
        oy = joriy_oy

        for _ in range(7):
            if kun > 30:
                kun = 1
                oy += 1
            if oy > 12:
                break
            try:
                ws = sh.worksheet(f"{oy}-oy")
                rows = ws.get_all_records()
                for row in rows:
                    if kasb.lower() in str(row.get("Kasb", "")).lower() and int(row.get("Kun", 0)) == kun:
                        vazifalar.append({
                            "oy": oy,
                            "kun": kun,
                            "vazifa": row.get("Vazifa", ""),
                            "xp": row.get("XP", 20),
                            "daraja": row.get("Daraja", "bepul"),
                        })
                        break
            except:
                pass
            kun += 1
    except Exception as e:
        print(f"Preview xato: {e}")
    return vazifalar

# ============================================================
# PROGRESS HISOBLASH
# ============================================================
def hisobla_progress(bajarilgan_kunlar: list) -> dict:
    jami_kun = 360
    bajarilgan = len(bajarilgan_kunlar)
    joriy_kun = bajarilgan + 1
    joriy_oy = ((joriy_kun - 1) // 30) + 1
    oy_ichi_kun = ((joriy_kun - 1) % 30) + 1
    foiz = round((bajarilgan / jami_kun) * 100, 1)

    # Progress bar (20 belgi)
    tolgan = int(foiz / 5)
    bosh = 20 - tolgan
    progress_bar = "█" * tolgan + "░" * bosh

    # Liga
    xp_jami = sum(range(1, bajarilgan + 1)) * 2  # taxminiy
    if bajarilgan < 30:
        liga = "🥉 Bronza"
    elif bajarilgan < 90:
        liga = "🥈 Kumush"
    elif bajarilgan < 180:
        liga = "🥇 Oltin"
    else:
        liga = "💎 Olmos"

    # Bosqich
    if joriy_oy <= 2:
        bosqich = "🟢 Asoslar (BEPUL)"
        bosqich_tavsif = "Kasbingizning asoslarini o'rganayapsiz"
    elif joriy_oy <= 6:
        bosqich = "🔵 Amaliyot (PREMIUM)"
        bosqich_tavsif = "Haqiqiy amaliyot va loyihalar boshlandi"
    else:
        bosqich = "🟣 Professional (PREMIUM)"
        bosqich_tavsif = "Professional daraja — siz ekspert bo'lyapsiz!"

    return {
        "bajarilgan": bajarilgan,
        "jami_kun": jami_kun,
        "joriy_kun": joriy_kun,
        "joriy_oy": joriy_oy,
        "oy_ichi_kun": oy_ichi_kun,
        "foiz": foiz,
        "progress_bar": progress_bar,
        "liga": liga,
        "bosqich": bosqich,
        "bosqich_tavsif": bosqich_tavsif,
    }

# ============================================================
# KUNLIK VAZIFA KEYBOARD
# ============================================================
def vazifa_kb(kun: int, bajarilganmi: bool = False) -> InlineKeyboardMarkup:
    if bajarilganmi:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Bajarildi!", callback_data="already_done")],
            [InlineKeyboardButton(text="🗺 Yo'l xaritam", callback_data="yol_xarita")],
        ])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Bajardim!", callback_data=f"bajarildi_{kun}")],
        [InlineKeyboardButton(text="🗺 Yo'l xaritam", callback_data="yol_xarita")],
        [InlineKeyboardButton(text="⏰ Eslatma qo'y", callback_data="eslatma")],
    ])

# ============================================================
# KUNLIK VAZIFA YUBORISH
# ============================================================
async def yuborilsin_bugungi_vazifa(bot: Bot, telegram_id: int):
    """Bir userni bugungi vazifasini yuborish"""
    user = await get_user(telegram_id)
    if not user:
        return

    # user tuple: (id, telegram_id, ism, sinf, ota_raqam, yonalish, kasb, vazifa_vaqti, streak, level, premium, created_at)
    ism = user[2]
    kasb = user[6]
    premium = user[10]

    bajarilgan_kunlar = await get_done_days(telegram_id)
    prog = hisobla_progress(bajarilgan_kunlar)
    joriy_kun = prog["joriy_kun"]
    joriy_oy = prog["joriy_oy"]

    # Premium tekshiruv
    if joriy_oy > 2 and not premium:
        await bot.send_message(
            telegram_id,
            f"🔒 <b>{ism}, {joriy_oy}-oy vazifalari Premium uchun!</b>\n\n"
            f"Siz allaqachon <b>{bajarilgan_kunlar.__len__()} kun</b> bajardingiz — zo'r! 💪\n\n"
            f"Davom etish uchun Premium obuna oling:\n"
            f"💎 Oylik: <b>39,000 so'm</b>\n"
            f"🏆 Yillik: <b>299,000 so'm</b> (36% chegirma)\n\n"
            f"7 kunlik bepul sinov bor! 🎁",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💎 Premium olish", callback_data="premium_info")],
                [InlineKeyboardButton(text="🎁 7 kun bepul sinov", callback_data="trial_start")],
            ])
        )
        return

    vazifa = get_vazifa(kasb, joriy_oy, joriy_oy_kun := prog["oy_ichi_kun"])
    if not vazifa:
        await bot.send_message(telegram_id, f"⚠️ Bugun vazifa topilmadi. Tez orada qo'shiladi!")
        return

    streak = await get_streak(telegram_id)

    # Streak emoji
    if streak == 0:
        streak_txt = "Bugun boshlang! 🚀"
    elif streak < 3:
        streak_txt = f"🔥 {streak} kun ketma-ket!"
    elif streak < 7:
        streak_txt = f"🔥🔥 {streak} kun! Zo'r ketayapsiz!"
    elif streak < 30:
        streak_txt = f"🔥🔥🔥 {streak} kun! Ustasiz!"
    else:
        streak_txt = f"💎 {streak} kun! Legendasiz!"

    # Vazifa xabari
    xabar = (
        f"☀️ <b>Xayrli tong, {ism}!</b>\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📅 <b>{joriy_oy}-oy | {joriy_kun}-kun</b>\n"
        f"💼 <b>{kasb}</b>\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"📌 <b>Bugungi vazifa:</b>\n"
        f"{vazifa['vazifa']}\n\n"
        f"⏱ <b>Vaqt:</b> {vazifa['vaqt']} daqiqa\n"
        f"⭐ <b>XP:</b> +{vazifa['xp']}\n\n"
        f"🔥 <b>Streak:</b> {streak_txt}\n\n"
        f"<i>Bajarsangiz ✅ tugmasini bosing!</i>"
    )

    await bot.send_message(
        telegram_id,
        xabar,
        parse_mode="HTML",
        reply_markup=vazifa_kb(joriy_kun)
    )

async def barcha_userlarga_vazifa(bot: Bot):
    """Vaqtga qarab barcha userlarga vazifa yuborish"""
    joriy_soat = datetime.now().hour
    users = await get_all_users()
    for telegram_id, ism in users:
        try:
            user = await get_user(telegram_id)
            if user:
                vazifa_vaqti = user[7] if user[7] else 8
                if vazifa_vaqti == joriy_soat:
                    await yuborilsin_bugungi_vazifa(bot, telegram_id)
                    await asyncio.sleep(0.1)  # Spam oldini olish
        except Exception as e:
            print(f"Vazifa yuborishda xato ({telegram_id}): {e}")

# ============================================================
# VAZIFA BAJARILDI
# ============================================================
@router.callback_query(F.data.startswith("bajarildi_"))
async def vazifa_bajarildi(call: CallbackQuery):
    kun = int(call.data.replace("bajarildi_", ""))
    telegram_id = call.from_user.id
    user = await get_user(telegram_id)
    if not user:
        return

    ism = user[2]
    bajarilgan_kunlar = await get_done_days(telegram_id)

    if kun in bajarilgan_kunlar:
        await call.answer("✅ Bu vazifani allaqachon bajargansiz!", show_alert=True)
        return

    await mark_done(telegram_id, kun)
    streak = await get_streak(telegram_id)
    prog = hisobla_progress(bajarilgan_kunlar + [kun])

    # Streak milestone
    milestone = ""
    if streak in [3, 7, 14, 30, 60, 100]:
        milestone = f"\n\n🏆 <b>MILESTONE!</b> {streak} kunlik streak! Siz ajoyibsiz!"

    await call.message.edit_reply_markup(reply_markup=vazifa_kb(kun, bajarilganmi=True))
    await call.message.answer(
        f"🎉 <b>Barakalla, {ism}!</b>\n\n"
        f"✅ {kun}-kun vazifasi bajarildi!\n"
        f"⭐ XP qo'shildi!\n"
        f"🔥 Streak: <b>{streak} kun</b>\n\n"
        f"📊 Umumiy progress: <b>{prog['foiz']}%</b>\n"
        f"<code>{prog['progress_bar']}</code>{milestone}",
        parse_mode="HTML"
    )

@router.callback_query(F.data == "already_done")
async def already_done(call: CallbackQuery):
    await call.answer("✅ Allaqachon bajargansiz! Zo'r!", show_alert=True)

# ============================================================
# YO'L XARITA — CHIROYLI VA SIRLI
# ============================================================
@router.callback_query(F.data == "yol_xarita")
@router.message(F.text.in_(["🗺 Yo'l xarita", "/yolxarita"]))
async def yol_xarita_handler(update):
    if isinstance(update, CallbackQuery):
        telegram_id = update.from_user.id
        send = update.message.answer
    else:
        telegram_id = update.from_user.id
        send = update.answer

    user = await get_user(telegram_id)
    if not user:
        await send("❌ Avval /start orqali ro'yxatdan o'ting!")
        return

    ism = user[2]
    kasb = user[6]
    bajarilgan_kunlar = await get_done_days(telegram_id)
    streak = await get_streak(telegram_id)
    prog = hisobla_progress(bajarilgan_kunlar)

    # ============ UMUMIY YO'L XARITA ============
    oy_holati = []
    for oy in range(1, 13):
        boshi = (oy - 1) * 30 + 1
        oxiri = oy * 30
        bajarilgan_oy = len([k for k in bajarilgan_kunlar if boshi <= k <= oxiri])

        if oy < prog["joriy_oy"]:
            if bajarilgan_oy == 30:
                emoji = "✅"
            else:
                emoji = "⚠️"
            holat = f"{emoji} {oy}-oy → {bajarilgan_oy}/30 kun"
        elif oy == prog["joriy_oy"]:
            emoji = "🔥"
            holat = f"{emoji} {oy}-oy → {prog['oy_ichi_kun']-1}/30 kun (hozir)"
        elif oy <= 2:
            emoji = "⏳"
            holat = f"{emoji} {oy}-oy → kutilmoqda (BEPUL)"
        else:
            emoji = "🔒"
            holat = f"{emoji} {oy}-oy → kutilmoqda (PREMIUM)"
        oy_holati.append(holat)

    xabar = (
        f"🗺 <b>{ism}ning Yo'l Xaritasi</b>\n\n"
        f"💼 <b>Kasb:</b> {kasb}\n"
        f"📊 <b>Umumiy progress:</b> {prog['foiz']}%\n"
        f"<code>[{prog['progress_bar']}]</code>\n\n"
        f"🏅 <b>Liga:</b> {prog['liga']}\n"
        f"🔥 <b>Streak:</b> {streak} kun\n"
        f"✅ <b>Bajarilgan:</b> {prog['bajarilgan']}/360 kun\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📅 <b>Bosqich:</b> {prog['bosqich']}\n"
        f"<i>{prog['bosqich_tavsif']}</i>\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"<b>12 Oylik Yo'l:</b>\n\n"
    )
    for holat in oy_holati:
        xabar += f"  {holat}\n"

    await send(
        xabar,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔮 Keyingi 7 kun", callback_data="preview_7kun")],
            [InlineKeyboardButton(text="📋 Bugungi vazifa", callback_data="bugungi_vazifa")],
        ])
    )

# ============================================================
# KEYINGI 7 KUN PREVIEW — SIRLI VA QIZIQARLI
# ============================================================
@router.callback_query(F.data == "preview_7kun")
async def preview_7kun(call: CallbackQuery):
    telegram_id = call.from_user.id
    user = await get_user(telegram_id)
    if not user:
        return

    kasb = user[6]
    premium = user[10]
    bajarilgan_kunlar = await get_done_days(telegram_id)
    prog = hisobla_progress(bajarilgan_kunlar)

    await call.message.answer("🔮 Keyingi 7 kun yuklanmoqda...")
    await asyncio.sleep(1)

    vazifalar = get_keyingi_7_kun(kasb, prog["joriy_oy"], prog["oy_ichi_kun"])

    if not vazifalar:
        await call.message.answer("⚠️ Keyingi vazifalar topilmadi.")
        return

    xabar = f"🔮 <b>Keyingi 7 kun — sizni nima kutmoqda:</b>\n\n"

    for i, v in enumerate(vazifalar, 1):
        kun_raqami = prog["joriy_kun"] + i
        oy = v["oy"]

        # Premium kunlar uchun yashirin
        if oy > 2 and not premium:
            xabar += (
                f"<b>{i}.</b> {kun_raqami}-kun ({oy}-oy)\n"
                f"   🔒 <i>Premium vazifa — yashirin</i>\n\n"
            )
        else:
            # Vazifani qisqartirish (50 belgi)
            vazifa_qisqa = v['vazifa'][:50] + "..." if len(v['vazifa']) > 50 else v['vazifa']
            xabar += (
                f"<b>{i}.</b> {kun_raqami}-kun\n"
                f"   📌 {vazifa_qisqa}\n"
                f"   ⭐ +{v['xp']} XP\n\n"
            )

    xabar += f"<i>💡 Har kuni yangi sirlar ochiladi! Davom eting...</i>"

    await call.message.answer(
        xabar,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗺 To'liq yo'l xarita", callback_data="yol_xarita")],
            [InlineKeyboardButton(text="📋 Bugungi vazifa", callback_data="bugungi_vazifa")],
        ])
    )

# ============================================================
# BUGUNGI VAZIFA TUGMASI
# ============================================================
@router.callback_query(F.data == "bugungi_vazifa")
@router.message(F.text.in_(["📋 Bugungi vazifa", "/vazifa"]))
async def bugungi_vazifa_handler(update):
    if isinstance(update, CallbackQuery):
        telegram_id = update.from_user.id
        bot = update.bot
    else:
        telegram_id = update.from_user.id
        bot = update.bot

    await yuborilsin_bugungi_vazifa(bot, telegram_id)

# ============================================================
# SCHEDULER — Har soatda tekshirib vazifa yuboradi
# ============================================================
def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
    scheduler.add_job(
        barcha_userlarga_vazifa,
        trigger="cron",
        minute=0,  # Har soatning boshida
        args=[bot],
        id="kunlik_vazifa"
    )
    return scheduler
