from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    CallbackQuery,
    InlineKeyboardButton
)
from app.database.models.users import SessionLocal
from app.filters.chat_types import IsAdmin
from app.templates.keyboard.inline import news_menu, back_admin
from app.handlers.admin.start_admin import back_adm
from app.database.requests.crud import get_user_id


class SessionManager:
    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()



post_router = Router()
post_router.message.filter(IsAdmin())
post_router.callback_query.filter(IsAdmin())


@post_router.callback_query(F.data == "newsletter")
async def newsletter_menu(callback: CallbackQuery):
    reply = InlineKeyboardMarkup(inline_keyboard=news_menu)
    await callback.message.answer(text="<b>📨 Меню постинга</b>\n\nТы можешь сделать рассылку пользователям 👇", reply_markup=reply)


class Form(StatesGroup):
    add_text = State()
    add_photo = State()
    add_button_text = State()
    add_button_url = State()
    done_post = State()
    send_post = State()


@post_router.callback_query(F.data == "add_post")
async def text_post(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await state.set_state(Form.add_text)
    await callback.message.answer(text="👇 Введите текст будущего поста 👇")


@post_router.message(Form.add_text)
async def process_text(message: Message, state: FSMContext) -> None:
    await state.update_data(add_text=message.text)
    await state.set_state(Form.add_photo)
    await message.answer("Теперь добавьте фото или видео к посту")


@post_router.message(Form.add_photo)
async def process_photo(message: Message, state: FSMContext) -> None:
    try:
        if message.photo:
            media_file_id = message.photo[-1].file_id
            media_type = 'photo'
        elif message.video:
            media_file_id = message.video.file_id
            media_type = 'video'
        else:
            await message.answer("Пожалуйста, отправьте фото или видео.")
            return

        await state.update_data(add_media=media_file_id, media_type=media_type)
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
    await message.answer(text="Напиши ГОТОВО для просмотра поста 👇")


@post_router.message(Form.done_post)
async def finish_post_creation(message: Message, state: FSMContext) -> None:
    if F.text.lower() == "ГОТОВО":
        data = await state.get_data()
        add_text = data.get("add_text", "")
        add_media = data.get("add_media", "")
        media_type = data.get("media_type", "")
        add_button_text = data.get("add_button_text", "")
        add_button_url = data.get("add_button_url", "")

        button = [
            [InlineKeyboardButton(text=add_button_text, url=add_button_url)]
        ]


        post_data = {
            "text": add_text,
            "photo": add_media,
            "button": button
        }

        await state.update_data(final_post=post_data)
        reply = InlineKeyboardMarkup(inline_keyboard=button)
        if media_type == 'photo':
            await message.answer_photo(photo=add_media, caption=add_text, reply_markup=reply)
        elif media_type == 'video':
            await message.answer_video(video=add_media, caption=add_text, reply_markup=reply)
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
async def cancel_handler(callback: CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    try:
        await state.clear()
        baki = InlineKeyboardMarkup(inline_keyboard=back_admin)
        await callback.message.answer(
            "Пост удален",
            reply_markup=baki
        )
    except Exception as e:
        print(e)


@post_router.callback_query(F.data == 'send_post')
async def send_post(callback: CallbackQuery, state: FSMContext) -> None:
    if F.data == 'send_post':
        data = await state.get_data()
        add_text = data.get("add_text", "")
        add_media = data.get("add_media", "")
        media_type = data.get("media_type", "")
        add_button_text = data.get("add_button_text", "")
        add_button_url = data.get("add_button_url", "")

        button = [
            [InlineKeyboardButton(text=add_button_text, url=add_button_url)]
        ]
        reply = InlineKeyboardMarkup(inline_keyboard=button)

        post_data = {
            "text": add_text,
            "photo": add_media,
            "button": button
        }

        await state.update_data(final_post=post_data)

        with SessionManager() as db:
            user_ids = get_user_id(db=db)

        for ids in user_ids:
            if media_type == 'photo':
                await callback.bot.send_photo(chat_id=ids, photo=add_media, caption=add_text, reply_markup=reply)
            elif media_type == 'video':
                await callback.bot.send_video(chat_id=ids, video=add_media, caption=add_text, reply_markup=reply)

        await state.clear()
        return await back_adm(callback)




