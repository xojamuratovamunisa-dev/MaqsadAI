from aiogram import Router, Bot, F
from aiogram.types import (Message, ReplyKeyboardMarkup, KeyboardButton,
                            ReplyKeyboardRemove, InlineKeyboardMarkup,
                            InlineKeyboardButton, CallbackQuery)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
import re
import asyncio

from db import save_user
from menus import yonalish_keyboard, kasb_keyboard

router = Router()

CHANNEL_ID = "@AI_Maqsad"
INSTAGRAM = "instagram.com/maqsadai"

# ============================================================
# KASB MA'LUMOTLARI
# ============================================================
KASB_MALUMOTLARI = {
    "👨‍💻 Dasturchi": {"emoji": "👨‍💻", "tavsif": "Dasturchilar kompyuter dasturlari, ilovalar va veb saytlar yaratadi.", "maosh": "O'zbekistonda: $500-3000/oy | Xorijda: $3000-15000/oy", "kelajak": "IT sohasi tez rivojlanmoqda. Sun'iy intellekt, mobil ilovalar va cloud texnologiyalar bo'yicha talab katta!", "talablar": "Python, JavaScript, SQL bilimi. Ingliz tili muhim.", "universitetlar": "TATU, INHA, Webster, Turin Polytechnic"},
    "🤖 AI Engineer": {"emoji": "🤖", "tavsif": "AI muhandislari sun'iy intellekt tizimlarini loyihalaydi va amalga oshiradi.", "maosh": "O'zbekistonda: $800-4000/oy | Xorijda: $5000-20000/oy", "kelajak": "Dunyodagi eng istiqbolli kasb!", "talablar": "Python, matematika, Machine Learning.", "universitetlar": "TATU, MIT (xorij), Stanford (xorij)"},
    "🔐 Cybersecurity Specialist": {"emoji": "🔐", "tavsif": "Kiberjamiyat mutaxassislari kompaniyalar va davlatni xaker hujumlaridan himoya qiladi.", "maosh": "O'zbekistonda: $600-2500/oy | Xorijda: $4000-18000/oy", "kelajak": "Raqamli dunyoda xavfsizlik talab katta.", "talablar": "Network, Linux, kriptografiya. CEH, CISSP sertifikatlari.", "universitetlar": "TATU, Milliy gvardiya akademiyasi"},
    "📊 Data Analyst": {"emoji": "📊", "tavsif": "Ma'lumotlar tahlilchilari katta hajmdagi ma'lumotlardan foydali xulosalar chiqaradi.", "maosh": "O'zbekistonda: $500-2000/oy | Xorijda: $3500-12000/oy", "kelajak": "Har bir kompaniya ma'lumotlar asosida qaror qabul qilmoqda.", "talablar": "Excel, SQL, Python, Tableau.", "universitetlar": "TATU, ToshDU, INHA"},
    "🎮 Game Developer": {"emoji": "🎮", "tavsif": "O'yin dasturchilar kompyuter va mobil o'yinlar yaratadi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy", "kelajak": "O'yin sanoati yiliga $200 milliarddan ortiq.", "talablar": "Unity yoki Unreal Engine, C# yoki C++.", "universitetlar": "TATU, xususiy kurslar"},
    "🚀 Startup Founder": {"emoji": "🚀", "tavsif": "Startap asoschilari yangi biznes g'oyalarini hayotga tadbiq etadi.", "maosh": "Cheksiz!", "kelajak": "O'zbekistonda startap ekotizimi rivojlanmoqda.", "talablar": "Biznes tafakkuri, liderlik, muammo hal qilish.", "universitetlar": "Westminster, Turin, INHA"},
    "👔 CEO": {"emoji": "👔", "tavsif": "Bosh ijrochi direktor kompaniyani boshqaradi, strategiya belgilaydi.", "maosh": "O'zbekistonda: $2000-20000/oy | Xorijda: cheksiz", "kelajak": "Har doim kerak.", "talablar": "MBA darajasi, liderlik, moliya, marketing.", "universitetlar": "Westminster MBA, TIQXMMI"},
    "📦 Product Manager": {"emoji": "📦", "tavsif": "Mahsulot menejeri IT mahsulotning strategiyasini belgilaydi.", "maosh": "O'zbekistonda: $800-3000/oy | Xorijda: $5000-20000/oy", "kelajak": "IT kompaniyalarning eng talab qilinadigan kasbi.", "talablar": "IT va biznes bilimlari, analitik fikrlash.", "universitetlar": "INHA, Westminster"},
    "📋 Project Manager": {"emoji": "📋", "tavsif": "Loyiha menejeri loyihalarni boshidan oxirigacha boshqaradi.", "maosh": "O'zbekistonda: $600-2500/oy | Xorijda: $4000-15000/oy", "kelajak": "Barcha sohalarda kerak.", "talablar": "PMP sertifikati, Agile/Scrum.", "universitetlar": "Har qanday universitet + PMP"},
    "💡 Biznes Konsultant": {"emoji": "💡", "tavsif": "Biznes konsultantlar kompaniyalarga muammolarini aniqlash va yechim topishda yordam beradi.", "maosh": "O'zbekistonda: $500-3000/oy | Xorijda: $3000-15000/oy", "kelajak": "McKinsey, BCG kabi konsalting firmalari eng yuqori maosh to'laydi!", "talablar": "Tahliliy fikrlash, biznes bilimlari.", "universitetlar": "Westminster, TIQXMMI"},
    "📈 Trader": {"emoji": "📈", "tavsif": "Treyderlar fond bozori, valyuta yoki kripto bozorlarida savdo qilib daromad oladi.", "maosh": "Cheksiz.", "kelajak": "Raqamli moliya va kripto bozorlar kengaymoqda.", "talablar": "Texnik tahlil, moliya bilimlari.", "universitetlar": "ToshDU + o'z-o'zini o'qitish"},
    "💹 Investor": {"emoji": "💹", "tavsif": "Investorlar kompaniyalar yoki loyihalarga pul tikib, daromad oladi.", "maosh": "Cheksiz.", "kelajak": "O'zbekiston investitsiya muhiti yaxshilanmoqda.", "talablar": "Moliya tahlili, risk baholash.", "universitetlar": "ToshDU, Westminster + CFA"},
    "📊 Financial Analyst": {"emoji": "📊", "tavsif": "Moliyaviy tahlilchilar kompaniyalar va investitsiyalarni baholab, tavsiyalar beradi.", "maosh": "O'zbekistonda: $600-2500/oy | Xorijda: $4000-15000/oy", "kelajak": "Bank, moliya kompaniyalari uchun zarur.", "talablar": "Excel, moliya modellashtirish, CFA.", "universitetlar": "ToshDU, Westminster"},
    "🧾 Accountant": {"emoji": "🧾", "tavsif": "Buxgalterlar moliyaviy hisobotlarni yuritadi.", "maosh": "O'zbekistonda: $400-1500/oy | Xorijda: $3000-8000/oy", "kelajak": "Har bir tashkilotga kerak.", "talablar": "1C, soliq qonunchiligi, ACCA.", "universitetlar": "ToshDU, TIQXMMI"},
    "🏦 Bankir": {"emoji": "🏦", "tavsif": "Bankirlar kredit berish va moliyaviy xizmatlarni boshqaradi.", "maosh": "O'zbekistonda: $500-3000/oy | Xorijda: $3000-20000/oy", "kelajak": "Raqamli bank va fintech rivojlanmoqda.", "talablar": "Moliya bilimlari, CFA/MBA.", "universitetlar": "ToshDU, Moliya instituti"},
    "🖼️ Grafik Dizayner": {"emoji": "🖼️", "tavsif": "Grafik dizaynerlar logo, broshyura, reklama va vizual materiallar yaratadi.", "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $2000-8000/oy", "kelajak": "Har bir biznesga kerak.", "talablar": "Adobe Photoshop, Illustrator, Figma.", "universitetlar": "Kamolot, San'at akademiyasi"},
    "📱 UI/UX Dizayner": {"emoji": "📱", "tavsif": "UI/UX dizaynerlar ilova va veb saytlarning foydalanuvchilar uchun qulay bo'lishini ta'minlaydi.", "maosh": "O'zbekistonda: $500-2500/oy | Xorijda: $4000-15000/oy", "kelajak": "IT kompaniyalar uchun eng zarur mutaxassis.", "talablar": "Figma, Adobe XD, foydalanuvchi psixologiyasi.", "universitetlar": "TATU, Amaliy san'at"},
    "🎬 Motion Dizayner": {"emoji": "🎬", "tavsif": "Motion dizaynerlar animatsiya va video effektlar yaratadi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy", "kelajak": "Video kontent o'sishi bilan talab yuqori.", "talablar": "After Effects, Cinema 4D, Premiere Pro.", "universitetlar": "San'at akademiyasi"},
    "🗿 3D Artist": {"emoji": "🗿", "tavsif": "3D artistlar uch o'lchamli modellar va animatsiyalar yaratadi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-15000/oy", "kelajak": "O'yin, kino, arxitektura uchun katta talab.", "talablar": "Blender, Maya, 3ds Max.", "universitetlar": "San'at akademiyasi"},
    "🌐 Web Dizayner": {"emoji": "🌐", "tavsif": "Veb dizaynerlar chiroyli va qulay veb saytlar yaratadi.", "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $2500-10000/oy", "kelajak": "Hamma biznes veb sayt kerak.", "talablar": "Figma, HTML/CSS asoslari.", "universitetlar": "TATU + online kurslar"},
    "📹 YouTuber": {"emoji": "📹", "tavsif": "YouTuberlar video kontent yaratib, auditoriya to'playdi.", "maosh": "Cheksiz — 100 ming obunachidan $1000-10000/oy", "kelajak": "Video kontent iste'moli o'sib bormoqda.", "talablar": "Kamera, montaj, ijodkorlik.", "universitetlar": "Maxsus ta'lim shart emas"},
    "✍️ Blogger": {"emoji": "✍️", "tavsif": "Bloggerlar matn, foto yoki video orqali kontent yaratadi.", "maosh": "Cheksiz.", "kelajak": "Personal brend va influencer marketing o'sib bormoqda.", "talablar": "Yozish ko'nikmalari, ijodkorlik.", "universitetlar": "Maxsus ta'lim shart emas"},
    "🎞️ Video Editor": {"emoji": "🎞️", "tavsif": "Video montajchilar xom video materiallarni professional ko'rinishga keltiradi.", "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $2000-8000/oy", "kelajak": "Har bir media kompaniyasiga kerak.", "talablar": "Premiere Pro, After Effects, CapCut.", "universitetlar": "San'at akademiyasi"},
    "🎮 Streamer": {"emoji": "🎮", "tavsif": "Streamerlar o'yin yoki boshqa kontentni jonli efirda ko'rsatadi.", "maosh": "Cheksiz.", "kelajak": "Esport va streaming sanoati tez rivojlanmoqda.", "talablar": "Xarizmatik shaxsiyat, OBS, kamera.", "universitetlar": "Maxsus ta'lim shart emas"},
    "📰 Jurnalist": {"emoji": "📰", "tavsif": "Jurnalistlar yangilik yig'ib, tahlil qilib, jamoatchilika yetkazadi.", "maosh": "O'zbekistonda: $300-1200/oy | Xorijda: $2000-8000/oy", "kelajak": "Raqamli jurnalistika yangi imkoniyatlar ochmoqda.", "talablar": "Yozish, intervyu olish, ob'ektivlik.", "universitetlar": "O'zMU jurnalistika, ToshDU"},
    "🎤 Singer": {"emoji": "🎤", "tavsif": "Qo'shiqchilar konsert, studiya yozuvi va ijro orqali o'z san'atini namoyish etadi.", "maosh": "Cheksiz.", "kelajak": "Musiqa sanoati o'smoqda.", "talablar": "Vokal mahorati, sahna tajribasi.", "universitetlar": "Davlat konservatoriyasi"},
    "🎭 Aktyor": {"emoji": "🎭", "tavsif": "Aktyorlar teatr, kino va televizion loyihalarda rol o'ynaydi.", "maosh": "O'zbekistonda: $300-5000/loyiha | Xorijda: cheksiz", "kelajak": "O'zbek kinosi va seriallar sanoati rivojlanmoqda.", "talablar": "Aktyorlik ko'nikmalari, plastika, nutq.", "universitetlar": "Davlat san'at instituti"},
    "🎵 Musiqachi": {"emoji": "🎵", "tavsif": "Musiqachilar cholg'u asbob chaladi, kuy bichadi.", "maosh": "Cheksiz.", "kelajak": "Musiqa sanoati o'smoqda.", "talablar": "Cholg'u asbob mahorati, nota bilimi.", "universitetlar": "Davlat konservatoriyasi"},
    "🎧 DJ": {"emoji": "🎧", "tavsif": "DJ-lar musiqa mikslab, konsert va tadbirlarda his-hayajon beradi.", "maosh": "O'zbekistonda: $200-2000/tadbir | Xorijda: cheksiz", "kelajak": "Klub, to'y va festival sanoati katta.", "talablar": "Musiqa hisi, DJ jihozlari, mikslash texnikasi.", "universitetlar": "Maxsus ta'lim shart emas"},
    "🎬 Rejissyor": {"emoji": "🎬", "tavsif": "Rejissyorlar film, serial yoki teatr spektaklini boshqaradi.", "maosh": "O'zbekistonda: $500-10000/loyiha | Xorijda: cheksiz", "kelajak": "O'zbek kinosi rivojlanmoqda.", "talablar": "Rejissyorlik mahorati, skript tahlili.", "universitetlar": "Davlat san'at instituti"},
    "🏛️ Arxitektor": {"emoji": "🏛️", "tavsif": "Arxitektorlar binolar va inshootlar loyihasini yaratadi.", "maosh": "O'zbekistonda: $500-3000/oy | Xorijda: $4000-15000/oy", "kelajak": "O'zbekistonda qurilish sanoati tez rivojlanmoqda.", "talablar": "AutoCAD, ArchiCAD, Revit, ijodkorlik.", "universitetlar": "ToshDTU, TIQXMMI arxitektura"},
    "🛋️ Interyer Dizayner": {"emoji": "🛋️", "tavsif": "Interyer dizaynerlar xona va binolarning ichki ko'rinishini chiroyli qiladi.", "maosh": "O'zbekistonda: $400-2500/oy | Xorijda: $3000-12000/oy", "kelajak": "Ko'chmas mulk bozori o'sishi bilan talab yuqori.", "talablar": "AutoCAD, 3ds Max, rang nazariyasi.", "universitetlar": "ToshDTU, San'at instituti"},
    "🏙️ Urban Planner": {"emoji": "🏙️", "tavsif": "Shaharsozlar shahar rivojlanish rejalarini ishlab chiqadi.", "maosh": "O'zbekistonda: $500-2000/oy | Xorijda: $4000-12000/oy", "kelajak": "Toshkent shaharsozligi uchun zarur.", "talablar": "GIS dasturlari, shaharsozlik qonunchiligi.", "universitetlar": "ToshDTU"},
    "🌿 Landshaft Dizayner": {"emoji": "🌿", "tavsif": "Landshaft dizaynerlar bog' va park maydonlarini rejalashtiradi.", "maosh": "O'zbekistonda: $400-1800/oy | Xorijda: $3000-10000/oy", "kelajak": "Yashil shaharlar konsepti o'sishi bilan talab kuchaymoqda.", "talablar": "O'simlikshunoslik, AutoCAD, ekologiya.", "universitetlar": "ToshDTU"},
    "👷 Qurilish Muhandisi": {"emoji": "👷", "tavsif": "Qurilish muhandislari loyiha hujjatlarini tayyorlaydi va qurilishni nazorat qiladi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy", "kelajak": "O'zbekiston qurilish boomi.", "talablar": "AutoCAD, qurilish materiallar, hisob-kitob.", "universitetlar": "ToshDTU"},
    "🤖 Robototexnika Muhandisi": {"emoji": "🤖", "tavsif": "Robototexnika muhandislari robotlar va avtomatlashtirilgan tizimlarni loyihalaydi.", "maosh": "O'zbekistonda: $600-2500/oy | Xorijda: $5000-18000/oy", "kelajak": "Sanoat avtomatlashtirish juda istiqbolli!", "talablar": "Mexanika, elektronika, dasturlash.", "universitetlar": "TATU, ToshDTU"},
    "⚡ Elektr Muhandisi": {"emoji": "⚡", "tavsif": "Elektr muhandislari elektr tizimlarini loyihalaydi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $4000-12000/oy", "kelajak": "Yangilanuvchi energiya sohasida katta talab.", "talablar": "Elektrotexnika, AutoCAD.", "universitetlar": "TATU, ToshDTU"},
    "🔧 Mexanik Muhandis": {"emoji": "🔧", "tavsif": "Mexanik muhandislar mashinalar va mexanik tizimlarni loyihalaydi.", "maosh": "O'zbekistonda: $400-1800/oy | Xorijda: $3500-12000/oy", "kelajak": "Avtomobil, aviatsiya sanoatida zarur.", "talablar": "SolidWorks, materialshunoslik.", "universitetlar": "ToshDTU"},
    "🏭 Avtomatika Muhandisi": {"emoji": "🏭", "tavsif": "Avtomatika muhandislari ishlab chiqarish jarayonlarini avtomatlashtirishni loyihalaydi.", "maosh": "O'zbekistonda: $500-2000/oy | Xorijda: $4000-14000/oy", "kelajak": "Sanoat 4.0 va aqlli fabrikalar!", "talablar": "PLC dasturlash, SCADA, robotika.", "universitetlar": "TATU, ToshDTU"},
    "🏗️ Sanoat Muhandisi": {"emoji": "🏗️", "tavsif": "Sanoat muhandislari ishlab chiqarish samaradorligini oshirish uchun tizimlar yaratadi.", "maosh": "O'zbekistonda: $400-1800/oy | Xorijda: $4000-13000/oy", "kelajak": "Lean va Six Sigma metodologiyalari bilan sanoat samaradorligi oshirilmoqda.", "talablar": "Lean, Six Sigma.", "universitetlar": "ToshDTU"},
    "👨‍⚕️ Shifokor": {"emoji": "👨‍⚕️", "tavsif": "Shifokorlar kasalliklarni tashxislaydi va davolaydi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $6000-30000/oy", "kelajak": "Tibbiyot doimo zarur.", "talablar": "6 yillik tibbiyot ta'limi + rezidentura.", "universitetlar": "ToshDTI, Samarqand DTI"},
    "🔪 Jarroh": {"emoji": "🔪", "tavsif": "Jarrohlar operatsiya orqali kasalliklarni davolaydi.", "maosh": "O'zbekistonda: $600-3000/oy | Xorijda: $10000-40000/oy", "kelajak": "Robot-assistli jarrohlik kelajagi katta.", "talablar": "8+ yillik ta'lim, qo'l mahorati.", "universitetlar": "ToshDTI"},
    "🦷 Stomatolog": {"emoji": "🦷", "tavsif": "Stomatologlar tish va og'iz kasalliklarini davolaydi.", "maosh": "O'zbekistonda: $500-3000/oy | Xorijda: $5000-20000/oy", "kelajak": "Xususiy stomatologiya klinikalari ko'paymoqda.", "talablar": "5 yillik ta'lim, nozik qo'l ishi.", "universitetlar": "ToshDTI"},
    "❤️ Kardiolog": {"emoji": "❤️", "tavsif": "Kardiologlar yurak va qon tomir kasalliklarini davolaydi.", "maosh": "O'zbekistonda: $600-2500/oy | Xorijda: $8000-30000/oy", "kelajak": "Yurak kasalliklari dunyoda eng ko'p tarqalgan.", "talablar": "8+ yillik ta'lim, EKG.", "universitetlar": "ToshDTI, Kardiologiya instituti"},
    "🧠 Psixiatr": {"emoji": "🧠", "tavsif": "Psixiatrlar ruhiy kasalliklarni tashxislaydi va davolaydi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $7000-25000/oy", "kelajak": "Mental salomatlik muammolari o'smoqda.", "talablar": "8+ yillik ta'lim, empatiya.", "universitetlar": "ToshDTI"},
    "🧠 Psixolog": {"emoji": "🧠", "tavsif": "Psixologlar odamlarning ruhiy holatini baholaydi.", "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $3000-12000/oy", "kelajak": "Mental salomatlik trendining o'sishi bilan talab oshmoqda.", "talablar": "Psixologiya ta'limi, empatiya.", "universitetlar": "O'zMU, TDPU"},
    "💆 Psixoterapevt": {"emoji": "💆", "tavsif": "Psixoterapevtlar mijozlarga uzoq muddatli terapiya orqali yordam beradi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $4000-15000/oy", "kelajak": "Onlayn terapiya platformalari global imkoniyat ochmoqda.", "talablar": "Psixologiya magistri, sertifikat.", "universitetlar": "O'zMU"},
    "👥 HR Mutaxassisi": {"emoji": "👥", "tavsif": "HR mutaxassislari xodimlarni yollash va o'qitishni boshqaradi.", "maosh": "O'zbekistonda: $400-1800/oy | Xorijda: $3000-10000/oy", "kelajak": "Har bir kompaniya HR kerak.", "talablar": "Psixologiya, kommunikatsiya, mehnat qonunchiligi.", "universitetlar": "O'zMU, TIQXMMI"},
    "🎯 Career Coach": {"emoji": "🎯", "tavsif": "Karyera kouchilar odamlarga karyera yo'lini topishda yordam beradi.", "maosh": "O'zbekistonda: $300-2000/oy | Xorijda: $3000-15000/oy", "kelajak": "Karyera maslahat xizmatlariga talab oshib bormoqda.", "talablar": "Psixologiya, coaching sertifikati (ICF).", "universitetlar": "O'zMU + ICF"},
    "👨‍👩‍👧 Oilaviy Psixolog": {"emoji": "👨‍👩‍👧", "tavsif": "Oilaviy psixologlar oila munosabatlaridagi muammolarni hal qilishga yordam beradi.", "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $3500-12000/oy", "kelajak": "Oila masalasi doimo dolzarb.", "talablar": "Oilaviy terapiya sertifikati, empatiya.", "universitetlar": "O'zMU"},
    "📚 O'qituvchi": {"emoji": "📚", "tavsif": "O'qituvchilar bilim beradi, yoshlarni tarbiyalaydi.", "maosh": "O'zbekistonda: $200-800/oy | Xususiy: $500-2000/oy", "kelajak": "Xususiy maktablar o'sishi bilan talab oshmoqda.", "talablar": "Pedagog ta'limi, sabr, kommunikatsiya.", "universitetlar": "TDPU, ToshDU"},
    "🎓 Professor": {"emoji": "🎓", "tavsif": "Professorlar oliy ta'limda dars beradi, ilmiy tadqiqot o'tkazadi.", "maosh": "O'zbekistonda: $400-1500/oy | Xorijda: $5000-20000/oy", "kelajak": "Xalqaro universitetlar doktorantlar qidirmoqda.", "talablar": "PhD darajasi, ilmiy maqolalar.", "universitetlar": "Har qanday yetakchi universitet"},
    "🧑‍🏫 Mentor": {"emoji": "🧑‍🏫", "tavsif": "Mentorlar shaxsiy tajribalarini bo'lishib, boshqalarga yo'l ko'rsatadi.", "maosh": "Cheksiz.", "kelajak": "Online mentoring platformalari global bozor ochmoqda.", "talablar": "Tajriba, empatiya, kommunikatsiya.", "universitetlar": "Maxsus ta'lim shart emas"},
    "💪 Trener": {"emoji": "💪", "tavsif": "Trenerlar sport, biznes yoki hayot ko'nikmalarini o'rgatadi.", "maosh": "O'zbekistonda: $300-2000/oy | Xorijda: cheksiz", "kelajak": "Onlayn treninglar global auditoriya bermoqda.", "talablar": "Sertifikat, tajriba, motivatsiya.", "universitetlar": "Sport akademiyasi + sertifikatlar"},
    "🏫 Ta'lim Menejeri": {"emoji": "🏫", "tavsif": "Ta'lim menejerlari maktab yoki ta'lim muassasasini boshqaradi.", "maosh": "O'zbekistonda: $500-2000/oy", "kelajak": "Xususiy maktab va EdTech kompaniyalar kengaymoqda.", "talablar": "Boshqaruv, pedagogika, moliya.", "universitetlar": "TDPU, TIQXMMI"},
    "⚖️ Advokat": {"emoji": "⚖️", "tavsif": "Advokatlar sud jarayonlarida mijozlarini himoya qiladi.", "maosh": "O'zbekistonda: $400-5000/oy | Xorijda: $5000-30000/oy", "kelajak": "Biznes va xususiy huquqiy xizmatlarga talab oshmoqda.", "talablar": "Yuridik ta'lim, advokat sertifikati, nutq san'ati.", "universitetlar": "ToshDYUI, O'zMU huquq"},
    "📜 Yurist": {"emoji": "📜", "tavsif": "Yuristlar huquqiy masalalar bo'yicha maslahat beradi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-15000/oy", "kelajak": "Korxonalar va davlat tashkilotlarda doimiy talab.", "talablar": "Yuridik ta'lim, qonunchilik.", "universitetlar": "ToshDYUI, O'zMU"},
    "👮 Prokuror": {"emoji": "👮", "tavsif": "Prokurorlar jinoyat ishlarini ko'rib chiqadi.", "maosh": "O'zbekistonda: $400-1500/oy + imtiyozlar", "kelajak": "Davlat xizmatida barqaror ish.", "talablar": "Yuridik ta'lim, prokuratura akademiyasi.", "universitetlar": "ToshDYUI, Prokuratura akademiyasi"},
    "🏛️ Sudya": {"emoji": "🏛️", "tavsif": "Sudyalar qonun asosida sud ishlarini ko'rib chiqib, adolatli qaror chiqaradi.", "maosh": "O'zbekistonda: $600-2000/oy + imtiyozlar", "kelajak": "Sud tizimi islohoti davom etmoqda.", "talablar": "Yuridik ta'lim, 5+ yil tajriba.", "universitetlar": "ToshDYUI, Sud akademiyasi"},
    "🔍 Tergovchi": {"emoji": "🔍", "tavsif": "Tergovchilar jinoyat ishlarini o'rganib, dalillar yig'adi.", "maosh": "O'zbekistonda: $350-1200/oy + imtiyozlar", "kelajak": "Kiber jinoyatlar yangi yo'nalish.", "talablar": "Yuridik ta'lim, kriminalistika.", "universitetlar": "ToshDYUI, IIV akademiyasi"},
    "📱 SMM Manager": {"emoji": "📱", "tavsif": "SMM menejerlar ijtimoiy tarmoqlarda brend sahifalarini boshqaradi.", "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $2000-8000/oy", "kelajak": "Har bir brend ijtimoiy tarmoq kerak.", "talablar": "Kontent yaratish, tahlil, ijodkorlik.", "universitetlar": "Marketing kurslari + amaliyot"},
    "🔍 SEO Specialist": {"emoji": "🔍", "tavsif": "SEO mutaxassislari veb saytlarni Google tepasiga chiqaradi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy", "kelajak": "Raqamli marketing o'sishi bilan talab katta.", "talablar": "Google Analytics, Ahrefs, kalit so'z tahlili.", "universitetlar": "Online kurslar + amaliyot"},
    "💻 Digital Marketer": {"emoji": "💻", "tavsif": "Raqamli marketologlar onlayn kanallar orqali mahsulot targ'ib qiladi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy", "kelajak": "Bizneslar raqamli kanalga o'tmoqda.", "talablar": "Google Ads, Facebook Ads, SEO.", "universitetlar": "Marketing kurslari, Google sertifikatlari"},
    "🏷️ Brand Manager": {"emoji": "🏷️", "tavsif": "Brend menejerlari kompaniya brendining qiyofasini boshqaradi.", "maosh": "O'zbekistonda: $500-2500/oy | Xorijda: $4000-15000/oy", "kelajak": "Global brendlar va mahalliy kompaniyalar uchun zarur.", "talablar": "Marketing strategiyasi, kommunikatsiya.", "universitetlar": "TIQXMMI, Westminster"},
    "✍️ Copywriter": {"emoji": "✍️", "tavsif": "Kopirayterlar reklama va marketing uchun sotuv qiluvchi matn yozadi.", "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $2000-10000/oy", "kelajak": "Kontent marketing o'sishi bilan talab oshmoqda.", "talablar": "Yozish ko'nikmalari, psixologiya, marketing.", "universitetlar": "Jurnalistika + marketing kurslari"},
    "🤝 Diplomat": {"emoji": "🤝", "tavsif": "Diplomatlar mamlakatlar o'rtasida munosabatlarni boshqaradi.", "maosh": "O'zbekistonda: $600-3000/oy + imtiyozlar", "kelajak": "O'zbekiston xalqaro aloqalarini kengaytirmoqda.", "talablar": "Xalqaro aloqalar ta'limi, til bilimlari (3+).", "universitetlar": "O'zMU XHXF, TMDH"},
    "🗣️ Tarjimon": {"emoji": "🗣️", "tavsif": "Tarjimonlar tillar o'rtasida ma'no va g'oyalarni yetkazadi.", "maosh": "O'zbekistonda: $300-2000/oy | Xorijda: $2000-10000/oy", "kelajak": "Sifatli tarjimonlar kerak bo'lib qolaveradi.", "talablar": "2+ til mukammal bilimi, madaniy tushuncha.", "universitetlar": "O'zMU filologiya, ToshDU"},
    "🌐 Xalqaro Menejer": {"emoji": "🌐", "tavsif": "Xalqaro menejerlar global kompaniyalarning xorijiy operatsiyalarini boshqaradi.", "maosh": "O'zbekistonda: $600-3000/oy | Xorijda: $4000-20000/oy", "kelajak": "Multinatsional kompaniyalar O'zbekistonga kirib kelmoqda.", "talablar": "MBA, ingliz tili, menejment.", "universitetlar": "Westminster, Turin"},
    "🏛️ Elchixona Xodimi": {"emoji": "🏛️", "tavsif": "Elchixona xodimlari xorijdagi vatandoshlar manfaatini himoya qiladi.", "maosh": "O'zbekistonda: $400-1500/oy + xorijda yashash imtiyozlari", "kelajak": "Diplomatik korpus barqaror va nufuzli kasb.", "talablar": "XH ta'limi, til bilimlari, protokol.", "universitetlar": "O'zMU XHXF, TMDH"},
    "📦 Tashqi Savdo Mutaxassisi": {"emoji": "📦", "tavsif": "Tashqi savdo mutaxassislari eksport-import operatsiyalarini boshqaradi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy", "kelajak": "O'zbekiston eksportini oshirish siyosati bu kasb talabini oshirmoqda.", "talablar": "Savdo huquqi, til bilimlari, logistika.", "universitetlar": "TIQXMMI"},
    "🗺️ Tur Menejer": {"emoji": "🗺️", "tavsif": "Tur menejerlar turistik marshrut va paketlarni tashkil qiladi.", "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $2000-8000/oy", "kelajak": "O'zbekistonga turizm o'smoqda.", "talablar": "Turizm ta'limi, til bilimlari, kommunikatsiya.", "universitetlar": "ToshDTU turizm"},
    "🧭 Gid": {"emoji": "🧭", "tavsif": "Gidlar turistlarni tarixiy joylarda olib yuradi.", "maosh": "O'zbekistonda: $20-100/tur | Xorijda: $50-500/kun", "kelajak": "Chet ellik turistlar uchun malakali gidlar yetishmayapti.", "talablar": "Til bilimlari, tarix, kommunikatsiya.", "universitetlar": "Turizm instituti + til kurslari"},
    "🏨 Hotel Manager": {"emoji": "🏨", "tavsif": "Hotel menejerlari mehmonxona operatsiyalarini boshqaradi.", "maosh": "O'zbekistonda: $500-2500/oy | Xorijda: $3000-15000/oy", "kelajak": "Yangi mehmonxonalar qurilishi bilan menejerlar kerak.", "talablar": "Gostepriimlik menejment, til bilimlari.", "universitetlar": "ToshDTU"},
    "📸 Travel Blogger": {"emoji": "📸", "tavsif": "Sayohat bloggerlar safari davomida kontent yaratib, auditoriya to'playdi.", "maosh": "Cheksiz.", "kelajak": "Sayohat kontenti qiziqishi o'smoqda.", "talablar": "Fotografiya, video montaj, yozish, SEO.", "universitetlar": "Maxsus ta'lim shart emas"},
    "✈️ Pilot": {"emoji": "✈️", "tavsif": "Pilotlar yo'lovchi va yuk samolyotlarini boshqaradi.", "maosh": "O'zbekistonda: $1500-5000/oy | Xorijda: $5000-25000/oy", "kelajak": "O'zbekiston aviatsiyasi kengaymoqda.", "talablar": "Aviatsiya akademiyasi, PPL/CPL, ingliz tili.", "universitetlar": "O'zbekiston Aviatsiya akademiyasi"},
    "⚽ Futbolchi": {"emoji": "⚽", "tavsif": "Professional futbolchilar sport klublari uchun o'ynaydi.", "maosh": "O'zbekistonda: $500-5000/oy | Xorijda: cheksiz", "kelajak": "O'zbek futboli rivojlanmoqda.", "talablar": "Jismoniy tayyorgarlik, texnika, taktika.", "universitetlar": "RSSSMM, futbol akademiyalari"},
    "🥊 Bokschi": {"emoji": "🥊", "tavsif": "Professional bokschlar ring raqobatida kurashadi.", "maosh": "O'zbekistonda: $300-2000/musobaqa | Xorijda: cheksiz", "kelajak": "O'zbek bokschilar olimpiya chempionlari.", "talablar": "Texnika, jismoniy kuch, taktika.", "universitetlar": "Sport akademiyalari, boks maktablari"},
    "🥋 UFC Jangchisi": {"emoji": "🥋", "tavsif": "UFC jangchilar aralash kurash (MMA) bilan shug'ullanadi.", "maosh": "UFC: $10,000-100,000+/musobaqa", "kelajak": "MMA sanoati tez o'smoqda.", "talablar": "Ko'p kurash turi, jismoniy tayyorgarlik.", "universitetlar": "Sport akademiyalari"},
    "🏀 Basketbolchi": {"emoji": "🏀", "tavsif": "Professional basketbolchilar jamoalar uchun o'ynaydi.", "maosh": "O'zbekistonda: $300-2000/oy | NBA: millionlar", "kelajak": "Yosh iqtidorlarni chet el klublari qidirmoqda.", "talablar": "Bo'y, texnika, jamoaviy o'yin.", "universitetlar": "RSSSMM, sport akademiyalari"},
    "🎾 Tennischi": {"emoji": "🎾", "tavsif": "Professional tennis o'yinchilar ATP/WTA turnirlarida qatnashadi.", "maosh": "Cheksiz — Grand Slam g'oliblar millionlar ishlaydi", "kelajak": "O'zbek tennischilari xalqaro reyting olmoqda.", "talablar": "Texnika, jismoniy tayyorgarlik, taktika.", "universitetlar": "Tennis akademiyalari"},
    "📦 Logistika Menejeri": {"emoji": "📦", "tavsif": "Logistika menejerlari yuk tashish va yetkazib berish jarayonlarini boshqaradi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy", "kelajak": "E-commerce o'sishi bilan talab oshmoqda.", "talablar": "Logistika ta'limi, ERP tizimlar.", "universitetlar": "TIQXMMI, ToshDTU"},
    "🔗 Supply Chain Specialist": {"emoji": "🔗", "tavsif": "Ta'minot zanjiri mutaxassislari xomashyodan mahsulotgacha jarayonni optimallashtiradi.", "maosh": "O'zbekistonda: $500-2500/oy | Xorijda: $4000-15000/oy", "kelajak": "Global ta'minot zanjirlari murakkablashishi bilan talab o'sdi.", "talablar": "CSCP sertifikati, ERP.", "universitetlar": "TIQXMMI + APICS"},
    "🚛 Transport Menejeri": {"emoji": "🚛", "tavsif": "Transport menejerlari transport parki va yuk tashish operatsiyalarini boshqaradi.", "maosh": "O'zbekistonda: $400-1800/oy | Xorijda: $3000-10000/oy", "kelajak": "Transport infratuzilmasi rivojlanishi bilan talab oshmoqda.", "talablar": "Transport qonunchiligi, fleet management.", "universitetlar": "ToshDTU"},
    "🌏 Import/Export Mutaxassisi": {"emoji": "🌏", "tavsif": "Import/eksport mutaxassislari xalqaro savdo operatsiyalarini boshqaradi.", "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy", "kelajak": "O'zbekiston eksporti kengaymoqda.", "talablar": "Xalqaro savdo qoidalari, Incoterms, til bilimlari.", "universitetlar": "TIQXMMI"},
    "✈️ Aviatsiya Logistika Mutaxassisi": {"emoji": "✈️", "tavsif": "Aviatsiya logistika mutaxassislari havo yo'li bilan yuk tashishni boshqaradi.", "maosh": "O'zbekistonda: $500-2500/oy | Xorijda: $4000-15000/oy", "kelajak": "O'zbekiston tranzit markaz bo'lmoqda.", "talablar": "Aviatsiya qoidalari, logistika, ingliz tili.", "universitetlar": "Aviatsiya akademiyasi"},
    "⚛️ Fizik": {"emoji": "⚛️", "tavsif": "Fiziklar tabiat qonunlarini o'rganadi, yangi texnologiyalar kashf etadi.", "maosh": "O'zbekistonda: $300-1200/oy | Xorijda: $4000-15000/oy", "kelajak": "Kvant hisoblash va nanotexnologiya rivojlanmoqda.", "talablar": "Fizika va matematika, PhD.", "universitetlar": "ToshDU fizika, O'zMU"},
    "🧪 Kimyogar": {"emoji": "🧪", "tavsif": "Kimyogarlar yangi moddalar va materiallarni kashf etadi.", "maosh": "O'zbekistonda: $300-1200/oy | Xorijda: $4000-14000/oy", "kelajak": "Farmatsevtika va yangi materiallar sanoatida talab bor.", "talablar": "Kimyo ta'limi, laboratoriya ko'nikmalari.", "universitetlar": "ToshDU"},
    "🌿 Biolog": {"emoji": "🌿", "tavsif": "Biologlar tirik organizmlarni o'rganadi.", "maosh": "O'zbekistonda: $300-1100/oy | Xorijda: $3500-12000/oy", "kelajak": "Biotexnologiya va biofarmatsevtika rivojlanmoqda.", "talablar": "Biologiya ta'limi, laboratoriya.", "universitetlar": "ToshDU biologiya"},
    "🔭 Astronom": {"emoji": "🔭", "tavsif": "Astronomlar yulduzlar, sayyoralar va koinotni o'rganadi.", "maosh": "O'zbekistonda: $300-1000/oy | Xorijda: $4000-15000/oy", "kelajak": "SpaceX va NASA kosmik tadqiqotlarni kengaytirmoqda.", "talablar": "Fizika va matematika, PhD.", "universitetlar": "ToshDU, O'zFA Astronomiya instituti"},
    "🔬 Tadqiqotchi": {"emoji": "🔬", "tavsif": "Tadqiqotchilar muayyan sohalarda yangi bilimlar kashf etadi.", "maosh": "O'zbekistonda: $300-1200/oy | Xorijda: $4000-15000/oy", "kelajak": "Ilmiy grantlar va xalqaro hamkorlik imkoniyatlari o'smoqda.", "talablar": "PhD darajasi, tadqiqot metodologiyasi.", "universitetlar": "Har qanday oliy ta'lim muassasasi"},
    "🐾 Veterinar": {"emoji": "🐾", "tavsif": "Veterinarlar hayvon kasalliklarini davolaydi.", "maosh": "O'zbekistonda: $300-1200/oy | Xorijda: $3000-10000/oy", "kelajak": "Chorvachilik sanoati o'sishi bilan talab oshmoqda.", "talablar": "Veterinariya ta'limi, hayvonlarni sevish.", "universitetlar": "SamQXI, ToshDQXI"},
    "🌾 Agronom": {"emoji": "🌾", "tavsif": "Agronomlar o'simlik yetishtirish va hosildorlikni oshirish bo'yicha mutaxassis.", "maosh": "O'zbekistonda: $300-1200/oy | Xorijda: $3000-10000/oy", "kelajak": "Smart farming agronom talabini oshirmoqda.", "talablar": "Agronomy ta'limi, tuproqshunoslik.", "universitetlar": "ToshDQXI, SamQXI"},
    "👨‍🌾 Fermer": {"emoji": "👨‍🌾", "tavsif": "Fermerlar qishloq xo'jaligi mahsulotlari yetishtirib, bozorga yetkazadi.", "maosh": "Cheksiz.", "kelajak": "Organik fermerchilik va agroturizm yangi imkoniyatlar bermoqda.", "talablar": "Agronomy bilimi, biznes tafakkuri.", "universitetlar": "QXI yoki amaliy tajriba"},
    "🌱 Agrotexnolog": {"emoji": "🌱", "tavsif": "Agrotexnologlar yangi texnologiyalar orqali qishloq xo'jaligi samaradorligini oshiradi.", "maosh": "O'zbekistonda: $400-1500/oy | Xorijda: $3000-12000/oy", "kelajak": "Dronlar, sensorlar va AI fermerchilikda keng qo'llanilmoqda.", "talablar": "Agronomy + IT bilimlari.", "universitetlar": "ToshDQXI"},
    "🐄 Zooinjener": {"emoji": "🐄", "tavsif": "Zooinjenerlar hayvon zotlarini yaxshilash va mahsuldorlikni oshiradi.", "maosh": "O'zbekistonda: $300-1200/oy", "kelajak": "Chorvachilik modernizatsiyasi bilan talab oshmoqda.", "talablar": "Zoologiya, genetika, hayvon fiziologiyasi.", "universitetlar": "ToshDQXI"},
    "🎖️ Harbiy Ofitser": {"emoji": "🎖️", "tavsif": "Harbiy ofitserlar qurolli kuchlarni boshqaradi, mamlakatni himoya qiladi.", "maosh": "O'zbekistonda: $400-1500/oy + imtiyozlar", "kelajak": "Barqaror davlat xizmati va ijtimoiy himoya.", "talablar": "Harbiy akademiya, jismoniy tayyorgarlik, liderlik.", "universitetlar": "O'zbekiston Harbiy akademiyasi"},
    "🔬 Kriminalist": {"emoji": "🔬", "tavsif": "Kriminalistlar jinoyat dalillarini ilmiy usullar bilan o'rganadi.", "maosh": "O'zbekistonda: $350-1200/oy | Xorijda: $3000-10000/oy", "kelajak": "DNA tahlili, raqamli kriminalistika yangi yo'nalishlar.", "talablar": "Kimyo, biologiya, huquqshunoslik.", "universitetlar": "ToshDYUI, IIV akademiyasi"},
    "💪 Maxsus Kuchlar Xodimi": {"emoji": "💪", "tavsif": "Maxsus kuchlar xodimlari murakkab vaziyatlarda harakat qiladigan elita harbiy guruhlar.", "maosh": "O'zbekistonda: $500-2000/oy + imtiyozlar", "kelajak": "Milliy xavfsizlik tizimida eng nufuzli lavozim.", "talablar": "Juda yuqori jismoniy va aqliy tayyorgarlik.", "universitetlar": "Harbiy akademiya"},
    "🕵️ Detektiv": {"emoji": "🕵️", "tavsif": "Detektivlar jinoyatlarni tekshiradi, dalil yig'adi.", "maosh": "O'zbekistonda: $350-1500/oy | Xorijda: $3000-10000/oy", "kelajak": "Kiber jinoyatlar va moliyaviy tergov yangi ixtisoslik.", "talablar": "Huquq, psixologiya, kuzatuv ko'nikmalari.", "universitetlar": "ToshDYUI, IIV akademiyasi"},
    "🛡️ Milliy Xavfsizlik Mutaxassisi": {"emoji": "🛡️", "tavsif": "Milliy xavfsizlik mutaxassislari davlat xavfsizligini ta'minlash uchun tahlil qiladi.", "maosh": "O'zbekistonda: $500-2000/oy + imtiyozlar", "kelajak": "Kiber xavfsizlik va razvedka sohalari rivojlanmoqda.", "talablar": "Huquq, xalqaro aloqalar, analitik fikrlash.", "universitetlar": "DXA, harbiy akademiyalar"},
}

