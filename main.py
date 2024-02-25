import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from config import token_bot
from app.keyboard.button import start_keyboard
from app.keyboard.inline import start_menu, menu_buttons

TOKEN = token_bot
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message(Command("start"))
async def command_start_handler(message: Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=start_keyboard, resize_keyboard=True)
    buttons = types.InlineKeyboardMarkup(inline_keyboard=start_menu)
    await message.answer("🤖 Бот запущен 👍️", reply_markup=keyboard)
    await message.answer('🍿 Привет, киноман!\n\n'
                         '🔍 Для поиска используй кнопки ниже или напиши название мне',
                         reply_markup=buttons)


@dp.message(F.text.lower() == "📖 меню")
async def menu(message: Message):
    buttons_menu = types.InlineKeyboardMarkup(inline_keyboard=menu_buttons)
    await message.answer(f"🆔 {message.from_user.id}\n🕔 Дата регистрации 23.02.24 20:43\n\n🍿 "
                         f"Приятного просмотра! 🍿", reply_markup=buttons_menu)


@dp.message(F.text.lower() == "⚙️ фильтр")
async def filters(message: Message):
    await message.answer("В разработке...")


@dp.callback_query(F.data == "video_guide")
async def video_guide_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer('Принято')


@dp.callback_query(F.data == "menu")
async def menu_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer('Принято')


@dp.callback_query(F.data == "search")
async def search_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer('Принято')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())