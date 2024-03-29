import os
from aiogram import F, Router
from aiogram.types import (
    InlineKeyboardMarkup,
    CallbackQuery,
    FSInputFile
)
from app.database.requests.crud import find_user, get_user_count
from app.templates.keyboard.inline import stat
from app.database.models.users import SessionLocal
from app.filters.chat_types import IsAdmin


stat_router = Router()
stat_router.message.filter(IsAdmin())
stat_router.callback_query.filter(IsAdmin())


class SessionManager:
    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


@stat_router.callback_query(F.data == 'statistics')
async def statistic(callback: CallbackQuery):
    await callback.message.delete()
    reply_mark = InlineKeyboardMarkup(inline_keyboard=stat)
    with SessionManager() as db:
        count_user = get_user_count(db=db)
    await callback.message.answer(text=f'👥 Всего пользователей: {count_user}\n\n💻 Нагрузка сервера: -'
                                       f'\n💿 Процессор: -\n💾 Оперативная память: -',
                                  reply_markup=reply_mark)


@stat_router.callback_query(F.data == 'users')
async def show_users(callback_query: CallbackQuery):

    user = find_user(db=SessionLocal())
    users_text = "\n".join(user)

    temp_file_path = "users_list.txt"
    with open(temp_file_path, "w") as file:
        file.write(users_text)

    await callback_query.bot.send_document(
        chat_id=callback_query.from_user.id,
        document=FSInputFile(path=temp_file_path, filename="Список пользователей.txt")
    )

    os.remove(temp_file_path)