# ============================================================
# STATES
# ============================================================
class Onboarding(StatesGroup):
    ism             = State()
    sinf            = State()
    ota_raqam       = State()
    yo_l_tanlash    = State()
    test_savol      = State()
    yonalish        = State()
    kasb_tanlash    = State()
    kasb_tasdiqlash = State()
    vaqt_tanlash    = State()

# ============================================================
# TEST SAVOLLARI
# ============================================================
TEST_SAVOLLAR = [
    {"savol": "🎮 Bo'sh vaqtingizda nima qilishni yaxshi ko'rasiz?", "javoblar": [("💻 Kompyuter/telefonda o'ynash yoki kod yozish", {"T": 3, "Me": 2}), ("🎨 Rasm chizish, dizayn qilish", {"D": 3, "S": 2}), ("📚 Kitob o'qish yoki yangi narsa o'rganish", {"Ta": 3, "I": 2}), ("⚽ Sport bilan shug'ullanish", {"Sp": 3, "Xa": 1})]},
    {"savol": "💡 Do'stlaringiz sizni qanday ta'riflaydi?", "javoblar": [("🧠 Aqlli va muammolarni yaxshi yechasiz", {"T": 2, "I": 2, "H": 1}), ("🗣 Gapirishni va ishontirishni yaxshi bilasiz", {"B": 3, "Ma": 2}), ("🎨 Ijodiy va original fikrlaysiz", {"D": 3, "S": 2, "Me": 2}), ("❤️ Mehribon, odamlarga yordam berishni yaxshi ko'rasiz", {"Ti": 3, "Ps": 3, "Ta": 2})]},
    {"savol": "🌍 Qaysi dunyo sizni hayajontiradi?", "javoblar": [("🚀 Texnologiya va kelajak — robotlar, AI, dasturlar", {"T": 3, "Mu": 2}), ("💰 Pul, biznes va muvaffaqiyat", {"B": 3, "M": 3}), ("🎭 San'at, musiqa, kino va ijodiyot", {"S": 3, "Me": 2, "D": 1}), ("🌿 Tabiat, fan va kashfiyotlar", {"I": 3, "Q": 2, "Ti": 1})]},
    {"savol": "🏆 Qaysi vazifani bajarishdan zavq olasiz?", "javoblar": [("🔧 Biror narsani tamir qilish yoki qurish", {"Mu": 3, "A": 2, "T": 1}), ("📊 Raqamlarni tahlil qilish va hisobot tuzish", {"M": 3, "Ma": 2, "B": 1}), ("🎤 Odamlar oldida gapirish yoki o'qitish", {"Ta": 3, "S": 2, "Ma": 1}), ("🔍 Muammoni topish va yechim izlash", {"H": 3, "Xa": 2, "I": 2})]},
    {"savol": "📱 Ijtimoiy tarmoqlarda ko'pincha nima ko'rasiz?", "javoblar": [("🎬 Video, musiqa va kontent", {"Me": 3, "S": 2}), ("📰 Yangiliklar, siyosat va jamiyat", {"X": 3, "H": 2, "Ma": 1}), ("💼 Biznes, startap va motivatsiya", {"B": 3, "Ma": 2}), ("🏋️ Sport, sayohat va sarguzashtlar", {"Sp": 3, "Tu": 3})]},
    {"savol": "🎯 10 yildan keyin o'zingizni qanday ko'rasiz?", "javoblar": [("👨‍💻 O'z IT kompaniyam bor, texnologiya sohasidaman", {"T": 3, "B": 2}), ("🏥 Odamlarga shifokor yoki psixolog sifatida yordam beraman", {"Ti": 3, "Ps": 3}), ("🎨 Mashhur ijodkor, dizayner yoki san'atkormаn", {"D": 3, "S": 3, "Me": 2}), ("⚖️ Jamiyatga xizmat qilaman — advokat, diplomat yoki harbiy", {"H": 3, "X": 2, "Xa": 2})]},
    {"savol": "🛠 Qaysi ko'nikma sizda eng kuchli?", "javoblar": [("🔢 Matematika va mantiqiy fikrlash", {"T": 3, "M": 3, "I": 2, "Mu": 2}), ("✍️ Yozish va til — insho, hikoya, tavsif", {"Me": 3, "Ma": 3, "H": 1}), ("👁 Ko'rish va estetika — chiroylini his qilaman", {"D": 3, "A": 2, "S": 2}), ("🤝 Odamlar bilan muloqot va ishontirish", {"B": 3, "Ps": 2, "Ta": 2, "X": 2})]},
    {"savol": "💼 Ish joyingiz qanday bo'lishini xohlaysiz?", "javoblar": [("🏠 Uydan ishlash, erkin jadval", {"T": 3, "Me": 2, "D": 2}), ("🏢 Katta ofis, jamoa va korporatsiya", {"B": 3, "M": 2, "L": 2}), ("🌍 Sayohat qilish, har joyda bo'lish", {"Tu": 3, "X": 3, "Sp": 1}), ("🔬 Laboratoriya, shifoxona yoki dala ishi", {"I": 3, "Ti": 3, "Q": 2})]},
    {"savol": "🚀 Qaysi loyihada ishlashni xohlardingiz?", "javoblar": [("🤖 AI robot yoki ilova yaratish", {"T": 3, "Mu": 2, "I": 1}), ("🏗 Bino yoki shahar loyihalash", {"A": 3, "Mu": 2}), ("📺 Film, musiqa yoki kontent yaratish", {"Me": 3, "S": 3, "D": 1}), ("🌾 Qishloq xo'jaligi yoki ekologiya loyihasi", {"Q": 3, "I": 2})]},
    {"savol": "⚡ Sizni eng ko'p nima motivatsiya qiladi?", "javoblar": [("💰 Ko'p pul ishlash va moliyaviy erkinlik", {"M": 3, "B": 3, "T": 1}), ("🌟 Mashhur bo'lish va e'tirof olish", {"S": 3, "Me": 3, "Sp": 2}), ("❤️ Odamlarga yordam berish va jamiyatni o'zgartirish", {"Ti": 3, "Ps": 3, "Ta": 2, "H": 2}), ("🧩 Murakkab muammolarni yechish va kashfiyot qilish", {"I": 3, "T": 2, "Mu": 2, "Xa": 2})]},
]

