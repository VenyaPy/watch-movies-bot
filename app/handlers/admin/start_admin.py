from aiogram import types, Router
from app.templates.keyboard.inline import admin_buttons

router = Router()


@router.message()
async def admin_start(message: types):
    user = message.from_user.first_name
    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=admin_buttons)
    await message.answer(f"👑 {user}, добро пожаловать в админ-меню!\n\nТвои функции👇",
                         reply_markup=reply_markup)
