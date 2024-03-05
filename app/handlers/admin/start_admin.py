from aiogram import types, Router, F
from aiogram.types import CallbackQuery, Message
from app.templates.keyboard.inline import admin_buttons
from app.filters.chat_types import IsAdmin
from aiogram.filters import Command

adm_router = Router()
adm_router.message.filter(IsAdmin())


@adm_router.message(Command('start_admin'))
async def admin_start(message: Message):
    user = message.from_user.first_name
    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=admin_buttons)
    await message.answer(f"👑 {user}, добро пожаловать в админ-меню!\n\nТвои функции👇",
                         reply_markup=reply_markup)


@adm_router.callback_query(F.data == 'back_admin')
async def back_adm(callback: CallbackQuery):
    user = callback.from_user.first_name
    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=admin_buttons)
    await callback.message.edit_text(f"👑 {user}, добро пожаловать в админ-меню!\n\nТвои функции👇",
                                     reply_markup=reply_markup)

