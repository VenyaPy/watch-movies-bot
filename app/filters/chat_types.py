from aiogram.filters import Filter
from aiogram import Bot, types
from app.database.models.users import SessionLocal
from app.database.requests.crud import show_admins


class SessionManager:
    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


class IsAdmin(Filter):
    async def __call__(self, message: types.Message, bot: Bot):
        with SessionManager() as db:
            try:
                admins = show_admins(db=db)
                is_admin = message.from_user.id in admins
            except Exception as e:
                print(f"Ошибка при доступе к базе данных: {e}")
                is_admin = False
            return is_admin