YONALISH_NATIJA = {
    "T":  ("💻 Texnologiya",        ["👨‍💻 Dasturchi", "🤖 AI Engineer", "📊 Data Analyst"]),
    "B":  ("💼 Biznes",             ["🚀 Startup Founder", "👔 CEO", "📦 Product Manager"]),
    "M":  ("💰 Moliya",             ["📈 Trader", "💹 Investor", "📊 Financial Analyst"]),
    "D":  ("🎨 Dizayn",             ["📱 UI/UX Dizayner", "🖼️ Grafik Dizayner", "🌐 Web Dizayner"]),
    "Me": ("🎥 Media",              ["📹 YouTuber", "🎞️ Video Editor", "✍️ Blogger"]),
    "S":  ("🎤 San'at",             ["🎤 Singer", "🎵 Musiqachi", "🎭 Aktyor"]),
    "A":  ("🏛️ Arxitektura",       ["🏛️ Arxitektor", "🛋️ Interyer Dizayner", "🏙️ Urban Planner"]),
    "Mu": ("⚙️ Muhandislik",       ["🤖 Robototexnika Muhandisi", "⚡ Elektr Muhandisi", "🔧 Mexanik Muhandis"]),
    "Ti": ("🏥 Tibbiyot",           ["👨‍⚕️ Shifokor", "🔪 Jarroh", "🦷 Stomatolog"]),
    "Ps": ("🧠 Psixologiya",        ["🧠 Psixolog", "🎯 Career Coach", "👥 HR Mutaxassisi"]),
    "Ta": ("📚 Ta'lim",             ["📚 O'qituvchi", "🧑‍🏫 Mentor", "💪 Trener"]),
    "H":  ("⚖️ Huquq",             ["⚖️ Advokat", "📜 Yurist", "🔍 Tergovchi"]),
    "Ma": ("📈 Marketing",          ["📱 SMM Manager", "💻 Digital Marketer", "✍️ Copywriter"]),
    "X":  ("🌍 Xalqaro Aloqalar",  ["🤝 Diplomat", "🗣️ Tarjimon", "🌐 Xalqaro Menejer"]),
    "Tu": ("✈️ Turizm",             ["🗺️ Tur Menejer", "✈️ Pilot", "📸 Travel Blogger"]),
    "Sp": ("⚽ Sport",              ["⚽ Futbolchi", "🥊 Bokschi", "🎾 Tennischi"]),
    "L":  ("🚚 Logistika",          ["📦 Logistika Menejeri", "🔗 Supply Chain Specialist", "🚛 Transport Menejeri"]),
    "I":  ("🔬 Ilm-fan",            ["🔬 Tadqiqotchi", "⚛️ Fizik", "🌿 Biolog"]),
    "Q":  ("🌾 Qishloq Xo'jaligi", ["🌾 Agronom", "🐾 Veterinar", "👨‍🌾 Fermer"]),
    "Xa": ("🛡️ Xavfsizlik",        ["🎖️ Harbiy Ofitser", "🕵️ Detektiv", "🔬 Kriminalist"]),
}

