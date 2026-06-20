from aiogram import Router, Bot, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
import re

from db import save_user
from menus import yonalish_keyboard, kasb_keyboard

router = Router()

CHANNEL_ID = "@AI_Maqsad"
INSTAGRAM = "instagram.com/maqsadai"

# Kasb ma'lumotlari
KASB_MALUMOTLARI = {
    # TEXNOLOGIYA
    "👨‍💻 Dasturchi": {
        "emoji": "👨‍💻",
        "tavsif": "Dasturchilar kompyuter dasturlari, ilovalar va veb saytlar yaratadi.",
        "maosh": "O'zbekistonda: $500-3000/oy | Xorijda: $3000-15000/oy",
        "kelajak": "IT sohasi tez rivojlanmoqda. Sun'iy intellekt, mobil ilovalar va cloud texnologiyalar bo'yicha talab katta!",
        "talablar": "Python, JavaScript, SQL bilimi. Ingliz tili muhim.",
        "universitetlar": "TATU, INHA, Webster, Turin Polytechnic"
    },
    "🤖 AI Engineer": {
        "emoji": "🤖",
        "tavsif": "AI muhandislari sun'iy intellekt tizimlarini loyihalaydi va amalga oshiradi.",
        "maosh": "O'zbekistonda: $800-4000/oy | Xorijda: $5000-20000/oy",
        "kelajak": "Dunyodagi eng istiqbolli kasb! ChatGPT, robotlar, tibbiyot AI — hamma sohada kerak.",
        "talablar": "Python, matematika, Machine Learning. Master daraja tavsiya etiladi.",
        "universitetlar": "TATU, MIT (xorij), Stanford (xorij)"
    },
    "🔐 Cybersecurity Specialist": {
        "emoji": "🔐",
        "tavsif": "Kiberjamiyat mutaxassislari kompaniyalar va davlatni xaker hujumlaridan himoya qiladi.",
        "maosh": "O'zbekistonda: $600-2500/oy | Xorijda: $4000-18000/oy",
        "kelajak": "Raqamli dunyoda xavfsizlik talab katta. Bank, davlat, IT kompaniyalar uchun zarur.",
        "talablar": "Network, Linux, kriptografiya bilimi. CEH, CISSP sertifikatlari.",
        "universitetlar": "TATU, Milliy gvardiya akademiyasi"
    },
    "📊 Data Analyst": {
        "emoji": "📊",
        "tavsif": "Ma'lumotlar tahlilchilari katta hajmdagi ma'lumotlardan foydali xulosalar chiqaradi.",
        "maosh": "O'zbekistonda: $500-2000/oy | Xorijda: $3500-12000/oy",
        "kelajak": "Har bir kompaniya ma'lumotlar asosida qaror qabul qilmoqda. Talab juda yuqori!",
        "talablar": "Excel, SQL, Python, Tableau. Statistika bilimi muhim.",
        "universitetlar": "TATU, ToshDU, INHA"
    },
    "🎮 Game Developer": {
        "emoji": "🎮",
        "tavsif": "O'yin dasturchilar kompyuter va mobil o'yinlar yaratadi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy",
        "kelajak": "O'yin sanoati yiliga $200 milliarddan ortiq. Metaverse va VR o'yinlari kelajagi porloq!",
        "talablar": "Unity yoki Unreal Engine, C# yoki C++, 3D modellashtirish.",
        "universitetlar": "TATU, xususiy kurslar"
    },
    # BIZNES
    "🚀 Startup Founder": {
        "emoji": "🚀",
        "tavsif": "Startap asoschilari yangi biznes g'oyalarini hayotga tadbiq etadi va jamoani boshqaradi.",
        "maosh": "Cheksiz! Muvaffaqiyatli startap milliard dollarga baholanishi mumkin.",
        "kelajak": "O'zbekistonda startap ekotizimi rivojlanmoqda. IT Park, Astrum kabi markazlar qo'llab-quvvatlaydi.",
        "talablar": "Biznes tafakkuri, liderlik, muammo hal qilish, chidamlilik.",
        "universitetlar": "Westminster, Turin, INHA + akseleratorlar"
    },
    "👔 CEO": {
        "emoji": "👔",
        "tavsif": "Bosh ijrochi direktor kompaniyani boshqaradi, strategiya belgilaydi va natijalar uchun javob beradi.",
        "maosh": "O'zbekistonda: $2000-20000/oy | Xorijda: cheksiz",
        "kelajak": "Har doim kerak. Yaxshi rahbarlar kamyob va qimmatbaho!",
        "talablar": "MBA darajasi, liderlik, moliya, marketing bilimlari.",
        "universitetlar": "Westminster MBA, TIQXMMI, Harvard Business School (xorij)"
    },
    "📦 Product Manager": {
        "emoji": "📦",
        "tavsif": "Mahsulot menejeri IT mahsulotning strategiyasini belgilaydi va jamoani yo'naltiradi.",
        "maosh": "O'zbekistonda: $800-3000/oy | Xorijda: $5000-20000/oy",
        "kelajak": "IT kompaniyalarning eng talab qilinadigan kasbi. Google, Meta, Amazon doimiy qidiradi!",
        "talablar": "IT va biznes bilimlari, analitik fikrlash, kommunikatsiya.",
        "universitetlar": "INHA, Westminster + online kurslar (Coursera)"
    },
    "📋 Project Manager": {
        "emoji": "📋",
        "tavsif": "Loyiha menejeri loyihalarni boshidan oxirigacha boshqaradi — vaqt, byudjet, jamoa.",
        "maosh": "O'zbekistonda: $600-2500/oy | Xorijda: $4000-15000/oy",
        "kelajak": "Barcha sohalarda kerak: IT, qurilish, tibbiyot, davlat sektori.",
        "talablar": "PMP sertifikati, Agile/Scrum bilimlari, liderlik.",
        "universitetlar": "Har qanday universitet + PMP sertifikat"
    },
    "💡 Biznes Konsultant": {
        "emoji": "💡",
        "tavsif": "Biznes konsultantlar kompaniyalarga muammolarini aniqlash va yechim topishda yordam beradi.",
        "maosh": "O'zbekistonda: $500-3000/oy | Xorijda: $3000-15000/oy",
        "kelajak": "McKinsey, BCG kabi konsalting firmalari eng yuqori maosh to'laydi!",
        "talablar": "Tahliliy fikrlash, biznes bilimlari, prezentatsiya ko'nikmalari.",
        "universitetlar": "Westminster, TIQXMMI, Turin"
    },
    # MOLIYA
    "📈 Trader": {
        "emoji": "📈",
        "tavsif": "Treyderlar fond bozori, valyuta yoki kripto bozorlarida savdo qilib daromad oladi.",
        "maosh": "Cheksiz — o'z kapitalingizdan foiz.",
        "kelajak": "Raqamli moliya va kripto bozorlar kengaymoqda. Malakali treyderlar kamyob.",
        "talablar": "Texnik tahlil, moliya bilimlari, psixologik barqarorlik.",
        "universitetlar": "ToshDU iqtisodiyot + o'z-o'zini o'qitish"
    },
    "💹 Investor": {
        "emoji": "💹",
        "tavsif": "Investorlar kompaniyalar yoki loyihalarga pul tikib, daromad oladi.",
        "maosh": "Cheksiz — investitsiyadan 10-30% yillik daromad.",
        "kelajak": "O'zbekiston investitsiya muhiti yaxshilanmoqda. Angel investor va VC fondlari o'smoqda.",
        "talablar": "Moliya tahlili, risk baholash, tarmoq (network).",
        "universitetlar": "ToshDU, Westminster + CFA sertifikati"
    },
    "📊 Financial Analyst": {
        "emoji": "📊",
        "tavsif": "Moliyaviy tahlilchilar kompaniyalar va investitsiyalarni baholab, tavsiyalar beradi.",
        "maosh": "O'zbekistonda: $600-2500/oy | Xorijda: $4000-15000/oy",
        "kelajak": "Bank, moliya kompaniyalari, investitsiya fondlari uchun zarur.",
        "talablar": "Excel, moliya modellashtirish, CFA sertifikati.",
        "universitetlar": "ToshDU, Westminster, TIQXMMI"
    },
    "🧾 Accountant": {
        "emoji": "🧾",
        "tavsif": "Buxgalterlar moliyaviy hisobotlarni yuritadi va soliq masalalarini hal qiladi.",
        "maosh": "O'zbekistonda: $400-1500/oy | Xorijda: $3000-8000/oy",
        "kelajak": "Har bir tashkilotga kerak. ACCA sertifikati xalqaro ish eshiklarini ochadi!",
        "talablar": "1C, soliq qonunchiligi, ACCA sertifikati.",
        "universitetlar": "ToshDU, TIQXMMI, moliya universiteti"
    },
    "🏦 Bankir": {
        "emoji": "🏦",
        "tavsif": "Bankirlar kredit berish, omonat qabul qilish va moliyaviy xizmatlarni boshqaradi.",
        "maosh": "O'zbekistonda: $500-3000/oy | Xorijda: $3000-20000/oy",
        "kelajak": "Raqamli bank (Neobank) va fintech rivojlanishi yangi imkoniyatlar yaratmoqda.",
        "talablar": "Moliya bilimlari, kommunikatsiya, CFA/MBA.",
        "universitetlar": "ToshDU, Moliya instituti, Westminster"
    },
    # DIZAYN
    "🖼️ Grafik Dizayner": {
        "emoji": "🖼️",
        "tavsif": "Grafik dizaynerlar logo, broshyura, reklama va vizual materiallar yaratadi.",
        "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $2000-8000/oy",
        "kelajak": "Har bir biznesga kerak. Freelance orqali xorijiy mijozlar bilan ishlash mumkin.",
        "talablar": "Adobe Photoshop, Illustrator, Figma, ijodkorlik.",
        "universitetlar": "Kamolot, San'at akademiyasi + Canva/Adobe kurslari"
    },
    "📱 UI/UX Dizayner": {
        "emoji": "📱",
        "tavsif": "UI/UX dizaynerlar ilova va veb saytlarning foydalanuvchilar uchun qulay bo'lishini ta'minlaydi.",
        "maosh": "O'zbekistonda: $500-2500/oy | Xorijda: $4000-15000/oy",
        "kelajak": "IT kompaniyalar uchun eng zarur mutaxassis. Figma, Sketch asoschi bo'ladi.",
        "talablar": "Figma, Adobe XD, foydalanuvchi psixologiyasi, prototiplash.",
        "universitetlar": "TATU, Amaliy san'at + Coursera kurslar"
    },
    "🎬 Motion Dizayner": {
        "emoji": "🎬",
        "tavsif": "Motion dizaynerlar animatsiya, video effektlar va harakatdagi grafikalar yaratadi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy",
        "kelajak": "Video kontent o'sishi bilan motion dizayn talab yuqori. OTT platformalar ko'p foydalanadi.",
        "talablar": "After Effects, Cinema 4D, Premiere Pro.",
        "universitetlar": "San'at akademiyasi + YouTube o'z-o'zini o'qitish"
    },
    "🗿 3D Artist": {
        "emoji": "🗿",
        "tavsif": "3D artistlar uch o'lchamli modellar, animatsiyalar va vizualizatsiyalar yaratadi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-15000/oy",
        "kelajak": "O'yin, kino, arxitektura vizualizatsiyasi va metaverse uchun katta talab.",
        "talablar": "Blender, Maya, 3ds Max, ijodkorlik.",
        "universitetlar": "San'at akademiyasi + online kurslar"
    },
    "🌐 Web Dizayner": {
        "emoji": "🌐",
        "tavsif": "Veb dizaynerlar chiroyli va qulay veb saytlar dizaynini yaratadi.",
        "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $2500-10000/oy",
        "kelajak": "Hamma biznes veb sayt kerakligi uchun talab kamaymasligi mumkin. Freelance yaxshi ishlaydi.",
        "talablar": "Figma, HTML/CSS asoslari, UX tushunchasi.",
        "universitetlar": "TATU + online kurslar"
    },
    # MEDIA
    "📹 YouTuber": {
        "emoji": "📹",
        "tavsif": "YouTuberlar video kontent yaratib, auditoriya to'playdi va reklama orqali pul ishlaydi.",
        "maosh": "Cheksiz — 100 ming obunachidan $1000-10000/oy",
        "kelajak": "Video kontent iste'moli yildan yilga o'sib bormoqda. Niche kontentlar alohida daromad beradi.",
        "talablar": "Kamera ko'nikmalari, montaj, ijodkorlik, doimiylik.",
        "universitetlar": "Maxsus ta'lim shart emas — amaliyot muhim"
    },
    "✍️ Blogger": {
        "emoji": "✍️",
        "tavsif": "Bloggerlar matn, foto yoki video orqali kontent yaratib, hamjamiyat shakllantiradi.",
        "maosh": "Cheksiz — hamkorlik va reklama orqali",
        "kelalak": "Personal brend va influencer marketing o'sib bormoqda.",
        "talablar": "Yozish ko'nikmalari, ijodkorlik, ijtimoiy tarmoq strategiyasi.",
        "universitetlar": "Maxsus ta'lim shart emas"
    },
    "🎞️ Video Editor": {
        "emoji": "🎞️",
        "tavsif": "Video montajchilar xom video materiallarni professional ko'rinishga keltiradi.",
        "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $2000-8000/oy",
        "kelajak": "Har bir media, reklama va ijtimoiy tarmoq kompaniyasiga kerak.",
        "talablar": "Premiere Pro, After Effects, CapCut, estetik his.",
        "universitetlar": "San'at akademiyasi + online kurslar"
    },
    "🎮 Streamer": {
        "emoji": "🎮",
        "tavsif": "Streamerlar o'yin yoki boshqa kontentni jonli efirda ko'rsatib, auditoriya to'playdi.",
        "maosh": "Cheksiz — donatsiya, subscribe va sponsorlar orqali",
        "kelajak": "Esport va streaming sanoati tez rivojlanmoqda.",
        "talablar": "Xarizmatik shaxsiyat, o'yin mahorati, OBS, kamera.",
        "universitetlar": "Maxsus ta'lim shart emas"
    },
    "📰 Jurnalist": {
        "emoji": "📰",
        "tavsif": "Jurnalistlar yangilik yig'ib, tahlil qilib, jamoatchilika yetkazadi.",
        "maosh": "O'zbekistonda: $300-1200/oy | Xorijda: $2000-8000/oy",
        "kelajak": "Raqamli jurnalistika va media startaplar yangi imkoniyatlar ochmoqda.",
        "talablar": "Yozish ko'nikmalari, intervyu olish, ob'ektivlik, til bilimlari.",
        "universitetlar": "O'zMU jurnalistika, ToshDU"
    },
    # SAN'AT
    "🎤 Singer": {
        "emoji": "🎤",
        "tavsif": "Qo'shiqchilar konsert, studiya yozuvi va ijro orqali o'z san'atini namoyish etadi.",
        "maosh": "Cheksiz — konsert, royalty va hamkorlik orqali",
        "kelajak": "Musiqa sanoati o'smoqda. Streaming platformalar yangi imkoniyat.",
        "talablar": "Vokal mahorati, sahna tajribasi, musiqa nazariyasi.",
        "universitetlar": "Davlat konservatoriyasi, O'zbekiston san'at instituti"
    },
    "🎭 Aktyor": {
        "emoji": "🎭",
        "tavsif": "Aktyorlar teatr, kino va televizion loyihalarda rol o'ynaydi.",
        "maosh": "O'zbekistonda: $300-5000/loyiha | Xorijda: cheksiz",
        "kelajak": "O'zbek kinosi va seriallar sanoati rivojlanmoqda.",
        "talablar": "Aktyorlik ko'nikmalari, plastika, nutq, sahna tajribasi.",
        "universitetlar": "Davlat san'at instituti, teatr akademiyasi"
    },
    "🎵 Musiqachi": {
        "emoji": "🎵",
        "tavsif": "Musiqachilar cholg'u asbob chaladi, kuy bichadi va musiqa loyihalarida ishtirok etadi.",
        "maosh": "Cheksiz — konsert, o'qitish, studiya ishlari orqali",
        "kelajak": "Musiqa ta'limi va professional musiqa sanoati o'smoqda.",
        "talablar": "Cholg'u asbob mahorati, nota bilimi, ijodkorlik.",
        "universitetlar": "Davlat konservatoriyasi, musiqa maktablari"
    },
    "🎧 DJ": {
        "emoji": "🎧",
        "tavsif": "DJ-lar musiqa mikslab, konsert va tadbirlarda tomoshabinlarga his-hayajon beradi.",
        "maosh": "O'zbekistonda: $200-2000/tadbir | Xorijda: cheksiz",
        "kelajak": "Klub, to'y va festival sanoati katta. Xalqaro festival budjetlari ulkan.",
        "talablar": "Musiqa hisi, DJ jihozlari, mikslash texnikasi.",
        "universitetlar": "Maxsus ta'lim shart emas — amaliyot muhim"
    },
    "🎬 Rejissyor": {
        "emoji": "🎬",
        "tavsif": "Rejissyorlar film, serial yoki teatr spektaklini sahna ortidan boshqaradi.",
        "maosh": "O'zbekistonda: $500-10000/loyiha | Xorijda: cheksiz",
        "kelajak": "O'zbek kinosi rivojlanmoqda. OTT platformalar (Netflix, YouTube) imkoniyat bermoqda.",
        "talablar": "Rejissyorlik mahorati, skript tahlili, jamoaviy ishlash.",
        "universitetlar": "Davlat san'at instituti, kino akademiyalari"
    },
    # ARXITEKTURA
    "🏛️ Arxitektor": {
        "emoji": "🏛️",
        "tavsif": "Arxitektorlar binolar va inshootlar loyihasini yaratadi, qurilishni nazorat qiladi.",
        "maosh": "O'zbekistonda: $500-3000/oy | Xorijda: $4000-15000/oy",
        "kelajak": "O'zbekistonda qurilish sanoati tez rivojlanmoqda. Toshkent shaharsozlik loyihalari ko'p.",
        "talablar": "AutoCAD, ArchiCAD, Revit, ijodkorlik, rasm chizish.",
        "universitetlar": "ToshDTU, TIQXMMI arxitektura, Milan Politexnika (xorij)"
    },
    "🛋️ Interyer Dizayner": {
        "emoji": "🛋️",
        "tavsif": "Interyer dizaynerlar xona va binolarning ichki ko'rinishini chiroyli va qulay qiladi.",
        "maosh": "O'zbekistonda: $400-2500/oy | Xorijda: $3000-12000/oy",
        "kelajak": "Ko'chmas mulk bozori o'sishi bilan interyer dizayn talab yuqori.",
        "talablar": "AutoCAD, 3ds Max, ijodkorlik, rang nazariyasi.",
        "universitetlar": "ToshDTU, San'at instituti, xususiy kurslar"
    },
    "🏙️ Urban Planner": {
        "emoji": "🏙️",
        "tavsif": "Shaharsozlar shahar va qishloqlarning rivojlanish rejalarini ishlab chiqadi.",
        "maosh": "O'zbekistonda: $500-2000/oy | Xorijda: $4000-12000/oy",
        "kelajak": "Toshkent va viloyatlar shaharsozligi uchun zarur. Xalqaro loyihalarda ishlash mumkin.",
        "talablar": "GIS dasturlari, shaharsozlik qonunchilik, jamiyat bilan ishlash.",
        "universitetlar": "ToshDTU, arxitektura institutlari"
    },
    "🌿 Landshaft Dizayner": {
        "emoji": "🌿",
        "tavsif": "Landshaft dizaynerlar bog', park va ochiq maydonlarni chiroyli va ekologik jihatdan rejalashtiradi.",
        "maosh": "O'zbekistonda: $400-1800/oy | Xorijda: $3000-10000/oy",
        "kelajak": "Yashil shaharlar konsepti o'sishi bilan landshaft dizayn talab kuchaymoqda.",
        "talablar": "O'simlikshunoslik, AutoCAD, ijodkorlik, ekologiya bilimlari.",
        "universitetlar": "ToshDTU, Qishloq xo'jaligi universiteti"
    },
    "👷 Qurilish Muhandisi": {
        "emoji": "👷",
        "tavsif": "Qurilish muhandislari loyiha hujjatlarini tayyorlaydi va qurilish jarayonini nazorat qiladi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy",
        "kelajak": "O'zbekiston qurilish boomi. Yirik infratuzilma loyihalari ko'p.",
        "talablar": "AutoCAD, qurilish materiallar, hisob-kitob, boshqaruv.",
        "universitetlar": "ToshDTU, qurilish institutlari"
    },
    # MUHANDISLIK
    "🤖 Robototexnika Muhandisi": {
        "emoji": "🤖",
        "tavsif": "Robototexnika muhandislari robotlar va avtomatlashtirilgan tizimlarni loyihalaydi.",
        "maosh": "O'zbekistonda: $600-2500/oy | Xorijda: $5000-18000/oy",
        "kelajak": "Sanoat avtomatlashtirish va AI bilan birgalikda juda istiqbolli!",
        "talablar": "Mexanika, elektronika, dasturlash (C++, Python), Arduino.",
        "universitetlar": "TATU, ToshDTU, MIT (xorij)"
    },
    "⚡ Elektr Muhandisi": {
        "emoji": "⚡",
        "tavsif": "Elektr muhandislari elektr tizimlarini loyihalaydi, o'rnatadi va xizmat ko'rsatadi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $4000-12000/oy",
        "kelajak": "Yangilanuvchi energiya (quyosh, shamol) sohasida katta talab.",
        "talablar": "Elektrotexnika, AutoCAD, xavfsizlik qoidalari.",
        "universitetlar": "TATU, ToshDTU, Energetika instituti"
    },
    "🔧 Mexanik Muhandis": {
        "emoji": "🔧",
        "tavsif": "Mexanik muhandislar mashinalar, dvigatellar va mexanik tizimlarni loyihalaydi.",
        "maosh": "O'zbekistonda: $400-1800/oy | Xorijda: $3500-12000/oy",
        "kelajak": "Avtomobil, aviatsiya va ishlab chiqarish sanoatida zarur.",
        "talablar": "SolidWorks, materialshunoslik, termodinamika.",
        "universitetlar": "ToshDTU, Politekhnika"
    },
    "🏭 Avtomatika Muhandisi": {
        "emoji": "🏭",
        "tavsif": "Avtomatika muhandislari ishlab chiqarish jarayonlarini avtomatlashtirishni loyihalaydi.",
        "maosh": "O'zbekistonda: $500-2000/oy | Xorijda: $4000-14000/oy",
        "kelajak": "Sanoat 4.0 va aqlli fabrikalar trendi juda katta imkoniyat!",
        "talablar": "PLC dasturlash, SCADA, robotika.",
        "universitetlar": "TATU, ToshDTU"
    },
    "🏗️ Sanoat Muhandisi": {
        "emoji": "🏗️",
        "tavsif": "Sanoat muhandislari ishlab chiqarish samaradorligini oshirish uchun tizimlar yaratadi.",
        "maosh": "O'zbekistonda: $400-1800/oy | Xorijda: $4000-13000/oy",
        "kelajak": "Lean va Six Sigma metodologiyalari bilan sanoat samaradorligi oshirilmoqda.",
        "talablar": "Lean, Six Sigma, jarayon tahlili.",
        "universitetlar": "ToshDTU, sanoat universitetlari"
    },
    # TIBBIYOT
    "👨‍⚕️ Shifokor": {
        "emoji": "👨‍⚕️",
        "tavsif": "Shifokorlar kasalliklarni tashxislaydi, davolaydi va bemorlar sog'lig'ini saqlaydi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $6000-30000/oy",
        "kelajak": "Tibbiyot doimo zarur kasb. Telemeditsina va AI diagnostika yangi imkoniyat.",
        "talablar": "6 yillik tibbiyot ta'limi + rezidentura.",
        "universitetlar": "ToshDTI, Samarqand DTI, xorij tibbiyot universitetlari"
    },
    "🔪 Jarroh": {
        "emoji": "🔪",
        "tavsif": "Jarrohlar operatsiya orqali kasalliklarni davolaydi va jarohatlarni to'g'rilaydi.",
        "maosh": "O'zbekistonda: $600-3000/oy | Xorijda: $10000-40000/oy",
        "kelajak": "Robot-assistli jarrohlik kelajagi. Da Vinci roboti bilan operatsiyalar o'smoqda.",
        "talablar": "8+ yillik ta'lim, qo'l mahorati, chidamlilik.",
        "universitetlar": "ToshDTI, Respublika ixtisoslashtirilgan markaz"
    },
    "🦷 Stomatolog": {
        "emoji": "🦷",
        "tavsif": "Stomatologlar tish va og'iz kasalliklarini davolaydi, estetik tibbiyot ham qiladi.",
        "maosh": "O'zbekistonda: $500-3000/oy | Xorijda: $5000-20000/oy",
        "kelajak": "Xususiy stomatologiya klinikalari ko'paymoqda. Estetik stomatologiya talabi yuqori.",
        "talablar": "5 yillik ta'lim, nozik qo'l ishi, bemorlar bilan ishlash.",
        "universitetlar": "ToshDTI stomatologiya fakulteti"
    },
    "❤️ Kardiolog": {
        "emoji": "❤️",
        "tavsif": "Kardiologlar yurak va qon tomir kasalliklarini ixtisoslashtirib davolaydi.",
        "maosh": "O'zbekistonda: $600-2500/oy | Xorijda: $8000-30000/oy",
        "kelajak": "Yurak kasalliklari dunyoda eng ko'p tarqalgan. Kardiologlar talab yuqori.",
        "talablar": "8+ yillik ta'lim, EKG, EXO-KG, kardioxirurgiya.",
        "universitetlar": "ToshDTI, Kardiologiya instituti"
    },
    "🧠 Psixiatr": {
        "emoji": "🧠",
        "tavsif": "Psixiatrlar ruhiy kasalliklarni tashxislaydi va dori-darmon bilan davolaydi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $7000-25000/oy",
        "kelajak": "Mental salomatlik muammolari o'smoqda. Psixiatrlarga talab oshmoqda.",
        "talablar": "8+ yillik ta'lim, empat,ya psixologiya bilimlari.",
        "universitetlar": "ToshDTI, Psixiatriya instituti"
    },
    # PSIXOLOGIYA
    "🧠 Psixolog": {
        "emoji": "🧠",
        "tavsif": "Psixologlar odamlarning ruhiy holatini baholaydi va maslahat beradi.",
        "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $3000-12000/oy",
        "kelajak": "Mental salomatlik trendining o'sishi bilan talab oshmoqda.",
        "talablar": "Psixologiya ta'limi, empatiya, tinglash ko'nikmalari.",
        "universitetlar": "O'zMU, TDPU, ToshDU"
    },
    "💆 Psixoterapevt": {
        "emoji": "💆",
        "tavsif": "Psixoterapevtlar mijozlarga uzoq muddatli terapiya orqali yordam beradi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $4000-15000/oy",
        "kelajak": "Onlayn terapiya platformalari global imkoniyat ochmoqda.",
        "talablar": "Psixologiya magistri, sertifikat, superviziya.",
        "universitetlar": "O'zMU, Xalqaro psixologiya institutlari"
    },
    "👥 HR Mutaxassisi": {
        "emoji": "👥",
        "tavsif": "HR mutaxassislari xodimlarni yollash, o'qitish va ish muhitini boshqaradi.",
        "maosh": "O'zbekistonda: $400-1800/oy | Xorijda: $3000-10000/oy",
        "kelajak": "Har bir kompaniya HR kerak. People Analytics yangi trend.",
        "talablar": "Psixologiya, kommunikatsiya, mehnat qonunchiligi.",
        "universitetlar": "O'zMU, TIQXMMI, Westminster"
    },
    "🎯 Career Coach": {
        "emoji": "🎯",
        "tavsif": "Karyera kouchilar odamlarga karyera yo'lini topish va maqsadlarga erishishda yordam beradi.",
        "maosh": "O'zbekistonda: $300-2000/oy | Xorijda: $3000-15000/oy",
        "kelajak": "Karyera maslahat xizmatlariga talab oshib bormoqda.",
        "talablar": "Psixologiya, coaching sertifikati (ICF), tajriba.",
        "universitetlar": "O'zMU + ICF sertifikati"
    },
    "👨‍👩‍👧 Oilaviy Psixolog": {
        "emoji": "👨‍👩‍👧",
        "tavsif": "Oilaviy psixologlar oila munosabatlaridagi muammolarni hal qilishga yordam beradi.",
        "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $3500-12000/oy",
        "kelajak": "Oila masalasi doimo dolzarb. Mahalla markazlari ham ko'proq psixolog yollaydi.",
        "talablar": "Oilaviy terapiya sertifikati, empatiya, sabr.",
        "universitetlar": "O'zMU, maxsus kurslar"
    },
    # TA'LIM
    "📚 O'qituvchi": {
        "emoji": "📚",
        "tavsif": "O'qituvchilar bilim beradi, yoshlarni tarbiyalaydi va jamiyat kelajagini shakllantiradi.",
        "maosh": "O'zbekistonda: $200-800/oy | Xususiy maktab: $500-2000/oy",
        "kelajak": "Ta'lim islohotlari va xususiy maktablar o'sishi bilan yaxshi o'qituvchilarga talab oshmoqda.",
        "talablar": "Pedagog ta'limi, fan bilimi, sabr, kommunikatsiya.",
        "universitetlar": "TDPU, ToshDU, fan universitetlari"
    },
    "🎓 Professor": {
        "emoji": "🎓",
        "tavsif": "Professorlar oliy ta'limda dars beradi, ilmiy tadqiqot o'tkazadi va maqolalar yozadi.",
        "maosh": "O'zbekistonda: $400-1500/oy | Xorijda: $5000-20000/oy",
        "kelajak": "Xalqaro universitetlar va ilmiy markazlar doktorantlar qidirmoqda.",
        "talablar": "PhD darajasi, ilmiy maqolalar, o'qitish tajribasi.",
        "universitetlar": "Har qanday yetakchi universitet"
    },
    "🧑‍🏫 Mentor": {
        "emoji": "🧑‍🏫",
        "tavsif": "Mentorlar shaxsiy tajribalarini bo'lishib, boshqalarga rivojlanishda yo'l ko'rsatadi.",
        "maosh": "Cheksiz — konsalting va o'qitish orqali",
        "kelajak": "Online mentoring platformalari global bozor ochmoqda.",
        "talablar": "Tajriba, empatiya, kommunikatsiya, o'qitish ko'nikmalari.",
        "universitetlar": "Maxsus ta'lim shart emas — tajriba muhim"
    },
    "💪 Trener": {
        "emoji": "💪",
        "tavsif": "Trenerlar sport, biznes yoki hayot ko'nikmalarini o'rgatadi va rivojlanishga yordam beradi.",
        "maosh": "O'zbekistonda: $300-2000/oy | Xorijda: cheksiz",
        "kelajak": "Onlayn treninglar global auditoriya imkoniyati bermoqda.",
        "talablar": "Sertifikat, tajriba, motivatsiya ko'nikmalari.",
        "universitetlar": "Sport akademiyasi + maxsus sertifikatlar"
    },
    "🏫 Ta'lim Menejeri": {
        "emoji": "🏫",
        "tavsif": "Ta'lim menejerlari maktab yoki ta'lim muassasasini boshqaradi, sifatni nazorat qiladi.",
        "maosh": "O'zbekistonda: $500-2000/oy",
        "kelajak": "Xususiy maktab va EdTech kompaniyalar kengaymoqda.",
        "talablar": "Boshqaruv, pedagogika, moliya bilimlari.",
        "universitetlar": "TDPU, TIQXMMI, Westminster"
    },
    # HUQUQ
    "⚖️ Advokat": {
        "emoji": "⚖️",
        "tavsif": "Advokatlar sud jarayonlarida mijozlarini himoya qiladi va huquqiy maslahat beradi.",
        "maosh": "O'zbekistonda: $400-5000/oy | Xorijda: $5000-30000/oy",
        "kelajak": "Biznes va xususiy huquqiy xizmatlarga talab oshmoqda.",
        "talablar": "Yuridik ta'lim, advokat sertifikati, nutq san'ati.",
        "universitetlar": "ToshDYUI, O'zMU huquq, TDYUI"
    },
    "📜 Yurist": {
        "emoji": "📜",
        "tavsif": "Yuristlar huquqiy masalalar bo'yicha maslahat beradi, hujjat tuzadi va nizolarni hal qiladi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-15000/oy",
        "kelajak": "Korxonalar, banklar va davlat tashkilotlarda doimiy talab.",
        "talablar": "Yuridik ta'lim, qonunchilik bilimlari.",
        "universitetlar": "ToshDYUI, O'zMU, TDYUI"
    },
    "👮 Prokuror": {
        "emoji": "👮",
        "tavsif": "Prokurorlar jinoyat ishlarini ko'rib chiqadi, aybdorlarni sudga tortadi.",
        "maosh": "O'zbekistonda: $400-1500/oy + imtiyozlar",
        "kelajak": "Davlat xizmatida barqaror ish va ijtimoiy himoya.",
        "talablar": "Yuridik ta'lim, prokuratura akademiyasi, xizmat.",
        "universitetlar": "ToshDYUI, Prokuratura akademiyasi"
    },
    "🏛️ Sudya": {
        "emoji": "🏛️",
        "tavsif": "Sudyalar qonun asosida sud ishlarini ko'rib chiqib, adolatli qaror chiqaradi.",
        "maosh": "O'zbekistonda: $600-2000/oy + imtiyozlar",
        "kelalak": "Sud tizimi islohoti davom etmoqda. Katta mas'uliyat va nufuz.",
        "talablar": "Yuridik ta'lim, 5+ yil tajriba, Oliy sud tavsiyasi.",
        "universitetlar": "ToshDYUI, Sud akademiyasi"
    },
    "🔍 Tergovchi": {
        "emoji": "🔍",
        "tavsif": "Tergovchilar jinoyat ishlarini o'rganib, dalillar yig'adi va tergov olib boradi.",
        "maosh": "O'zbekistonda: $350-1200/oy + imtiyozlar",
        "kelajak": "Kiber jinoyatlar va moliyaviy tergov yangi yo'nalishlar.",
        "talablar": "Yuridik ta'lim, kriminalistika, jismoniy tayyorgarlik.",
        "universitetlar": "ToshDYUI, IIV akademiyasi"
    },
    # MARKETING
    "📱 SMM Manager": {
        "emoji": "📱",
        "tavsif": "SMM menejerlar ijtimoiy tarmoqlarda brend sahifalarini boshqaradi va kontent yaratadi.",
        "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $2000-8000/oy",
        "kelajak": "Har bir brend ijtimoiy tarmoq kerakligi uchun talab kamaymasligi mumkin.",
        "talablar": "Kontent yaratish, tahlil, ijodkorlik, Canva, dizayn.",
        "universitetlar": "Marketing kurslari + amaliyot"
    },
    "🔍 SEO Specialist": {
        "emoji": "🔍",
        "tavsif": "SEO mutaxassislari veb saytlarni Google qidiruv natijalari tepasiga chiqaradi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy",
        "kelajak": "Raqamli marketing o'sishi bilan SEO talab katta.",
        "talablar": "Google Analytics, Ahrefs, kalit so'z tahlili, HTML asoslari.",
        "universitetlar": "Online kurslar + amaliyot"
    },
    "💻 Digital Marketer": {
        "emoji": "💻",
        "tavsif": "Raqamli marketologlar onlayn kanallar orqali mahsulot va xizmatlarni targ'ib qiladi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy",
        "kelajak": "Bizneslar raqamli kanalga o'tishi bilan talab o'smoqda.",
        "talablar": "Google Ads, Facebook Ads, SEO, email marketing.",
        "universitetlar": "Marketing kurslari, Google sertifikatlari"
    },
    "🏷️ Brand Manager": {
        "emoji": "🏷️",
        "tavsif": "Brend menejerlari kompaniya brendining qiyofasini boshqaradi va rivojlantiradi.",
        "maosh": "O'zbekistonda: $500-2500/oy | Xorijda: $4000-15000/oy",
        "kelajak": "Global brendlar va mahalliy kompaniyalar uchun zarur.",
        "talablar": "Marketing strategiyasi, kommunikatsiya, analitika.",
        "universitetlar": "TIQXMMI, Westminster marketing"
    },
    "✍️ Copywriter": {
        "emoji": "✍️",
        "tavsif": "Kopirayterlar reklama, veb sayt va marketing uchun sotuv qiluvchi matn yozadi.",
        "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $2000-10000/oy",
        "kelajak": "Kontent marketing o'sishi bilan copywriting talab oshmoqda. Freelance yaxshi.",
        "talablar": "Yozish ko'nikmalari, psixologiya, marketing asoslari.",
        "universitetlar": "Jurnalistika + marketing kurslari"
    },
    # XALQARO ALOQALAR
    "🤝 Diplomat": {
        "emoji": "🤝",
        "tavsif": "Diplomatlar mamlakatlar o'rtasida munosabatlarni boshqaradi va manfaatlarni himoya qiladi.",
        "maosh": "O'zbekistonda: $600-3000/oy + imtiyozlar | Xorijda: cheksiz",
        "kelajak": "O'zbekiston xalqaro aloqalarini kengaytirib bormoqda. Diplomatik xizmat kengaymoqda.",
        "talablar": "Xalqaro aloqalar ta'limi, til bilimlari (3+), protokol.",
        "universitetlar": "O'zMU XHXF, TMDH, MGIMO (xorij)"
    },
    "🗣️ Tarjimon": {
        "emoji": "🗣️",
        "tavsif": "Tarjimonlar tillar o'rtasida ma'no va g'oyalarni to'liq va aniq yetkazadi.",
        "maosh": "O'zbekistonda: $300-2000/oy | Xorijda: $2000-10000/oy",
        "kelajak": "AI tarjimasi rivoji bo'lsa ham, sifatli tarjimonlar kerak bo'lib qolaveradi.",
        "talablar": "2+ til mukammal bilimi, madaniy tushuncha, diqqat.",
        "universitetlar": "O'zMU filologiya, ToshDU chet tillari"
    },
    "🌐 Xalqaro Menejer": {
        "emoji": "🌐",
        "tavsif": "Xalqaro menejerlar global kompaniyalarning xorijiy operatsiyalarini boshqaradi.",
        "maosh": "O'zbekistonda: $600-3000/oy | Xorijda: $4000-20000/oy",
        "kelajak": "Multinatsional kompaniyalar O'zbekistonga kirib kelmoqda.",
        "talablar": "MBA, ingliz tili, madaniyatlararo muloqot, menejment.",
        "universitetlar": "Westminster, Turin, TIQXMMI"
    },
    "🏛️ Elchixona Xodimi": {
        "emoji": "🏛️",
        "tavsif": "Elchixona xodimlari xorijdagi vatandoshlar manfaatini himoya qiladi, viza va konsular xizmat ko'rsatadi.",
        "maosh": "O'zbekistonda (MFA): $400-1500/oy + xorijda yashash imtiyozlari",
        "kelajak": "Diplomatik korpus barqaror va nufuzli kasb.",
        "talablar": "XH ta'limi, til bilimlari, protokol bilimi.",
        "universitetlar": "O'zMU XHXF, TMDH"
    },
    "📦 Tashqi Savdo Mutaxassisi": {
        "emoji": "📦",
        "tavsif": "Tashqi savdo mutaxassislari eksport-import operatsiyalarini boshqaradi va xalqaro shartnomalar tuzadi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy",
        "kelajak": "O'zbekiston eksportini oshirish siyosati bu kasb talabini oshirmoqda.",
        "talablar": "Savdo huquqi, til bilimlari, logistika asoslari.",
        "universitetlar": "TIQXMMI, O'zMU iqtisodiyot"
    },
    # TURIZM
    "🗺️ Tur Menejer": {
        "emoji": "🗺️",
        "tavsif": "Tur menejerlar turistik marshrut va paketlarni tashkil qiladi, mijozlarga xizmat ko'rsatadi.",
        "maosh": "O'zbekistonda: $300-1500/oy | Xorijda: $2000-8000/oy",
        "kelajak": "O'zbekistonga turizm o'smoqda. Samarqand, Buxoro — xalqaro markaz.",
        "talablar": "Turizm ta'limi, til bilimlari, geogfiya, kommunikatsiya.",
        "universitetlar": "ToshDTU turizm, O'zMU"
    },
    "🧭 Gid": {
        "emoji": "🧭",
        "tavsif": "Gidlar turistlarni tarixiy joylarda olib yuradi, ma'lumot beradi va tajribani boyitadi.",
        "maosh": "O'zbekistonda: $20-100/tur + choy pullari | Xorijda: $50-500/kun",
        "kelajak": "Chet ellik turistlar uchun malakali gidlar yetishmayapti. Katta imkoniyat!",
        "talablar": "Til bilimlari (ingliz, rus, xitoy), tarix bilimi, kommunikatsiya.",
        "universitetlar": "Turizm instituti + til kurslari"
    },
    "🏨 Hotel Manager": {
        "emoji": "🏨",
        "tavsif": "Hotel menejerlari mehmonxona operatsiyalarini boshqaradi, mehmonlar tajribasini ta'minlaydi.",
        "maosh": "O'zbekistonda: $500-2500/oy | Xorijda: $3000-15000/oy",
        "kelajak": "Yangi mehmonxonalar qurilishi bilan malakali menejerlar kerak.",
        "talablar": "Gostepriimlik menejment, til bilimlari, boshqaruv.",
        "universitetlar": "ToshDTU, Swiss Hotel Management School (xorij)"
    },
    "📸 Travel Blogger": {
        "emoji": "📸",
        "tavsif": "Sayohat bloggerlar safari davomida kontent yaratib, auditoriya to'playdi va reklama orqali daromad oladi.",
        "maosh": "Cheksiz — hamkorlik, reklama, affiliate marketing",
        "kelajak": "Sayohat kontenti qiziqishi o'smoqda. O'zbek sayohat bloggerlari kam.",
        "talablar": "Fotografiya, video montaj, yozish, SEO, ijtimoiy tarmoq.",
        "universitetlar": "Maxsus ta'lim shart emas — amaliyot muhim"
    },
    "✈️ Pilot": {
        "emoji": "✈️",
        "tavsif": "Pilotlar yo'lovchi va yuk samolyotlarini boshqaradi, xavfsiz parvozlarni ta'minlaydi.",
        "maosh": "O'zbekistonda: $1500-5000/oy | Xorijda: $5000-25000/oy",
        "kelajak": "O'zbekiston aviatsiyasi kengaymoqda. Yangi pilot talab katta.",
        "talablar": "Aviatsiya akademiyasi, PPL/CPL litsenziya, ingliz tili (ICAO).",
        "universitetlar": "O'zbekiston Aviatsiya akademiyasi"
    },
    # SPORT
    "⚽ Futbolchi": {
        "emoji": "⚽",
        "tavsif": "Professional futbolchilar sport klublari uchun o'ynaydi, musobaqalarda ishtirok etadi.",
        "maosh": "O'zbekistonda: $500-5000/oy | Xorijda: cheksiz",
        "kelajak": "O'zbek futboli rivojlanmoqda. Xorijiy ligalarga chiqqan futbolchilar soni o'smoqda.",
        "talablar": "Jismoniy tayyorgarlik, texnika, taktika, intizom.",
        "universitetlar": "RSSSMM, futbol akademiyalari"
    },
    "🥊 Bokschi": {
        "emoji": "🥊",
        "tavsif": "Professional bokschlar ring raqobatida kurashadi va professional daromad oladi.",
        "maosh": "O'zbekistonda: $300-2000/musobaqa | Xorijda: cheksiz",
        "kelajak": "O'zbek bokschilar olimpiya chempionlari. Professional boks sanoati katta.",
        "talablar": "Texnika, jismoniy kuch, taktika, psixologik barqarorlik.",
        "universitetlar": "Sport akademiyalari, boks maktablari"
    },
    "🥋 UFC Jangchisi": {
        "emoji": "🥋",
        "tavsif": "UFC jangchilar aralash kurash (MMA) bilan shug'ullanadi va professional musobaqalarda ishtirok etadi.",
        "maosh": "UFC: $10,000-100,000+/musobaqa",
        "kelajak": "MMA sanoati tez o'smoqda. O'zbek jangchilar UFC ga kirmoqda.",
        "talablar": "Ko'p kurash turi (boks, judo, grappling), jismoniy tayyorgarlik.",
        "universitetlar": "Sport akademiyalari, MMA zamlari"
    },
    "🏀 Basketbolchi": {
        "emoji": "🏀",
        "tavsif": "Professional basketbolchilar jamoalar uchun o'ynaydi, milliy va xalqaro musobaqalarda ishtirok etadi.",
        "maosh": "O'zbekistonda: $300-2000/oy | NBA: millionlar",
        "kelajak": "O'zbek basketbol rivojlanmoqda. Yosh iqtidorlarni chet el klublari qidirmoqda.",
        "talablar": "Bo'y, texnika, jamoaviy o'yin, jismoniy tayyorgarlik.",
        "universitetlar": "RSSSMM, sport akademiyalari"
    },
    "🎾 Tennischi": {
        "emoji": "🎾",
        "tavsif": "Professional tennis o'yinchilar ATP/WTA turnirlarida qatnashib, reyting va mukofot pullar yig'adi.",
        "maosh": "Cheksiz — Grand Slam g'oliblar millionlar ishlaydi",
        "kelajak": "Tennis global sport. O'zbek tennischilari xalqaro reyting olmoqda.",
        "talablar": "Texnika, jismoniy tayyorgarlik, taktika, ruhiy barqarorlik.",
        "universitetlar": "Tennis akademiyalari, sport maktablari"
    },
    # LOGISTIKA
    "📦 Logistika Menejeri": {
        "emoji": "📦",
        "tavsif": "Logistika menejerlari yuk tashish, saqlash va yetkazib berish jarayonlarini boshqaradi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy",
        "kelajak": "E-commerce o'sishi bilan logistika talab oshmoqda.",
        "talablar": "Logistika ta'limi, ERP tizimlar, boshqaruv ko'nikmalari.",
        "universitetlar": "TIQXMMI, ToshDTU, logistika kurslari"
    },
    "🔗 Supply Chain Specialist": {
        "emoji": "🔗",
        "tavsif": "Ta'minot zanjiri mutaxassislari xomashyodan mahsulotgacha jarayonni optimallashtiradi.",
        "maosh": "O'zbekistonda: $500-2500/oy | Xorijda: $4000-15000/oy",
        "kelajak": "Global ta'minot zanjirlari murakkablashishi bilan talab o'sdi.",
        "talablar": "CSCP sertifikati, ERP, tahliliy fikrlash.",
        "universitetlar": "TIQXMMI + APICS sertifikat"
    },
    "🚛 Transport Menejeri": {
        "emoji": "🚛",
        "tavsif": "Transport menejerlari transport parki va yuk tashish operatsiyalarini boshqaradi.",
        "maosh": "O'zbekistonda: $400-1800/oy | Xorijda: $3000-10000/oy",
        "kelajak": "Transport infratuzilmasi rivojlanishi bilan talab oshmoqda.",
        "talablar": "Transport qonunchiligi, fleet management, logistika.",
        "universitetlar": "ToshDTU transport, TIQXMMI"
    },
    "🌏 Import/Export Mutaxassisi": {
        "emoji": "🌏",
        "tavsif": "Import/eksport mutaxassislari xalqaro savdo operatsiyalarini boshqaradi va bojxona rasmiylashtiruvi.",
        "maosh": "O'zbekistonda: $400-2000/oy | Xorijda: $3000-12000/oy",
        "kelajak": "O'zbekiston eksporti kengayishi bilan bu kasb talabi oshmoqda.",
        "talablar": "Xalqaro savdo qoidalari, Incoterms, til bilimlari.",
        "universitetlar": "TIQXMMI, O'zMU iqtisodiyot"
    },
    "✈️ Aviatsiya Logistika Mutaxassisi": {
        "emoji": "✈️",
        "tavsif": "Aviatsiya logistika mutaxassislari havo yo'li bilan yuk tashish va saqlashni boshqaradi.",
        "maosh": "O'zbekistonda: $500-2500/oy | Xorijda: $4000-15000/oy",
        "kelajak": "Havo yuk tashish sanoati o'smoqda. O'zbekiston tranzit markaz bo'lmoqda.",
        "talablar": "Aviatsiya qoidalari, logistika, ingliz tili.",
        "universitetlar": "Aviatsiya akademiyasi, TIQXMMI"
    },
    # ILM-FAN
    "⚛️ Fizik": {
        "emoji": "⚛️",
        "tavsif": "Fiziklar tabiat qonunlarini o'rganadi, yangi texnologiyalar va bilimlar kashf etadi.",
        "maosh": "O'zbekistonda: $300-1200/oy | Xorijda: $4000-15000/oy",
        "kelalak": "Kvant hisoblash, yadrо energiyasi va nanotexnologiya sohalari rivojlanmoqda.",
        "talablar": "Fizika va matematika, PhD darajasi, tadqiqot ko'nikmalari.",
        "universitetlar": "ToshDU fizika, O'zMU, JINR (xorij)"
    },
    "🧪 Kimyogar": {
        "emoji": "🧪",
        "tavsif": "Kimyogarlar yangi moddalar va materiallarni kashf etadi, sanoat va tibbiyotda qo'llaydi.",
        "maosh": "O'zbekistonda: $300-1200/oy | Xorijda: $4000-14000/oy",
        "kelajak": "Farmatsevtika, neft-kimyo va yangi materiallar sanoatida talab bor.",
        "talablar": "Kimyo ta'limi, laboratoriya ko'nikmalari, PhD.",
        "universitetlar": "ToshDU, O'z FA kimyo instituti"
    },
    "🌿 Biolog": {
        "emoji": "🌿",
        "tavsif": "Biologlar tirik organizmlarni o'rganadi, tibbiyot va ekologiya uchun kashfiyotlar qiladi.",
        "maosh": "O'zbekistonda: $300-1100/oy | Xorijda: $3500-12000/oy",
        "kelajak": "Biotexnologiya, genetik muhandislik va biofarmatsevtika rivojlanmoqda.",
        "talablar": "Biologiya ta'limi, laboratoriya ko'nikmalari, PhD.",
        "universitetlar": "ToshDU biologiya, O'z FA"
    },
    "🔭 Astronom": {
        "emoji": "🔭",
        "tavsif": "Astronomlar yulduzlar, sayyoralar va koinotni o'rganadi, kosmik tadqiqotlar olib boradi.",
        "maosh": "O'zbekistonda: $300-1000/oy | Xorijda: $4000-15000/oy",
        "kelajak": "SpaceX va NASA kabi kompaniyalar kosmik tadqiqotlarni kengaytirmoqda.",
        "talablar": "Fizika va matematika, PhD, teleskop bilan ishlash.",
        "universitetlar": "ToshDU, O'zbekiston FA Astronomiya instituti"
    },
    "🔬 Tadqiqotchi": {
        "emoji": "🔬",
        "tavsif": "Tadqiqotchilar muayyan sohalarda yangi bilimlar kashf etadi va ilmiy maqolalar yozadi.",
        "maosh": "O'zbekistonda: $300-1200/oy | Xorijda: $4000-15000/oy",
        "kelajak": "Ilmiy grantlar va xalqaro hamkorlik imkoniyatlari o'smoqda.",
        "talablar": "PhD darajasi, tadqiqot metodologiyasi, maqola yozish.",
        "universitetlar": "Har qanday oliy ta'lim muassasasi"
    },
    # QISHLOQ XO'JALIGI
    "🐾 Veterinar": {
        "emoji": "🐾",
        "tavsif": "Veterinarlar hayvon kasalliklarini davolaydi, sog'liqni saqlaydi va oldini olish choralari ko'radi.",
        "maosh": "O'zbekistonda: $300-1200/oy | Xorijda: $3000-10000/oy",
        "kelajak": "Chorvachilik sanoati o'sishi bilan veterinar talab oshmoqda.",
        "talablar": "Veterinariya ta'limi, hayvonlarni sevish, amaliy ko'nikmalar.",
        "universitetlar": "SamQXI, ToshDQXI"
    },
    "🌾 Agronom": {
        "emoji": "🌾",
        "tavsif": "Agronomlar o'simlik yetishtirish, tuproq sifati va hosildorlikni oshirish bo'yicha mutaxassis.",
        "maosh": "O'zbekistonda: $300-1200/oy | Xorijda: $3000-10000/oy",
        "kelajak": "Oziq-ovqat xavfsizligi va smart farming agronom talabini oshirmoqda.",
        "talablar": "Agronomy ta'limi, tuproqshunoslik, o'simlikshunoslik.",
        "universitetlar": "ToshDQXI, SamQXI"
    },
    "👨‍🌾 Fermer": {
        "emoji": "👨‍🌾",
        "tavsif": "Fermerlar qishloq xo'jaligi mahsulotlari yetishtirib, bozorga yetkazib beradi.",
        "maosh": "Cheksiz — o'z fermasi daromadiga qarab",
        "kelajak": "Organik fermerchilik va agroturizm yangi imkoniyatlar bermoqda.",
        "talablar": "Agronomy bilimi, biznes tafakkuri, mehnatsevarlik.",
        "universitetlar": "QXI yoki amaliy tajriba"
    },
    "🌱 Agrotexnolog": {
        "emoji": "🌱",
        "tavsif": "Agrotexnologlar yangi texnologiyalar orqali qishloq xo'jaligi samaradorligini oshiradi.",
        "maosh": "O'zbekistonda: $400-1500/oy | Xorijda: $3000-12000/oy",
        "kelajak": "Dronlar, sensorlar va AI fermerchilikda keng qo'llanilmoqda.",
        "talablar": "Agronomy + IT bilimlari, drone boshqarish.",
        "universitetlar": "ToshDQXI, TATU AgriTech"
    },
    "🐄 Zooinjener": {
        "emoji": "🐄",
        "tavsif": "Zooinjenerlar hayvon zotlarini yaxshilash, ularni parvarish qilish va mahsuldorlikni oshiradi.",
        "maosh": "O'zbekistonda: $300-1200/oy",
        "kelajak": "Chorvachilik modernizatsiyasi bilan talab oshmoqda.",
        "talablar": "Zoologiya, genetika, hayvon fizologiyasi.",
        "universitetlar": "ToshDQXI zootexniya"
    },
    # XAVFSIZLIK
    "🎖️ Harbiy Ofitser": {
        "emoji": "🎖️",
        "tavsif": "Harbiy ofitserlar qurolli kuchlarni boshqaradi, mamlakatni himoya qiladi.",
        "maosh": "O'zbekistonda: $400-1500/oy + imtiyozlar",
        "kelajak": "Barqaror davlat xizmati, ijtimoiy himoya va uy-joy imtiyozlari.",
        "talablar": "Harbiy akademiya, jismoniy tayyorgarlik, liderlik.",
        "universitetlar": "O'zbekiston Harbiy akademiyasi"
    },
    "🔬 Kriminalist": {
        "emoji": "🔬",
        "tavsif": "Kriminalistlar jinoyat dalillarini ilmiy usullar bilan o'rganib, tergovga yordam beradi.",
        "maosh": "O'zbekistonda: $350-1200/oy | Xorijda: $3000-10000/oy",
        "kelajak": "DNA tahlili, raqamli kriminalistika yangi yo'nalishlar.",
        "talablar": "Kimyo, biologiya, huquqshunoslik, laboratoriya ko'nikmalari.",
        "universitetlar": "ToshDYUI, IIV akademiyasi"
    },
    "💪 Maxsus Kuchlar Xodimi": {
        "emoji": "💪",
        "tavsif": "Maxsus kuchlar xodimlari murakkab vaziyatlarda harakat qiladigan elita harbiy guruhlar.",
        "maosh": "O'zbekistonda: $500-2000/oy + imtiyozlar",
        "kelajak": "Milliy xavfsizlik tizimida eng nufuzli lavozim.",
        "talablar": "Juda yuqori jismoniy va aqliy tayyorgarlik, harbiy ta'lim.",
        "universitetlar": "Harbiy akademiya + maxsus o'quv markazlari"
    },
    "🕵️ Detektiv": {
        "emoji": "🕵️",
        "tavsif": "Detektivlar jinoyatlarni tekshiradi, dalil yig'adi va aybdorlarni aniqlaydi.",
        "maosh": "O'zbekistonda: $350-1500/oy | Xorijda: $3000-10000/oy",
        "kelajak": "Kiber jinoyatlar va moliyaviy tergov yangi ixtisoslik yo'nalishlari.",
        "talablar": "Huquq, psixologiya, kuzatuv ko'nikmalari, OSINT.",
        "universitetlar": "ToshDYUI, IIV akademiyasi"
    },
    "🛡️ Milliy Xavfsizlik Mutaxassisi": {
        "emoji": "🛡️",
        "tavsif": "Milliy xavfsizlik mutaxassislari davlat xavfsizligini ta'minlash uchun tahlil va strategiya ishlab chiqadi.",
        "maosh": "O'zbekistonda: $500-2000/oy + imtiyozlar",
        "kelajak": "Kiber xavfsizlik, razvedka va strategik tahlil sohalari rivojlanmoqda.",
        "talablar": "Huquq, xalqaro aloqalar, analitik fikrlash, maxfiylik.",
        "universitetlar": "DXA, harbiy akademiyalar"
    },
}

