from aiogram import Bot, F, Router
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
from app.handlers.admin.start_admin import admin_start
from app.database.requests.crud import find_user


post_router = Router()
post_router.message.filter(IsAdmin())


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


@post_router.callback_query(F.data == "add_post")
async def text_post(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.add_text)
    await message.answer(text="Введите текст будущего поста")


@post_router.message(Form.add_text)
async def process_text(message: Message, state: FSMContext) -> None:
    await state.update_data(add_text=message.text)
    await state.set_state(Form.add_photo)
    await message.answer("Теперь добавьте фото к посту")


@post_router.message(Form.add_photo, F.photo)
async def process_photo(message: Message, state: FSMContext) -> None:
    photo_file_id = message.photo[-1].file_id
    await state.update_data(add_photo=photo_file_id)
    await state.set_state(Form.add_button_text)
    await message.answer('Добавьте текст для кнопки')


@post_router.message(Form.add_button_text)
async def process_button_text(message: Message, state: FSMContext) -> None:
    await state.update_data(add_button_text=message.text)
    await state.set_state(Form.add_button_url)
    await message.answer('Добавьте URL для ссылки')


@post_router.message(Form.add_button_url)
async def process_button_url(message: Message, state: FSMContext) -> None:
    await state.update_data(add_button_url=message.text)
    # Предлагаем пользователю завершить создание поста
    await message.answer('Пост готов к публикации. Нажмите "Завершить", чтобы продолжить.',
                          reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                              [InlineKeyboardButton(text="Завершить", callback_data="finish_post_creation")]
                          ]))


@post_router.callback_query(F.data == "finish_post_creation")
async def finish_post_creation(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.done_post)
    # Вызываем функцию для генерации поста или предоставляем пользователю следующие инструкции
    await generate_post(callback_query.message, state)


@post_router.message(Form.done_post)
async def generate_post(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    add_text = data.get("add_text", "")
    add_photo = data.get("add_photo", [])
    add_button_text = data.get("add_button_text", "")
    add_button_url = data.get("add_button_url", "")

    button = [
        [InlineKeyboardButton(text=add_button_text, url=add_button_url)]
    ]

    post_data = {
        "text": add_text,
        "photo": add_photo[-1] if add_photo else None,  # предполагаем, что photo это список ID фото, берем последнее
        "button": button
    }

    await state.update_data(final_post=post_data)
    reply = InlineKeyboardMarkup(inline_keyboard=news_menu)
    await message.answer(text='Удалить, Просмотреть, либо Отправить пост?', reply_markup=reply)


@post_router.callback_query(F.data == 'del_post')
async def delete_post(message: Message, state: FSMContext) -> None:
    await state.get_data()
    await state.clear()
    return await admin_start(message)


@post_router.callback_query(F.data == 'send_post')
async def send_post(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    final_post = data.get('final_post')

    user_ids = find_user(db=SessionLocal())

    for user_id in user_ids:
        if final_post.get('photo'):
            button = InlineKeyboardMarkup(inline_keyboard=final_post['button'])
            await callback_query.message.bot.send_photo(chat_id=user_id,
                                                        photo=final_post['photo'],
                                                        caption=final_post['text'],
                                                        reply_markup=button)
        else:
            button = InlineKeyboardMarkup(inline_keyboard=final_post['button'])
            await callback_query.message.bot.send_message(chat_id=user_id,
                                                          text=final_post['text'],
                                                          reply_markup=button)

    await state.clear()


@post_router.callback_query(F.data == 'show_post')
async def post(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    final_post = data.get('final_post')

    if final_post and 'photo' in final_post:
        button = InlineKeyboardMarkup(inline_keyboard=final_post['button'])
        await callback_query.message.bot.send_photo(chat_id=callback_query.from_user.id,
                                                    photo=final_post['photo'],
                                                    caption=final_post['text'],
                                                    reply_markup=button)
    elif final_post:
        button = InlineKeyboardMarkup(inline_keyboard=final_post['button'])
        await callback_query.message.bot.send_message(chat_id=callback_query.from_user.id,
                                                      text=final_post['text'],
                                                      reply_markup=button)
    else:
        # Если final_post не найден, отправляем сообщение об ошибке
        await callback_query.answer('Пост не найден.', show_alert=True)