# ============================================================
# KEYBOARDS
# ============================================================
def obuna_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanalga o'tish", url="https://t.me/AI_Maqsad")],
        [InlineKeyboardButton(text="✅ Obuna bo'ldim", callback_data="check_sub")]
    ])

def sinf_kb():
    buttons = []
    row = []
    for sinf in ["5", "6", "7", "8", "9", "10", "11"]:
        row.append(InlineKeyboardButton(text=f"{sinf}-sinf", callback_data=f"sinf_{sinf}"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    # Orqaga tugmasi
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="orqaga_ism")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def yo_l_tanlash_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧠 Test orqali aniqlash (10 savol)", callback_data="yol_test")],
        [InlineKeyboardButton(text="🎯 O'zim tanlayaman", callback_data="yol_oz")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="orqaga_ota_raqam")],
    ])

def test_javob_kb(savol_idx, javoblar):
    buttons = []
    for i, (matn, _) in enumerate(javoblar):
        buttons.append([InlineKeyboardButton(text=matn, callback_data=f"t_{savol_idx}_{i}")])
    # 1-savolda orqaga = yo'l tanlashga, qolganida oldingi savolga
    if savol_idx == 0:
        buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="orqaga_yol_tanlash")])
    else:
        buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"test_orqaga_{savol_idx}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def kasb_tasdiqlash_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Shu kasbni tanlayman!", callback_data="kasb_tasdiqlash")],
        [InlineKeyboardButton(text="⬅️ Boshqa kasb", callback_data="kasb_orqaga")],
        [InlineKeyboardButton(text="🔄 Yo'nalishni o'zgartirish", callback_data="yonalish_orqaga")]
    ])

