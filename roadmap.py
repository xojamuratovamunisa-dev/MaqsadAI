"""7 kunlik boshlang'ich yo'l xarita.
Har bir vazifa foydalanuvchi tanlagan kasb va yo'nalishga avtomatik moslashadi.
"""

# (vazifa, vaqt, maqsad) — {kasb} va {yonalish} avtomatik almashtiriladi
PLAN = [
    ("{kasb} kim va u nima qiladi? YouTube'dan 2 ta video ko'r", "30 daqiqa", "5 ta yangi faktni daftaringga yoz"),
    ("{yonalish} sohasidagi 3 ta mashhur insonni o'rgan", "40 daqiqa", "Har biri haqida 3 ta gap yoz"),
    ("{kasb} bo'lish uchun kerakli ko'nikmalar ro'yxatini tuz", "30 daqiqa", "Kamida 5 ta ko'nikma yoz"),
    ("Ro'yxatdan 1 ta ko'nikmani tanlab, asoslarini o'rgan", "45 daqiqa", "3 ta mashq yoki konspekt qil"),
    ("{kasb}ning bir ish kuni qanday o'tadi? Maqola yoki video top", "30 daqiqa", "O'z so'zing bilan qisqacha yozib chiq"),
    ("{kasb} O'zbekistonda va dunyoda qancha daromad qiladi? O'rgan", "25 daqiqa", "Raqamlarni solishtirib yoz"),
    ("1 yillik rejang: {kasb} bo'lish yo'lida nima qilasan?", "45 daqiqa", "3 ta aniq maqsad yozib chiq"),
]

TOTAL_DAYS = len(PLAN)


def get_task(day: int, yonalish: str, kasb: str):
    """Kun raqami bo'yicha vazifani qaytaradi."""
    title, vaqt, maqsad = PLAN[day - 1]
    return title.format(kasb=kasb, yonalish=yonalish), vaqt, maqsad
