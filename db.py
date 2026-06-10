import aiosqlite

DB_PATH = "maqsadai.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
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
        await db.commit()

async def save_user(telegram_id, ism, sinf, ota_raqam, yonalish, kasb):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO users 
            (telegram_id, ism, sinf, ota_raqam, yonalish, kasb)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (telegram_id, ism, sinf, ota_raqam, yonalish, kasb))
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
