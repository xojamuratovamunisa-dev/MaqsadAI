import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

from start import router as start_router
from tasks import router as tasks_router, barcha_userlarga_vazifa
from db import init_db

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

async def vazifa_scheduler(bot: Bot):
    while True:
        await asyncio.sleep(60)  # Har daqiqada tekshiradi
        try:
            await barcha_userlarga_vazifa(bot)
        except Exception as e:
            print(f"Scheduler xato: {e}")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(tasks_router)

    await init_db()

    # Polling bilan birga scheduler ishlasin
    await asyncio.gather(
        dp.start_polling(bot),
        vazifa_scheduler(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
