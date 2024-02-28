import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.enums import ParseMode

from app.handlers.start import dp
from config import token_bot

TOKEN = token_bot
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())