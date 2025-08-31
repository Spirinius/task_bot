from typing import Final
import asyncio
from taskdb import Tasks, db_init

from aiogram import Dispatcher, Bot

from tg_handlers import router

from const import TOKEN

TOKEN = Bot(TOKEN)
dp = Dispatcher()

async def main():
    await db_init()

    dp.include_router(router)
    await dp.start_polling(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())