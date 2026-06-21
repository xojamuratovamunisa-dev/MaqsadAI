import aiosqlite
from datetime import date

DB_PATH = "maqsadai.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (kasb TEXT,
vazifa_vaqti INTEGER DEFAULT 8,  # ← shu qatorni qo'shing
streak INTEGER DEFAULT 0,
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                ism TEXT,
                sinf TEXT,
                ota_raqam TEXT,
                yonalish TEXT,
                kasb TEXT,
                streak INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                premium INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                day INTEGER,
                done_date TEXT,
                UNIQUE(telegram_id, day)
            )
        """)
        
async def save_user(telegram_id, ism, sinf, ota_raqam, yonalish, kasb, vazifa_vaqti=8):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO users 
            (telegram_id, ism, sinf, ota_raqam, yonalish, kasb, vazifa_vaqti)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (telegram_id, ism, sinf, ota_raqam, yonalish, kasb, vazifa_vaqti))
        await db.commit()
async def get_user(telegram_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        ) as cursor:
            return await cursor.fetchone()

async def get_all_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT telegram_id, ism FROM users") as cursor:
            return await cursor.fetchall()

async def get_done_days(telegram_id):
    """Bajarilgan kunlar ro'yxati, masalan: [1, 2, 3]"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT day FROM progress WHERE telegram_id = ? ORDER BY day", (telegram_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [r[0] for r in rows]

async def get_last_done_date(telegram_id):
    """Oxirgi vazifa bajarilgan sana (YYYY-MM-DD) yoki None"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT done_date FROM progress WHERE telegram_id = ? ORDER BY day DESC LIMIT 1",
            (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def mark_done(telegram_id, day):
    """Vazifani bajarilgan deb belgilash va streakni oshirish"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO progress (telegram_id, day, done_date) VALUES (?, ?, ?)",
            (telegram_id, day, str(date.today()))
        )
        await db.execute(
            "UPDATE users SET streak = streak + 1 WHERE telegram_id = ?", (telegram_id,)
        )
        await db.commit()

async def get_streak(telegram_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT streak FROM users WHERE telegram_id = ?", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

