import asyncio

from aiogram import Bot, Dispatcher

from app.handler import db, router
from app.config import environment
from app.middleware import CheckDB

bot = Bot(environment["TELEGRAM"])
dp = Dispatcher()

router.message.middleware(CheckDB(db))
dp.include_router(router)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
