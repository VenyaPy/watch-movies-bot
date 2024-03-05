from aiogram import types, F, Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message

from app.handlers.admin.start_admin import admin_start
from app.templates.keyboard.button import start_keyboard
from app.templates.keyboard.inline import start_menu, menu_buttons
from app.templates.text.user import instructions
import random
from datetime import datetime
import aiohttp
from app.database.database import SessionLocal
from app.database.requests.crud import add_or_update_user, get_all_user_ids, find_public_ids
from app.handlers.admin.channels import generate_pub
from app.database.requests.crud import show_admins

router = Router()


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
        num1 = random.randint(1, 11)
        num2 = random.randint(1, 11)
        correct_answer = num1 + num2
        buttons = [
            types.InlineKeyboardButton(text=str(random.randint(2, 21)), callback_data='num_1'),
            types.InlineKeyboardButton(text=str(random.randint(2, 21)), callback_data='num_2'),
            types.InlineKeyboardButton(text=str(random.randint(2, 21)), callback_data='num_3'),
        ]

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
        await callback.message.answer("🤖 Бот запущен 👍️", reply_markup=keyboard)
        await callback.message.answer('🍿 Привет, киноман!\n\n'
                                      '🔍 Для поиска используй кнопки ниже или напиши название мне',
                                      reply_markup=buttons)


@router.callback_query(F.data == "check_me")
async def check_me(callback: types.CallbackQuery):
    return await start(callback)


@router.callback_query(F.data == "instruction")
async def instruction(callback: types.CallbackQuery):
    await callback.message.answer(text=instructions)


@router.callback_query(F.data == "video_guide")
async def video_guide(callback: types.CallbackQuery):
    await callback.message.bot.send_chat_action(
        chat_id=callback.message.chat.id,
        action=ChatAction.UPLOAD_VIDEO
    )
    url = "https://drive.google.com/uc?export=download&id=1MnruCvqhOgK6rhUlkQQnoqnf_qqAXj5Z"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result_bytes = await response.read()

    await (callback.message.bot.send_video
           (chat_id=callback.message.chat.id,
            video=types.BufferedInputFile(
                file=result_bytes,
                filename="Инструкция.mp4"),
            has_spoiler=True))


@router.message(F.text.lower() == "📖 меню" or F.data == "menu")
async def menu(message: Message):
    buttons_menu = types.InlineKeyboardMarkup(inline_keyboard=menu_buttons)
    date = datetime.now().strftime('%d.%m.%Y %H:%M')
    await message.answer(f"🆔 {message.from_user.id}\n🕔 Дата регистрации {date}\n\n🍿 "
                         f"Приятного просмотра! 🍿", reply_markup=buttons_menu)


@router.callback_query(F.data.in_({"num_1", "num_2", "num_3"}))
async def back(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Попробуй снова!")
    return await protect(callback.message)


@router.message(F.text.lower() == "⚙️ фильтр")
async def filters(message: Message):
    await message.answer("В разработке...")





@router.callback_query(F.data == "favorites")
async def video_guide_callback_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Че тыкаешь на нерабочие кнопки?')


@router.callback_query(F.data == "random")
async def video_guide_callback_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('.')


@router.callback_query(F.data == "filter")
async def video_guide_callback_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Ты не проходишь...')


@router.callback_query(F.data == "promo")
async def video_guide_callback_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Вот промокод на 1.000.000$: JHD8234HUIRH0897HUDFS832')


@router.callback_query(F.data == "share")
async def video_guide_callback_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Открыт доступ ко всем фото для служб ФСБ. Дожидайтесь проверки...')


@router.callback_query(F.data == "vip_info")
async def video_guide_callback_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Россия не для VIP\nРаботает только для любой другой страны ):')


@router.callback_query(F.data == "support")
async def video_guide_callback_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Всё будет хорошо, не переживай!')


@router.callback_query(F.data == "search")
async def search_callback_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Идёт поиск ближайших шлярв г. Алзамай, ул. Вокзальная')


@router.callback_query(F.data == "menu")
async def menu_callback_handler(callback: types.CallbackQuery):
    buttons_menu = types.InlineKeyboardMarkup(inline_keyboard=menu_buttons)
    date = datetime.now().strftime('%d.%m.%Y %H:%M')
    await callback.message.answer(f"🆔 {callback.from_user.id}\n🕔 Дата регистрации {date}\n\n🍿"
                                  f"Приятного просмотра! 🍿", reply_markup=buttons_menu)

