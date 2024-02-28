import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import token_bot
from app.handlers.user import start
from app.handlers.admin import start_admin

TOKEN = token_bot
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

dp = Dispatcher()

dp.include_routers(start.router, start_admin.router)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())