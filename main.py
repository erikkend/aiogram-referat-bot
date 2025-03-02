import os
import sys

import asyncio
import logging

from db import init_db
from handlers import menu_handlers, payment_handlers

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


load_dotenv()
TOKEN = os.getenv("TG_TOKEN")

dp = Dispatcher()
dp.include_router(menu_handlers.router)
dp.include_router(payment_handlers.router)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
