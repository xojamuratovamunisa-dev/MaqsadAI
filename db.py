import aiosqlite
from datetime import date

DB_PATH = "maqsadai.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                ism TEXT,
                sinf TEXT,
                ota_raqam TEXT,
                yonalish TEXT,
                kasb TEXT,
                vazifa_vaqti INTEGER DEFAULT 8,
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
        await db.commit()


async def save_user(telegram_id, ism, sinf, ota_raqam, yonalish, kasb, vazifa_vaqti=8):
    """
    Yangi foydalanuvchi qo'shadi yoki mavjudini yangilaydi.
    streak, level, premium kabi maydonlarga tegmaydi.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (telegram_id, ism, sinf, ota_raqam, yonalish, kasb, vazifa_vaqti)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                ism         = excluded.ism,
                sinf        = excluded.sinf,
                ota_raqam   = excluded.ota_raqam,
                yonalish    = excluded.yonalish,
                kasb        = excluded.kasb,
                vazifa_vaqti = excluded.vazifa_vaqti
        """, (telegram_id, ism, sinf, ota_raqam, yonalish, kasb, vazifa_vaqti))
        await db.commit()


async def get_user(telegram_id):
    """
    Foydalanuvchini dict ko'rinishida qaytaradi.
    Topilmasa None qaytaradi.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def get_all_users():
    """Barcha foydalanuvchilarning telegram_id va ismini qaytaradi."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT telegram_id, ism FROM users") as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]


async def get_done_days(telegram_id):
    """Foydalanuvchi bajargan kunlar ro'yxatini qaytaradi."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT day FROM progress WHERE telegram_id = ? ORDER BY day",
            (telegram_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [r[0] for r in rows]


async def get_last_done_date(telegram_id):
    """Foydalanuvchi eng oxirgi vazifani bajargan sanani qaytaradi."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT done_date FROM progress WHERE telegram_id = ? ORDER BY day DESC LIMIT 1",
            (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def mark_done(telegram_id, day):
    """
    Kunni bajarilgan deb belgilaydi.
    Streak faqat yangi kun qo'shilganda oshadi (duplicate bo'lsa oshmaydi).
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT OR IGNORE INTO progress (telegram_id, day, done_date) VALUES (?, ?, ?)",
            (telegram_id, day, str(date.today()))
        )
        # Faqat yangi qator kiritilganda streak oshsin
        if cursor.rowcount > 0:
            await db.execute(
                "UPDATE users SET streak = streak + 1 WHERE telegram_id = ?",
                (telegram_id,)
            )
        await db.commit()


async def get_streak(telegram_id):
    """Foydalanuvchining joriy streak sonini qaytaradi."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT streak FROM users WHERE telegram_id = ?", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


async def reset_streak(telegram_id):
    """Foydalanuvchi streakini nolga tushiradi (kun o'tkazib yuborilganda)."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET streak = 0 WHERE telegram_id = ?", (telegram_id,)
        )
        await db.commit()


async def update_level(telegram_id, level):
    """Foydalanuvchi levelini yangilaydi."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET level = ? WHERE telegram_id = ?", (level, telegram_id)
        )
        await db.commit()


async def set_premium(telegram_id, status: bool):
    """Foydalanuvchiga premium beradi yoki olib qo'yadi."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET premium = ? WHERE telegram_id = ?",
            (1 if status else 0, telegram_id)
        )
        await db.commit()