def vaqt_tanlash_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🌅 07:00", callback_data="vaqt_7"),
            InlineKeyboardButton(text="🌅 08:00", callback_data="vaqt_8"),
            InlineKeyboardButton(text="🌤 09:00", callback_data="vaqt_9"),
        ],
        [
            InlineKeyboardButton(text="☀️ 10:00", callback_data="vaqt_10"),
            InlineKeyboardButton(text="☀️ 11:00", callback_data="vaqt_11"),
            InlineKeyboardButton(text="🌞 12:00", callback_data="vaqt_12"),
        ],
        [
            InlineKeyboardButton(text="🌤 13:00", callback_data="vaqt_13"),
            InlineKeyboardButton(text="⛅ 14:00", callback_data="vaqt_14"),
            InlineKeyboardButton(text="⛅ 15:00", callback_data="vaqt_15"),
        ],
        [
            InlineKeyboardButton(text="🌆 16:00", callback_data="vaqt_16"),
            InlineKeyboardButton(text="🌆 17:00", callback_data="vaqt_17"),
            InlineKeyboardButton(text="🌇 18:00", callback_data="vaqt_18"),
        ],
        [
            InlineKeyboardButton(text="🌇 19:00", callback_data="vaqt_19"),
            InlineKeyboardButton(text="🌃 20:00", callback_data="vaqt_20"),
            InlineKeyboardButton(text="🌙 21:00", callback_data="vaqt_21"),
        ],
        [
            InlineKeyboardButton(text="🌙 22:00", callback_data="vaqt_22"),
        ],
    ])