class Onboarding(StatesGroup):
    ism = State()
    sinf = State()
    ota_raqam = State()
    yonalish = State()
    kasb_tanlash = State()
    kasb_tasdiqlash = State()

async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status not in ["left", "kicked"]
    except:
        return False

def obuna_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanalga o'tish", url="https://t.me/AI_Maqsad")],
        [InlineKeyboardButton(text="✅ Obuna bo'ldim", callback_data="check_sub")]
    ])

def kasb_tasdiqlash_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Shu kasbni tanlayman!", callback_data="kasb_tasdiqlash")],
        [InlineKeyboardButton(text="⬅️ Orqaga (kasb o'zgartirish)", callback_data="kasb_orqaga")],
        [InlineKeyboardButton(text="🔄 Yo'nalishni o'zgartirish", callback_data="yonalish_orqaga")]
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
        "Ismingiz nima?",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Onboarding.ism)

@router.message(Onboarding.ism)
async def get_ism(message: Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer(f"Zo'r ism! 👏\n\nNechichi sinfda o'qiysiz?")
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
        "✅ Ota-onangiz progressingizni ko'radi\n"
        "🏆 Sertifikat oladi\n"
        "🔔 Yutuqlaringizdan xabar topadi\n\n"
        "Quyidagi tugmani bosing yoki qo'lda kiriting (+998XXXXXXXXX):",
        reply_markup=keyboard
    )
    await state.set_state(Onboarding.ota_raqam)

