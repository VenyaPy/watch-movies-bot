from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    CallbackQuery,
    InlineKeyboardButton
)
from app.database.database import SessionLocal
from app.filters.chat_types import IsAdmin
from app.templates.keyboard.inline import news_menu
from app.database.requests.crud import get_user_id
import logging



logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")


post_router = Router()
post_router.message.filter(IsAdmin())
post_router.callback_query.filter(IsAdmin())


@post_router.callback_query(F.data == "newsletter")
async def newsletter_menu(callback: CallbackQuery):
    reply = InlineKeyboardMarkup(inline_keyboard=news_menu)
    await callback.message.answer(text="МЕНЮ ПОСТИНГА", reply_markup=reply)


class Form(StatesGroup):
    add_text = State()
    add_photo = State()
    add_button_text = State()
    add_button_url = State()
    done_post = State()
    send_post = State()


@post_router.callback_query(F.data == "add_post")
async def text_post(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.add_text)
    await message.answer(text="👇 Введите текст будущего поста 👇")


@post_router.message(Form.add_text)
async def process_text(message: Message, state: FSMContext) -> None:
    await state.update_data(add_text=message.text)
    await state.set_state(Form.add_photo)
    await message.answer("Теперь добавьте фото к посту")


@post_router.message(Form.add_photo, F.photo)
async def process_photo(message: Message, state: FSMContext) -> None:
    try:
        photo_file_id = message.photo[-1].file_id
        await state.update_data(add_photo=photo_file_id)
        await state.set_state(Form.add_button_text)
        await message.answer('Добавьте текст для кнопки')
    except Exception as e:
        print(e)


@post_router.message(Form.add_button_text)
async def process_button_text(message: Message, state: FSMContext) -> None:
    await state.update_data(add_button_text=message.text)
    await state.set_state(Form.add_button_url)
    await message.answer('Добавьте URL для ссылки')


@post_router.message(Form.add_button_url)
async def process_button_url(message: Message, state: FSMContext) -> None:
    await state.update_data(add_button_url=message.text)
    await state.set_state(Form.done_post)
    don = [
        [
            InlineKeyboardButton(text='Завершить', callback_data='goto')
        ]
    ]
    brake = InlineKeyboardMarkup(inline_keyboard=don)
    await message.answer(text="Нажми для завершения 👇",
                         reply_markup=brake)


@post_router.message(Form.done_post)
async def finish_post_creation(message: Message, state: FSMContext) -> None:
    if F.data == "goto":
        data = await state.get_data()
        add_text = data.get("add_text", "")
        add_photo = data.get("add_photo", "")
        add_button_text = data.get("add_button_text", "")
        add_button_url = data.get("add_button_url", "")

        button = [
            [InlineKeyboardButton(text=add_button_text, url=add_button_url)]
        ]

        post_data = {
            "text": add_text,
            "photo": add_photo,
            "button": button
        }

        await state.update_data(final_post=post_data)
        reply = InlineKeyboardMarkup(inline_keyboard=button)
        await message.answer_photo(photo=add_photo, caption=add_text, reply_markup=reply)
        done_button = [
            [
                InlineKeyboardButton(text='🚀 Отправить пост', callback_data='send_post')
            ],
            [
                InlineKeyboardButton(text='⛔ Удалить пост', callback_data='del_post')
            ]
        ]
        done_b = InlineKeyboardMarkup(inline_keyboard=done_button)
        await message.answer(text="Что делаем с постом?", reply_markup=done_b)
        await state.set_state(Form.send_post)


@post_router.callback_query(F.data == 'del_post')
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    try:
        await state.clear()
        await message.answer(
            "Пост удален"
        )
    except Exception as e:
        print(e)

@post_router.callback_query(F.data == 'send_post')
async def send_post(message: Message, state: FSMContext) -> None:
    if F.data == 'send_post':
        data = await state.get_data()
        add_text = data.get("add_text", "")
        add_photo = data.get("add_photo", "")
        add_button_text = data.get("add_button_text", "")
        add_button_url = data.get("add_button_url", "")

        button = [
            [InlineKeyboardButton(text=add_button_text, url=add_button_url)]
        ]

        post_data = {
            "text": add_text,
            "photo": add_photo,
            "button": button
        }

        await state.update_data(final_post=post_data)

        db = SessionLocal()
        user_ids = get_user_id(db=db)

        for ids in user_ids:
            reply = InlineKeyboardMarkup(inline_keyboard=button)
            await message.bot.send_photo(chat_id=ids, photo=add_photo, caption=add_text, reply_markup=reply)
        await message.answer('✅ Пост успешно отправлен.')



