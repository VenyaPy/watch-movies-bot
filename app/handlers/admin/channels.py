from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    CallbackQuery,
    InlineKeyboardButton
)
from app.templates.keyboard.inline import public_buttons, back_admin
from app.database.models.users import SessionLocal
from app.database.requests.crud import add_public, find_public, delete_all_publics, get_public_count
from app.handlers.admin.start_admin import admin_start
from app.filters.chat_types import IsAdmin


pub_router = Router()
pub_router.message.filter(IsAdmin())
pub_router.callback_query.filter(IsAdmin())

form_router = Router()
form_router.message.filter(IsAdmin())
form_router.callback_query.filter(IsAdmin())


class SessionManager:
    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


@form_router.callback_query(F.data == 'active_pub')
async def generate_pub(callback: CallbackQuery):
    await callback.message.delete()

    with SessionManager() as db:
        public_urls = find_public(db=db)

    if public_urls:
        keyboard_publics = [
                [InlineKeyboardButton(text="Подпишись👈", url=url)]
                for url in public_urls
            ]
        keyboard_publics.append([InlineKeyboardButton(text="Проверить подписку", callback_data='check_me')])
        buttons = InlineKeyboardMarkup(inline_keyboard=keyboard_publics)
        await callback.message.answer('⚠️ Пожалуйста, подпишитесь на все паблики для использования бота.',
                                      reply_markup=buttons)
    else:
        await callback.message.answer("Извините, у вас ещё нет пабликов")


@form_router.callback_query(F.data == "back")
async def back(callback: CallbackQuery, message):
    await callback.message.delete()
    return await admin_start(message)


@form_router.callback_query(F.data == 'delete_pub')
async def delete_pub(callback: CallbackQuery):
    with SessionManager() as db:
        delete_all_publics(db=db)
    await callback.message.answer("Все паблики успешно удалены!")


class Form(StatesGroup):
    id_pub = State()
    url_pub = State()
    done = State()


@form_router.callback_query(F.data == 'channels')
async def public(callback: CallbackQuery):
    await callback.message.delete()

    with SessionManager() as db:
        publics = get_public_count(db=db)

    reply_markup = InlineKeyboardMarkup(inline_keyboard=public_buttons)
    await callback.message.answer(text=f'🤖 Всего пабликов добавлено: {publics}\n\nУправление👇',
                         reply_markup=reply_markup)


@form_router.callback_query(F.data == 'add_pub')
async def begin_add(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.id_pub)
    await callback.message.answer(text="Введите ID паблика")


@form_router.message(Form.id_pub)
async def process_id(message: Message, state: FSMContext) -> None:
    await state.update_data(id_pub=message.text)
    await state.set_state(Form.url_pub)
    await message.answer("Теперь введите URL паблика")


@form_router.message(Form.url_pub)
async def process_url(message: Message, state: FSMContext) -> None:
    await state.update_data(url_pub=message.text)
    await state.set_state(Form.done)
    await message.answer(text='Введите "ГОТОВО" для добавления паблика')


@form_router.message(Form.done)
async def process_done(message: Message, state: FSMContext) -> None:
    if message.text.lower() == "готово":
        user_data = await state.get_data()
        id_pub = int(user_data['id_pub'])
        url_pub = user_data['url_pub']

        with SessionManager() as db:
            add_public(db=db, id_pub=id_pub, url_pub=url_pub)

        await state.clear()

        reply = InlineKeyboardMarkup(inline_keyboard=back_admin)
        await message.answer("Спасибо. Паблик добавлен.", reply_markup=reply)








