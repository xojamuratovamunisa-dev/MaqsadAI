from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def yonalish_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💻 Texnologiya"), KeyboardButton(text="💼 Biznes")],
            [KeyboardButton(text="💰 Moliya"), KeyboardButton(text="🎨 Dizayn")],
            [KeyboardButton(text="📱 Media"), KeyboardButton(text="🎭 San'at")],
            [KeyboardButton(text="🏗️ Arxitektura"), KeyboardButton(text="⚙️ Muhandislik")],
            [KeyboardButton(text="🧬 Tibbiyot"), KeyboardButton(text="🧠 Psixologiya")],
            [KeyboardButton(text="🎓 Ta'lim"), KeyboardButton(text="⚖️ Huquq")],
            [KeyboardButton(text="📊 Marketing"), KeyboardButton(text="🌍 Xalqaro Aloqalar")],
            [KeyboardButton(text="✈️ Turizm"), KeyboardButton(text="🏋️ Sport")],
            [KeyboardButton(text="🚚 Logistika"), KeyboardButton(text="🔭 Ilm-fan")],
            [KeyboardButton(text="🌱 Qishloq Xo'jaligi"), KeyboardButton(text="🛡️ Xavfsizlik")],
        ],
        resize_keyboard=True
    )

def kasb_keyboard(yonalish: str):
    kasblar = {
        "💻 Texnologiya": ["👨‍💻 Dasturchi", "🤖 AI Engineer", "🔐 Cybersecurity Specialist", "📊 Data Analyst", "🎮 Game Developer"],
        "💼 Biznes": ["🚀 Startup Founder", "👔 CEO", "📦 Product Manager", "📋 Project Manager", "💡 Biznes Konsultant"],
        "💰 Moliya": ["📈 Trader", "💹 Investor", "📊 Financial Analyst", "🧾 Accountant", "🏦 Bankir"],
        "🎨 Dizayn": ["🖼️ Grafik Dizayner", "📱 UI/UX Dizayner", "🎬 Motion Dizayner", "🗿 3D Artist", "🌐 Web Dizayner"],
        "📱 Media": ["📹 YouTuber", "✍️ Blogger", "🎞️ Video Editor", "🎮 Streamer", "📰 Jurnalist"],
        "🎭 San'at": ["🎤 Singer", "🎭 Aktyor", "🎵 Musiqachi", "🎧 DJ", "🎬 Rejissyor"],
        "🏗️ Arxitektura": ["🏛️ Arxitektor", "🛋️ Interyer Dizayner", "🏙️ Urban Planner", "🌿 Landshaft Dizayner", "👷 Qurilish Muhandisi"],
        "⚙️ Muhandislik": ["🤖 Robototexnika Muhandisi", "⚡ Elektr Muhandisi", "🔧 Mexanik Muhandis", "🏭 Avtomatika Muhandisi", "🏗️ Sanoat Muhandisi"],
        "🧬 Tibbiyot": ["👨‍⚕️ Shifokor", "🔪 Jarroh", "🦷 Stomatolog", "❤️ Kardiolog", "🧠 Psixiatr"],
        "🧠 Psixologiya": ["🧠 Psixolog", "💆 Psixoterapevt", "👥 HR Mutaxassisi", "🎯 Career Coach", "👨‍👩‍👧 Oilaviy Psixolog"],
        "🎓 Ta'lim": ["📚 O'qituvchi", "🎓 Professor", "🧑‍🏫 Mentor", "💪 Trener", "🏫 Ta'lim Menejeri"],
        "⚖️ Huquq": ["⚖️ Advokat", "📜 Yurist", "👮 Prokuror", "🏛️ Sudya", "🔍 Tergovchi"],
        "📊 Marketing": ["📱 SMM Manager", "🔍 SEO Specialist", "💻 Digital Marketer", "🏷️ Brand Manager", "✍️ Copywriter"],
        "🌍 Xalqaro Aloqalar": ["🤝 Diplomat", "🗣️ Tarjimon", "🌐 Xalqaro Menejer", "🏛️ Elchixona Xodimi", "📦 Tashqi Savdo Mutaxassisi"],
        "✈️ Turizm": ["🗺️ Tur Menejer", "🧭 Gid", "🏨 Hotel Manager", "📸 Travel Blogger", "✈️ Pilot"],
        "🏋️ Sport": ["⚽ Futbolchi", "🥊 Bokschi", "🥋 UFC Jangchisi", "🏀 Basketbolchi", "🎾 Tennischi"],
        "🚚 Logistika": ["📦 Logistika Menejeri", "🔗 Supply Chain Specialist", "🚛 Transport Menejeri", "🌏 Import/Export Mutaxassisi", "✈️ Aviatsiya Logistika Mutaxassisi"],
        "🔭 Ilm-fan": ["⚛️ Fizik", "🧪 Kimyogar", "🌿 Biolog", "🔭 Astronom", "🔬 Tadqiqotchi"],
        "🌱 Qishloq Xo'jaligi": ["🐾 Veterinar", "🌾 Agronom", "👨‍🌾 Fermer", "🌱 Agrotexnolog", "🐄 Zooinjener"],
        "🛡️ Xavfsizlik": ["🎖️ Harbiy Ofitser", "🔬 Kriminalist", "💪 Maxsus Kuchlar Xodimi", "🕵️ Detektiv", "🛡️ Milliy Xavfsizlik Mutaxassisi"],
    }
    kasb_list = kasblar.get(yonalish, ["Kasb 1", "Kasb 2", "Kasb 3", "Kasb 4", "Kasb 5"])
    keyboard = [[KeyboardButton(text=kasb)] for kasb in kasb_list]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Vazifalar"), KeyboardButton(text="🗺️ Yo'l xarita")],
            [KeyboardButton(text="🏆 Reyting"), KeyboardButton(text="👤 Profil")],
            [KeyboardButton(text="💎 Premium")],
        ],
        resize_keyboard=True
    )