@router.message(Onboarding.ota_raqam, F.contact)
async def get_raqam_contact(message: Message, state: FSMContext):
    raqam = message.contact.phone_number
    if not raqam.startswith("+"): raqam = "+" + raqam
    await state.update_data(ota_raqam=raqam)
    await message.answer(
        "✅ Raqam saqlandi!\n\nEndi yo'nalishingizni tanlang 👇",
        reply_markup=yonalish_keyboard()
    )
    await state.set_state(Onboarding.yonalish)

@router.message(Onboarding.ota_raqam, F.text)
async def get_raqam_text(message: Message, state: FSMContext):
    raqam = message.text.strip()
    if not re.match(r'^\+998\d{9}$', raqam):
        await message.answer("❌ Raqam noto'g'ri!\nTo'g'ri format: +998901234567\nQaytadan kiriting:")
        return
    await state.update_data(ota_raqam=raqam)
    await message.answer(

@router.callback_query(F.data == "kasb_orqaga", Onboarding.kasb_tasdiqlash)
async def kasb_orqaga_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.delete()
    await call.message.answer(
        f"Boshqa kasb tanlang 👇",
        reply_markup=kasb_keyboard(data["yonalish"])
    )
    await state.set_state(Onboarding.kasb_tanlash)

@router.callback_query(F.data == "yonalish_orqaga", Onboarding.kasb_tasdiqlash)
async def yonalish_orqaga_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        "Yo'nalishni qaytadan tanlang 👇",
        reply_markup=yonalish_keyboard()
    )
    await state.set_state(Onboarding.yonalish)
