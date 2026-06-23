async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_router)
    dp.include_router(tasks_router)
    await init_db()
    
    # Scheduler — apscheduler siz
    asyncio.create_task(vazifa_scheduler(bot))
    
    await dp.start_polling(bot)
from tasks import router as tasks_router
# dp ga qo'shing:
dp.include_router(tasks_router)

# main() ichiga:
scheduler = setup_scheduler(bot)
scheduler.start()
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

from start import router as start_router
# from tasks import router as tasks_router
from db import init_db

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    #  dp.include_router(tasks_router)

    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
