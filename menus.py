from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def yonalish_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📐 Texnika"), KeyboardButton(text="🧬 Tibbiyot")],
            [KeyboardButton(text="⚖️ Huquq"), KeyboardButton(text="💼 Biznes")],
            [KeyboardButton(text="🎨 Ijodkorlik"), KeyboardButton(text="💻 IT")],
        ],
        resize_keyboard=True
    )

def kasb_keyboard(yonalish: str):
    kasblar = {
        "📐 Texnika": ["⚙️ Muhandis", "🏗️ Arxitektor", "🔌 Elektrik", "🚗 Avtomexanik", "✈️ Aviator"],
        "🧬 Tibbiyot": ["👨‍⚕️ Shifokor", "🦷 Stomatolog", "💊 Farmatsevt", "🧠 Psixolog", "🔬 Laborant"],
        "⚖️ Huquq": ["⚖️ Yurist", "👮 Prokuror", "🏛️ Sudya", "🔍 Detektiv", "📜 Notarius"],
        "💼 Biznes": ["📊 Moliyachi", "📈 Marketolog", "🏢 Menejer", "💹 Investor", "🤝 HR Mutaxassis"],
        "🎨 Ijodkorlik": ["🎨 Dizayner", "📸 Fotograf", "🎬 Rejissyor", "✍️ Yozuvchi", "🎵 Musiqachi"],
        "💻 IT": ["👨‍💻 Dasturchi", "🔐 Kiberjamiyat", "📱 Mobile Dev", "🤖 AI Muhandis", "🗄️ Data Scientist"],
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
