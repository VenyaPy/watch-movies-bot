from aiogram.filters import Filter
from aiogram import Bot, types
from config import admins


class IsAdmin(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: types.Message, bot: Bot):
        return message.from_user.id in admins
