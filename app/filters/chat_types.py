from aiogram.filters import Filter
from aiogram import Bot, types
from app.database.models.users import SessionLocal
from app.database.requests.crud import show_admins



class IsAdmin(Filter):
    async def __call__(self, message: types.Message, bot: Bot):
        db = SessionLocal()
        try:
            admins = show_admins(db=db)
            is_admin = message.from_user.id in admins
        except Exception as e:
            print(f"Ошибка при доступе к базе данных: {e}")
            is_admin = False
        finally:
            db.close()
        return is_admin
