from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.handlers.admin.start_admin import admin_start
from app.templates.keyboard import start_keyboard
from app.templates.keyboard.inline import start_menu, menu_buttons
import random
from config import admins
from datetime import datetime

router = Router()

@router.message(Command("start"))
async def protect(message: types.Message):
    if message.from_user.id not in admins:
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

    else:
        return await admin_start(message)


@router.callback_query(F.data == "correct")
async def start(callback: types.CallbackQuery):
    await callback.message.delete()
    keyboard = types.ReplyKeyboardMarkup(keyboard=start_keyboard, resize_keyboard=True)
    buttons = types.InlineKeyboardMarkup(inline_keyboard=start_menu)
    await callback.message.answer("🤖 Бот запущен 👍️", reply_markup=keyboard)
    await callback.message.answer('🍿 Привет, киноман!\n\n'
                                  '🔍 Для поиска используй кнопки ниже или напиши название мне',
                                  reply_markup=buttons)


@router.message(F.text.lower() == "📖 меню")
async def menu(message: Message):
    buttons_menu = types.InlineKeyboardMarkup(inline_keyboard=menu_buttons)
    date = datetime.now().strftime('%d.%m.%Y %H:%M')
    await message.answer(f"🆔 {message.from_user.id}\n🕔 Дата регистрации {date}\n\n🍿 "
                         f"Приятного просмотра! 🍿", reply_markup=buttons_menu)


@router.callback_query(F.data.in_({"numone", "numtwo", "numthree"}))
async def back(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Попробуй снова!")
    return await protect(callback.message)


@router.message(F.text.lower() == "⚙️ фильтр")
async def filters(message: Message):
    await message.answer("В разработке...")


@router.callback_query(F.data == "video_guide")
async def video_guide_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer('Принято')


@router.callback_query(F.data == "menu")
async def menu_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer('Принято')


@router.callback_query(F.data == "search")
async def search_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer('Принято')
