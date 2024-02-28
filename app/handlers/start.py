from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from app.keyboard.button import start_keyboard
from app.keyboard.inline import start_menu, menu_buttons
import random


dp = Dispatcher()




@dp.message(Command("start"))
async def protect(message: types.Message) -> None:
    num1 = random.randint(1, 11)
    num2 = random.randint(1, 11)
    correct_answer = num1 + num2
    buttons = [
        types.InlineKeyboardButton(text=str(random.randint(2, 21)), callback_data='numone'),
        types.InlineKeyboardButton(text=str(random.randint(2, 21)), callback_data='numtwo'),
        types.InlineKeyboardButton(text=str(random.randint(2, 21)), callback_data='numthree'),
    ]

    correct_position = random.randint(0, len(buttons))

    buttons.insert(correct_position, types.InlineKeyboardButton(text=str(correct_answer), callback_data="correct"))

    protect_buttons = [buttons]

    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=protect_buttons)
    await message.answer(text=f"🛡 Для запуска, надо пройти проверку безопасности. Сколько будет {num1} + {num2}?",
                         reply_markup=reply_markup)


@dp.callback_query(F.data == "correct")
async def start(callback: types.CallbackQuery):
    await callback.message.delete()
    keyboard = types.ReplyKeyboardMarkup(keyboard=start_keyboard, resize_keyboard=True)
    buttons = types.InlineKeyboardMarkup(inline_keyboard=start_menu)
    await callback.message.answer("🤖 Бот запущен 👍️", reply_markup=keyboard)
    await callback.message.answer('🍿 Привет, киноман!\n\n'
                                  '🔍 Для поиска используй кнопки ниже или напиши название мне',
                                  reply_markup=buttons)


@dp.message(F.text.lower() == "📖 меню")
async def menu(message: Message):
    buttons_menu = types.InlineKeyboardMarkup(inline_keyboard=menu_buttons)
    await message.answer(f"🆔 {message.from_user.id}\n🕔 Дата регистрации 23.02.24 20:43\n\n🍿 "
                         f"Приятного просмотра! 🍿", reply_markup=buttons_menu)


@dp.callback_query(lambda f: f.data in ["numone", "numtwo", "numthree"])
async def back(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Попробуй снова!")
    return await protect(callback.message)


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