# ============================================================
# HELPER FUNKSIYALAR
# ============================================================
async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status not in ["left", "kicked"]
    except:
        return False

async def _keyin_raqam(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("✅ Raqam saqlandi!", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(0.5)
    await message.answer(
        f"<b>{data['ism']}</b>, endi eng qiziqarli qism! 🎯\n\n"
        f"Kasbingizni qanday tanlaysiz?",
        parse_mode="HTML",
        reply_markup=yo_l_tanlash_kb()
    )
    await state.set_state(Onboarding.yo_l_tanlash)

# ============================================================
# HANDLERS
# ============================================================
@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await message.answer("🌟", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(0.5)
    await message.answer(
        "Salom! Men <b>CareerUp</b> — sizning shaxsiy karyera yo'riqnomangiz! 🚀\n\n"
        "Men sizga <b>12 oyda professional</b> bo'lishingizga yordam beraman.\n\n"
        "Faqat <b>3 daqiqa</b> — va sizning yo'l xaritangiz tayyor! ⚡",
        parse_mode="HTML"
    )
    await asyncio.sleep(0.8)
    await message.answer(
        "Avval tanishamiz 👋\n\n<b>Ismingiz nima?</b>",
        parse_mode="HTML"
    )
    await state.set_state(Onboarding.ism)



# --- ISM ---
@router.message(Onboarding.ism)
async def get_ism(message: Message, state: FSMContext):
    ism = message.text.strip()
    if len(ism) < 2 or len(ism) > 50:
        await message.answer("❌ Iltimos, to'liq ismingizni yozing:")
        return
    await state.update_data(ism=ism)
    await message.answer(
        f"Zo'r ism, <b>{ism}</b>! 👏\n\n📚 <b>Nechi-sinfda o'qiysiz?</b>",
        parse_mode="HTML",
        reply_markup=sinf_kb()
    )
    await state.set_state(Onboarding.sinf)

# Sinf → orqaga = ismga qaytish
@router.callback_query(F.data == "orqaga_ism")
async def orqaga_ism(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        "✏️ <b>Ismingizni qaytadan kiriting:</b>",
        parse_mode="HTML"
    )
    await state.set_state(Onboarding.ism)

# --- SINF ---
@router.callback_query(F.data.startswith("sinf_"), Onboarding.sinf)
async def get_sinf(call: CallbackQuery, state: FSMContext):
    sinf = call.data.replace("sinf_", "")
    await state.update_data(sinf=sinf)
    await call.message.delete()
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni ulashish", request_contact=True)]],
        resize_keyboard=True
    )
    await call.message.answer(
        f"✅ <b>{sinf}-sinf</b>!\n\n"
        f"📱 <b>Ota-onangizning telefon raqami:</b>\n\n"
        f"• Progressingizni haftalik ko'radi 📊\n"
        f"• Yutuqlaringizdan xabar topadi 🏆\n"
        f"• Sertifikat oladi 🎓\n\n"
        f"Tugmani bosing yoki qo'lda kiriting (+998XXXXXXXXX):",
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await state.set_state(Onboarding.ota_raqam)

# Ota-ona raqami → orqaga = sinfga qaytish
@router.callback_query(F.data == "orqaga_ota_raqam")
async def orqaga_ota_raqam(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        "📚 <b>Nechi-sinfda o'qiysiz?</b>",
        parse_mode="HTML",
        reply_markup=sinf_kb()
    )
    await state.set_state(Onboarding.sinf)

# --- OTA-ONA RAQAMI ---
@router.message(Onboarding.ota_raqam, F.contact)
async def get_raqam_contact(message: Message, state: FSMContext):
    raqam = message.contact.phone_number
    if not raqam.startswith("+"): raqam = "+" + raqam
    await state.update_data(ota_raqam=raqam)
    await _keyin_raqam(message, state)

@router.message(Onboarding.ota_raqam, F.text)
async def get_raqam_text(message: Message, state: FSMContext):
    raqam = message.text.strip()
    if not re.match(r'^\+998\d{9}$', raqam):
        await message.answer(
            "❌ Raqam noto'g'ri!\nTo'g'ri format: <code>+998901234567</code>\nQaytadan kiriting:",
            parse_mode="HTML"
        )
        return
    await state.update_data(ota_raqam=raqam)
    await _keyin_raqam(message, state)

# --- YO'L TANLASH ---
@router.callback_query(F.data == "yol_test", Onboarding.yo_l_tanlash)
async def yol_test(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(ball={}, savol_idx=0)
    await call.message.answer(
        "🧠 <b>Kasb aniqlash testi</b>\n\n"
        "10 ta savol — har biri 4 variant.\n"
        "Eng mos javobni tanlang! ⏱ ~2 daqiqa",
        parse_mode="HTML"
    )
    await asyncio.sleep(0.8)
    savol = TEST_SAVOLLAR[0]
    await call.message.answer(
        f"<b>1/10</b> ⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪\n\n❓ {savol['savol']}",
        parse_mode="HTML",
        reply_markup=test_javob_kb(0, savol["javoblar"])
    )
    await state.set_state(Onboarding.test_savol)

@router.callback_query(F.data == "yol_oz")
async def yol_oz(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        "🎯 <b>Yo'nalishni tanlang:</b>",
        parse_mode="HTML",
        reply_markup=yonalish_keyboard()
    )
    await state.set_state(Onboarding.yonalish)

# Yo'l tanlash → orqaga = ota-ona raqamiga
@router.callback_query(F.data == "orqaga_yol_tanlash")
async def orqaga_yol_tanlash(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni ulashish", request_contact=True)]],
        resize_keyboard=True
    )
    await call.message.answer(
        "📱 <b>Ota-onangizning telefon raqami:</b>\n\nTugmani bosing yoki qo'lda kiriting:",
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await state.set_state(Onboarding.ota_raqam)

# --- TEST SAVOLLARI ---
@router.callback_query(F.data.startswith("t_"), Onboarding.test_savol)
async def test_javob(call: CallbackQuery, state: FSMContext):
    parts = call.data.split("_")
    savol_idx = int(parts[1])
    javob_idx = int(parts[2])
    data = await state.get_data()
    ball = data.get("ball", {})
    # Javob balllarini qo'shish
    _, balllar = TEST_SAVOLLAR[savol_idx]["javoblar"][javob_idx]
    for kod, qiymat in balllar.items():
        ball[kod] = ball.get(kod, 0) + qiymat
    # Javob tarixini saqlash
    tarix = data.get("javob_tarix", [])
    tarix.append({"savol": savol_idx, "javob": javob_idx, "ball_qoshildi": balllar})
    keyingi = savol_idx + 1
    await state.update_data(ball=ball, javob_tarix=tarix)
    await call.message.delete()
    progress = "🟢" * keyingi + "⚪" * (10 - keyingi)
    if keyingi < len(TEST_SAVOLLAR):
        savol = TEST_SAVOLLAR[keyingi]
        await call.message.answer(
            f"<b>{keyingi + 1}/10</b> {progress}\n\n❓ {savol['savol']}",
            parse_mode="HTML",
            reply_markup=test_javob_kb(keyingi, savol["javoblar"])
        )
    else:
        await call.message.answer("⏳ Tahlil qilinmoqda...")
        await asyncio.sleep(1.5)
        await test_natija_korsatish(call, state, ball)

# Test → orqaga (oldingi savolga)
@router.callback_query(F.data.startswith("test_orqaga_"), Onboarding.test_savol)
async def test_orqaga(call: CallbackQuery, state: FSMContext):
    joriy_idx = int(call.data.replace("test_orqaga_", ""))
    oldingi_idx = joriy_idx - 1
    data = await state.get_data()
    ball = data.get("ball", {})
    tarix = data.get("javob_tarix", [])
    # Oxirgi javob balllarini olib tashlash
    if tarix:
        oxirgi = tarix.pop()
        for kod, qiymat in oxirgi["ball_qoshildi"].items():
            ball[kod] = ball.get(kod, 0) - qiymat
            if ball[kod] <= 0:
                ball.pop(kod, None)
    await state.update_data(ball=ball, javob_tarix=tarix)
    await call.message.delete()
    progress = "🟢" * oldingi_idx + "⚪" * (10 - oldingi_idx)
    savol = TEST_SAVOLLAR[oldingi_idx]
    await call.message.answer(
        f"<b>{oldingi_idx + 1}/10</b> {progress}\n\n❓ {savol['savol']}",
        parse_mode="HTML",
        reply_markup=test_javob_kb(oldingi_idx, savol["javoblar"])
    )

async def test_natija_korsatish(call, state, ball):
    eng_yaxshi = max(ball, key=ball.get) if ball else "T"
    yonalish_nomi, kasblar = YONALISH_NATIJA.get(
        eng_yaxshi, ("💻 Texnologiya", ["👨‍💻 Dasturchi", "🤖 AI Engineer", "📊 Data Analyst"])
    )
    saralangan = sorted(ball.items(), key=lambda x: x[1], reverse=True)
    ikkinchi = YONALISH_NATIJA.get(saralangan[1][0], ("", []))[0] if len(saralangan) > 1 else ""
    uchinchi  = YONALISH_NATIJA.get(saralangan[2][0], ("", []))[0] if len(saralangan) > 2 else ""
    await state.update_data(yonalish=yonalish_nomi)
    xabar = (
        f"🎯 <b>Test natijasi!</b>\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🥇 <b>Asosiy yo'nalish:</b> {yonalish_nomi}\n"
    )
    if ikkinchi: xabar += f"🥈 <b>Qo'shimcha:</b> {ikkinchi}\n"
    if uchinchi: xabar += f"🥉 <b>Alternativ:</b> {uchinchi}\n"
    xabar += f"━━━━━━━━━━━━━━━\n\n<b>Sizga mos kasblar:</b>\n\n"
    for i, kasb in enumerate(kasblar, 1):
        xabar += f"  {i}. {kasb}\n"
    xabar += "\n<i>Qaysi kasb siz uchun?</i> 👇"
    await call.message.answer(xabar, parse_mode="HTML", reply_markup=kasb_keyboard(yonalish_nomi))
    await state.set_state(Onboarding.kasb_tanlash)

# --- O'ZI TANLASH ---
@router.message(Onboarding.yonalish)
async def get_yonalish(message: Message, state: FSMContext):
    await state.update_data(yonalish=message.text)
    await message.answer(
        f"Ajoyib tanlov! {message.text} 👏\n\nKasbingizni tanlang 👇",
        reply_markup=kasb_keyboard(message.text)
    )
    await state.set_state(Onboarding.kasb_tanlash)

# --- KASB TANLASH ---
@router.message(Onboarding.kasb_tanlash)
async def get_kasb(message: Message, state: FSMContext):
    kasb_nomi = message.text
    malumot = KASB_MALUMOTLARI.get(kasb_nomi)
    if not malumot:
        await message.answer("❌ Iltimos, ro'yxatdan kasb tanlang!")
        return
    await state.update_data(kasb=kasb_nomi)
    matn = (
        f"{malumot['emoji']} <b>{kasb_nomi}</b>\n\n"
        f"📋 <b>Nima qiladi:</b>\n{malumot['tavsif']}\n\n"
        f"💰 <b>Maosh:</b>\n{malumot['maosh']}\n\n"
        f"🚀 <b>Kelajak:</b>\n{malumot['kelajak']}\n\n"
        f"📚 <b>Nima o'rganish kerak:</b>\n{malumot['talablar']}\n\n"
        f"🏫 <b>Universitetlar:</b>\n{malumot['universitetlar']}\n\n"
        f"Bu kasb sizga yoqdimi?"
    )
    await message.answer(matn, reply_markup=kasb_tasdiqlash_keyboard(), parse_mode="HTML")
    await state.set_state(Onboarding.kasb_tasdiqlash)

# --- KASB TASDIQLASH ---
@router.callback_query(F.data == "kasb_tasdiqlash", Onboarding.kasb_tasdiqlash)
async def kasb_tasdiqlash_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.delete()
    await call.message.answer("⚡ Saqlanmoqda...")
    await asyncio.sleep(1)
    await call.message.answer(
        f"🎉 <b>TABRIKLAYMIZ, {data['ism'].upper()}!</b>\n\n"
        f"Siz rasmiy ravishda <b>CareerUp</b> ga qo'shildingiz! 🚀",
        parse_mode="HTML"
    )
    await asyncio.sleep(1.2)
    await call.message.answer(
        f"🗺 <b>Sizning 12 oylik yo'l xaritangiz:</b>\n\n"
        f"👤 <b>Kim:</b> {data['ism']}, {data['sinf']}-sinf\n"
        f"💼 <b>Maqsad:</b> {data['kasb']}\n"
        f"🎯 <b>Yo'nalish:</b> {data['yonalish']}\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🟢 1-2 oy → Asoslar (BEPUL)\n"
        f"🔵 3-6 oy → Amaliyot\n"
        f"🟣 7-12 oy → Professional daraja\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"⚡ Jami: <b>360 ta vazifa</b> — har kuni 1 ta!",
        parse_mode="HTML"
    )
    await asyncio.sleep(1.5)
    await call.message.answer(
        f"🏆 <b>Tizim qanday ishlaydi?</b>\n\n"
        f"✅ Vazifa bajaring → <b>XP yig'ing</b>\n"
        f"🔥 Har kun bajaring → <b>Streak kuchayadi</b>\n"
        f"🏅 XP to'plang → <b>Ligani oshiring</b>\n\n"
        f"🥉 Bronza → 🥈 Kumush → 🥇 Oltin → 💎 Olmos",
        parse_mode="HTML"
    )
    await asyncio.sleep(1.5)
    await call.message.answer(
        f"⏰ <b>Vazifa qaysi vaqtda kelsin?</b>\n\n"
        f"Har kuni shu vaqtda yangi vazifa yuboriladi 👇",
        parse_mode="HTML",
        reply_markup=vaqt_tanlash_kb()
    )
    await state.set_state(Onboarding.vaqt_tanlash)

# Kasb orqaga
@router.callback_query(F.data == "kasb_orqaga", Onboarding.kasb_tasdiqlash)
async def kasb_orqaga_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.delete()
    await call.message.answer("Boshqa kasb tanlang 👇", reply_markup=kasb_keyboard(data["yonalish"]))
    await state.set_state(Onboarding.kasb_tanlash)

# Yo'nalish orqaga
@router.callback_query(F.data == "yonalish_orqaga", Onboarding.kasb_tasdiqlash)
async def yonalish_orqaga_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Yo'nalishni qaytadan tanlang 👇", reply_markup=yonalish_keyboard())
    await state.set_state(Onboarding.yonalish)

# --- VAQT TANLASH ---
@router.callback_query(F.data.startswith("vaqt_"), Onboarding.vaqt_tanlash)
async def vaqt_tanlash_handler(call: CallbackQuery, state: FSMContext):
    vaqt = int(call.data.replace("vaqt_", ""))
    data = await state.get_data()
    await save_user(
        telegram_id=call.from_user.id,
        ism=data["ism"],
        sinf=data["sinf"],
        ota_raqam=data["ota_raqam"],
        yonalish=data["yonalish"],
        kasb=data["kasb"],
        vazifa_vaqti=vaqt
    )
    await call.message.delete()
    await call.message.answer(
        f"✅ <b>Ajoyib!</b>\n\n"
        f"Har kuni soat <b>{vaqt:02d}:00</b> da vazifa keladi! ⏰\n\n"
        f"Tayyor bo'ling, <b>{data['ism']}</b>! 💪🔥",
        parse_mode="HTML"
    )
    await state.clear()
