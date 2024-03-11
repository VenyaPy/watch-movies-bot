from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.filters.chat_types import IsAdmin
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from app.database.models.users import SessionLocal
from app.database.requests.crud import add_admin_bd, show_admins, del_admins_bd

from app.templates.keyboard.inline import l_add_admin, add_admin_b, add_vip, back_admin


per_router = Router()
per_router.message.filter(IsAdmin())
per_router.callback_query.filter(IsAdmin())


class SessionManager:
    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


@per_router.callback_query(F.data == "list_admins")
async def list_admins(callback: CallbackQuery):
    await callback.message.delete()
    with SessionManager() as db:
        try:
            admins_ids = show_admins(db=db)
            str_admins = '\n'.join(str(admins_id) for admins_id in admins_ids)
            reply_markup = InlineKeyboardMarkup(inline_keyboard=back_admin)
            await callback.message.answer(text=str_admins, reply_markup=reply_markup)
        except Exception as e:
            await callback.message.answer(text=f"Произошла ошибка {e}")


class FormDel(StatesGroup):
    id_admin_delete = State()
    done_delete = State()


@per_router.callback_query(F.data == "del_admin")
async def delete_admin_id(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(text="Введите ID администратора для удаления 👇")
    await state.set_state(FormDel.id_admin_delete)


@per_router.message(FormDel.id_admin_delete)
async def process_id(message: Message, state: FSMContext) -> None:
    await state.update_data(id_admin_delete=message.text)
    await state.set_state(FormDel.done_delete)
    await message.answer("Введите слово ПОДТВЕРДИТЬ для удаления")


@per_router.message(FormDel.done_delete)
async def process_done(message: Message, state: FSMContext) -> None:
    if F.text.lower() == "подтвердить":
        try:
            user_data = await state.get_data()
            user_id = int(user_data['id_admin_delete'])

            with SessionManager() as db:
                del_admins_bd(db=db, user_id=user_id)

            await message.answer(text=f"Администратор {user_id} успешно удалён")
            await state.clear()
        except Exception as e:
            await message.answer(f"Ошибка удаления: {e}")
            await state.clear()


@per_router.callback_query(F.data == "admins")
async def l_per_menu(callback: CallbackQuery):
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=l_add_admin)
    await callback.message.answer(text="Выберите меню для управления:", reply_markup=reply_markup)


@per_router.callback_query(F.data == "m_admins")
async def l_menu_admin(callback: CallbackQuery):
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=add_admin_b)
    await callback.message.answer(text="Управление администраторами:", reply_markup=reply_markup)


class Form(StatesGroup):
    id_admin = State()
    add = State()


@per_router.callback_query(F.data == "add_admin")
async def add_admin(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.id_admin)
    await callback.message.answer(text="Введите ID администратора, которого хотите добавить 👇")


@per_router.message(Form.id_admin)
async def set_id_admin(message: Message, state: FSMContext) -> None:
    await state.update_data(id_admin=message.text)
    await state.set_state(Form.add)
    await message.answer(text="Введите ПОДТВЕРДИТЬ для добавления администратора")


@per_router.message(Form.add)
async def bd_admin(message: Message, state: FSMContext) -> None:
    if F.text.lower() == "подтвердить":
        try:
            user_data = await state.get_data()
            user_id = int(user_data['id_admin'])

            with SessionManager() as db:
                add_admin_bd(db=db, user_id=user_id)
            reply_markup = InlineKeyboardMarkup(inline_keyboard=back_admin)
            await message.answer(text=f"Спасибо!\n\nАдминистратор {user_id} добавлен!", reply_markup=reply_markup)
            await state.clear()
        except Exception:
            await message.answer(text="Не удалось добавить администратора")
            await state.clear()




