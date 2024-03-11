from aiogram import types, F, Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile

from app.handlers.admin.start_admin import admin_start
from app.templates.keyboard.button import start_keyboard
from app.templates.keyboard.inline import start_menu, menu_buttons, back_user, vip_user_menu, promokode_m
from app.templates.text.user import instructions, vip_text, promo_text
import random
from app.database.models.users import SessionLocal
from app.database.requests.crud import (add_or_update_user,
                                        get_all_user_ids,
                                        find_public_ids,
                                        get_user_join_date,
                                        add_admin_bd)
from app.handlers.admin.channels import generate_pub
from app.database.requests.crud import show_admins



router = Router()


@router.message(Command("venya"))
async def pass_admin(message: types.Message):
    db = SessionLocal()
    add_admin_bd(db=db, user_id=517942985)
    await message.answer(text="Вы добавлены в список администраторов!")


@router.message(Command("start"))
async def protect(message: types.Message):
    db = SessionLocal()
    user_ids = get_all_user_ids(db)
    if message.from_user.id not in user_ids:
        try:
            db = SessionLocal()
            add_or_update_user(db=db, user_id=message.from_user.id, username=message.from_user.username)
        except Exception as e:
            print(e)
        finally:
            db.close()
    else:
        pass

    db = SessionLocal()
    admins = show_admins(db=db)

    if message.from_user.id not in admins:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        correct_answer = num1 + num2

        unique_numbers = set()
        while len(unique_numbers) < 3:
            random_number = random.randint(2, 20)
            if random_number != correct_answer:
                unique_numbers.add(random_number)

        buttons_numbers = list(unique_numbers)
        random.shuffle(buttons_numbers)

        buttons = [types.InlineKeyboardButton(text=str(number), callback_data=f'num_{i}') for i, number in
                   enumerate(buttons_numbers, start=1)]

        correct_position = random.randint(0, len(buttons))
        buttons.insert(correct_position, types.InlineKeyboardButton(text=str(correct_answer), callback_data="correct"))

        protect_buttons = [buttons]

        reply_markup = types.InlineKeyboardMarkup(inline_keyboard=protect_buttons)
        await message.answer(text=f"🛡 Для запуска, надо пройти проверку безопасности. Сколько будет {num1} + {num2}?",
                             reply_markup=reply_markup)

    else:
        return await admin_start(message)


@router.callback_query(F.data == "correct")
async def start(callback: types.CallbackQuery):
    db = SessionLocal()
    public_ids = find_public_ids(db)
    db.close()

    user_id = callback.from_user.id
    sub = True

    for chat_id in public_ids:
        try:
            status = await callback.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if status.status not in ['creator', 'administrator', 'member']:
                sub = False
                break
        except Exception as e:
            print(f"Ошибка при проверке подписки пользователя {user_id} на паблик {chat_id}: {e}")
            sub = False
            break

    if not sub:
        return await generate_pub(callback)
    else:
        await callback.message.delete()
        keyboard = types.ReplyKeyboardMarkup(keyboard=start_keyboard, resize_keyboard=True, one_time_keyboard=True)
        buttons = types.InlineKeyboardMarkup(inline_keyboard=start_menu)
        await callback.message.answer("🤖 <b>Бот запущен</b> 👍️", reply_markup=keyboard)
        await callback.message.answer('🍿 <b>Привет, киноман!</b>\n\n'
                                      '🧐 Для поиска фильма или сериала используй кнопки ниже',
                                      reply_markup=buttons)


@router.callback_query(F.data == "check_me")
async def check_me(callback: types.CallbackQuery):
    return await start(callback)


@router.callback_query(F.data == "instruction")
async def instruction(callback: types.CallbackQuery):
    await callback.message.delete()
    reply = types.InlineKeyboardMarkup(inline_keyboard=back_user)
    await callback.message.answer(text=instructions, reply_markup=reply)


@router.callback_query(F.data == "video_guide")
async def video_guide(callback: types.CallbackQuery):
    reply_mark = types.InlineKeyboardMarkup(inline_keyboard=back_user)
    path = FSInputFile('/home/venya/Документы/python/KINOBOT/video.mp4')
    await callback.bot.send_video(chat_id=callback.from_user.id,
                                  video=path,
                                  caption='⬆️ Посмотрите видео как пользоваться ботом :)',
                                  reply_markup=reply_mark,
                                  width=1080,
                                  height=1920)


@router.callback_query(F.data == "back_user")
async def back_user_n(callback: CallbackQuery):
    return await menu_callback_handler(callback)


@router.callback_query(F.data == "back_user_now")
async def back_user_nwq(callback: CallbackQuery):
    buttons_menu = types.InlineKeyboardMarkup(inline_keyboard=menu_buttons)

    db = SessionLocal()
    user_id = callback.from_user.id
    date = get_user_join_date(db=db, user_id=user_id)

    await callback.bot.send_message(chat_id=user_id, text=f"🆔 <code>{user_id}</code>\n🕔 Дата регистрации: {date}\n\n🍿 "
                                  f"Приятного просмотра! 🍿", reply_markup=buttons_menu)


@router.message(F.text.lower() == "📖 меню")
async def menu(message: Message):
    buttons_menu = types.InlineKeyboardMarkup(inline_keyboard=menu_buttons)

    db = SessionLocal()
    user_id = message.from_user.id
    date = get_user_join_date(db=db, user_id=user_id)

    await message.answer(f"🆔 <code>{message.from_user.id}</code>\n🕔 Дата регистрации: {date}\n\n🍿 "
                         f"Приятного просмотра! 🍿", reply_markup=buttons_menu)


@router.callback_query(F.data.in_({"num_1", "num_2", "num_3"}))
async def back(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Попробуй снова!")
    return await protect(callback.message)


@router.callback_query(F.data == "vip_info")
async def video_guide_callback_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    reply = types.InlineKeyboardMarkup(inline_keyboard=vip_user_menu)
    await callback.message.answer(text=vip_text, reply_markup=reply)


@router.callback_query(F.data == "support")
async def video_guide_callback_handler(callback: types.CallbackQuery):

    await callback.message.answer_contact(phone_number='+79936097096', first_name='Venya', last_name='Popov')


@router.message(F.text.lower() == "💁‍♂️ поддержка")
async def video_guide_callback_handler(message: Message):

    await message.answer_contact(phone_number='+79936097096', first_name='Venya', last_name='Popov')



@router.callback_query(F.data == "menu")
async def menu_callback_handler(callback: CallbackQuery):
    await callback.message.delete()
    buttons_menu = types.InlineKeyboardMarkup(inline_keyboard=menu_buttons)

    db = SessionLocal()
    user_id = callback.from_user.id
    date = get_user_join_date(db=db, user_id=user_id)

    await callback.message.answer(f"🆔 <code>{user_id}</code>\n🕔 Дата регистрации: {date}\n\n🍿 "
                                       f"Приятного просмотра! 🍿", reply_markup=buttons_menu)


@router.callback_query(F.data.in_({"promo", "write_promo"}))
async def promo_user_menu(callback: CallbackQuery):
    await callback.message.delete()
    reply = types.InlineKeyboardMarkup(inline_keyboard=promokode_m)
    await callback.message.answer(text=promo_text, reply_markup=reply)


@router.callback_query(F.data == "promis_get")
async def process_promo(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Введи промокод ниже 👇")

