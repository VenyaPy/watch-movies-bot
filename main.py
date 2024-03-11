import asyncio
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import token_bot
from app.handlers.user import start, payment
from app.handlers.admin import (start_admin,
                                channels,
                                statistic,
                                newsletter,
                                permissions)
from app.utils.cdn import cdn


TOKEN = token_bot
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

dp = Dispatcher()

dp.include_routers(start.router,
                   channels.pub_router,
                   channels.form_router,
                   start_admin.adm_router,
                   statistic.stat_router,
                   newsletter.post_router,
                   permissions.per_router,
                   cdn.cdn_rou,
                   payment.pay)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

