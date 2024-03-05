from aiogram import Bot, F, Router
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    CallbackQuery,
    InlineKeyboardButton
)
from app.database.requests.crud import find_user
from app.templates.keyboard.inline import stat
from app.database.database import SessionLocal
from app.filters.chat_types import IsAdmin


stat_router = Router()
stat_router.message.filter(IsAdmin())


@stat_router.callback_query(F.data == 'statistics')
async def statistic(callback: CallbackQuery):
    await callback.message.delete()
    reply_mark = InlineKeyboardMarkup(inline_keyboard=stat)
    await callback.message.answer(text='Добро пожаловать в меню статистики:',
                                  reply_markup=reply_mark)


@stat_router.callback_query(F.data == 'users')
async def show_users(callback: CallbackQuery):
    await callback.message.delete()
    user = find_user(db=SessionLocal())
    users_text = "\n".join(user)
    await callback.message.answer(text=users_text)
