import random
import aioredis
import aiohttp
from aiogram import F, types, Router
from aiogram.types import InlineKeyboardMarkup, CallbackQuery

from app.templates.keyboard.inline import catygory
from app.utils.model import KinopoiskCategory, Category, CategoryFilm, CategorySerial
from aiogram.exceptions import TelegramBadRequest


category_router = Router()


@category_router.callback_query(F.data == "random_film")
async def random_film(callback: types.CallbackQuery):
    await callback.message.delete()

    movie_data = await KinopoiskCategory.kinopoisk_api(
        url="https://kinobox.tv/api/films/popular"
    )

    if not isinstance(movie_data, list) or not movie_data:
        return

    # Выбираем случайный индекс
    current_index = random.randint(0, len(movie_data) - 1)
    movie = movie_data[current_index]

    id = movie.get('id', 'Название не указано')
    name = movie.get('title', 'Название не указано')
    year = movie.get('year', 'Описание не указано')
    rating = str(movie.get('rating', 'Описание не указано'))
    poster = movie.get('posterUrl', None)

    kew = [
        [
            types.InlineKeyboardButton(text="♻️ Повторить", callback_data="random_film")
        ],
        [
            types.InlineKeyboardButton(text='🎬 Смотреть', switch_inline_query_current_chat=f"kp{id}"),
            types.InlineKeyboardButton(text='👈 В меню', callback_data='back_user_go')
        ]
    ]
    d = InlineKeyboardMarkup(inline_keyboard=kew)

    await callback.message.answer_photo(photo=poster,
                                        caption=f"📽️ <b>Название:</b> {name}, {year}\n\nРейтинг: {rating}",
                                        reply_markup=d)


@category_router.callback_query(F.data == "category")
async def catygoryes(callback: CallbackQuery):
    await callback.message.delete()
    r = InlineKeyboardMarkup(inline_keyboard=catygory)
    await callback.message.answer(text="Выберите категорию 👇", reply_markup=r)


user_last_anime_index = {}

@category_router.callback_query(F.data == "random_anime")
async def random_anime(callback: types.CallbackQuery):
    await callback.message.delete()
    type = 'anime'
    user_id = callback.from_user.id
    if user_id not in user_last_anime_index:
        user_last_anime_index[user_id] = -1

    url = 'https://api.kinopoisk.dev/v1.4/movie?page=1&limit=100&type=anime'
    data = await Category.kinopoisk_search(url=url, types=type)
    anime_data = data.get('docs', [])
    if not anime_data:
        await callback.message.answer("Аниме не найдены.")
        return

    while True:
        user_last_anime_index[user_id] += 1
        current_index = user_last_anime_index[user_id] % len(anime_data)
        if user_last_anime_index[user_id] - len(anime_data) > 0:
            await callback.message.answer("Просмотрены все аниме.")
            break

        anime = anime_data[current_index]
        id = anime.get('id', 'ID не указан')
        name = anime.get('name', 'Название не указано')
        year = anime.get('year', 'Год не указан')
        altname = anime.get('alternativeName', '') or ('Аниме')
        details = anime.get('description', 'Описания нет')
        rating_kp = str(anime.get('rating', {}).get('kp', 'Рейтинг не указан'))
        poster = anime.get('poster', {}).get('url', None)

        caption = (f"🎬 <b>Название:</b> {name} ({altname}), {year}\n\n"
                   f"⭐ <b>Рейтинг КП:</b> {rating_kp}\n\n"
                   f"📝 <b>Описание:</b> {details}")

        anime_menu = [
            [types.InlineKeyboardButton(text="♻️ Далее", callback_data="random_anime")],
            [types.InlineKeyboardButton(text='🎬 Смотреть', switch_inline_query_current_chat=f"kp{id}"),
             types.InlineKeyboardButton(text='👈 В меню', callback_data='back_user_go')]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=anime_menu)

        try:
            await callback.message.answer_photo(
                photo=poster,
                caption=caption,
                reply_markup=reply_markup
            )
            break  # Успешно отправлено, выходим из цикла
        except TelegramBadRequest as e:
            if "wrong type of the web page content" in str(e):
                continue  # Пропускаем текущий элемент и пробуем следующий
            else:
                await callback.message.answer("Произошла ошибка.")
                break


user_last_film_index = {}

@category_router.callback_query(F.data == "random_films")
async def random_films(callback: types.CallbackQuery):
    await callback.message.delete()
    type = 'film'
    user_id = callback.from_user.id
    if user_id not in user_last_film_index:
        user_last_film_index[user_id] = -1

    url = 'https://api.kinopoisk.dev/v1.4/movie?page=1&limit=50&type=movie&lists=top250'
    data = await CategoryFilm.kinopoisk_search(url=url, types=type)
    film_data = data.get('docs', [])
    if not film_data:
        await callback.message.answer("Фильмы не найдены.")
        return

    while True:
        user_last_film_index[user_id] += 1
        current_index = user_last_film_index[user_id] % len(film_data)
        if user_last_film_index[user_id] - len(film_data) > 0:
            await callback.message.answer("Просмотрены все фильмы.")
            break

        film = film_data[current_index]
        id = film.get('id', 'ID не указан')
        name = film.get('name', 'Название не указано')
        year = film.get('year', 'Год не указан')
        altname = film.get('alternativeName', '') or ('Фильм')
        details = film.get('description', 'Описания нет')
        rating_kp = str(film.get('rating', {}).get('kp', 'Рейтинг не указан'))
        poster = film.get('poster', {}).get('url', None)

        caption = (f"🎬 <b>Название:</b> {name} ({altname}), {year}\n\n"
                   f"⭐ <b>Рейтинг КП:</b> {rating_kp}\n\n"
                   f"📝 <b>Описание:</b> {details}")

        film_menu = [
            [types.InlineKeyboardButton(text="♻️ Далее", callback_data="random_films")],
            [types.InlineKeyboardButton(text='🎬 Смотреть', switch_inline_query_current_chat=f"kp{id}"),
             types.InlineKeyboardButton(text='👈 В меню', callback_data='back_user_go')]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=film_menu)

        try:
            await callback.message.answer_photo(
                photo=poster,
                caption=caption,
                reply_markup=reply_markup
            )
            break
        except TelegramBadRequest as e:
            if "wrong type of the web page content" in str(e):
                continue
            else:
                await callback.message.answer("Произошла ошибка.")
                break


user_last_serial_index = {}


@category_router.callback_query(F.data == "random_serial")
async def random_serial(callback: types.CallbackQuery):
    await callback.message.delete()
    type = 'serial'
    user_id = callback.from_user.id
    if user_id not in user_last_serial_index:
        user_last_serial_index[user_id] = -1

    url = 'https://api.kinopoisk.dev/v1.4/movie?page=1&limit=50&type=tv-series&lists=series-top250'
    data = await CategorySerial.kinopoisk_search(url=url, types=type)
    serial_data = data.get('docs', [])
    if not serial_data:
        await callback.message.answer("Сериалы не найдены.")
        return

    while True:
        user_last_serial_index[user_id] += 1
        current_index = user_last_serial_index[user_id] % len(serial_data)
        if user_last_serial_index[user_id] - len(serial_data) > 0:
            await callback.message.answer("Просмотрены все сериалы.")
            break

        serial = serial_data[current_index]
        id = serial.get('id', 'ID не указан')
        name = serial.get('name', 'Название не указано')
        year = serial.get('year', 'Год не указан')
        altname = serial.get('alternativeName', '') or ('Сериал')
        details = serial.get('description', 'Описания нет')
        rating_kp = str(serial.get('rating', {}).get('kp', 'Рейтинг не указан'))
        poster = serial.get('poster', {}).get('url', None)

        caption = (f"🎬 <b>Название:</b> {name} ({altname}), {year}\n\n"
                   f"⭐ <b>Рейтинг КП:</b> {rating_kp}\n\n"
                   f"📝 <b>Описание:</b> {details}")

        serial_menu = [
            [types.InlineKeyboardButton(text="♻️ Далее", callback_data="random_serial")],
            [types.InlineKeyboardButton(text='🎬 Смотреть', switch_inline_query_current_chat=f"kp{id}"),
             types.InlineKeyboardButton(text='👈 В меню', callback_data='back_user_go')]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=serial_menu)

        try:
            await callback.message.answer_photo(
                photo=poster,
                caption=caption,
                reply_markup=reply_markup
            )
            break
        except TelegramBadRequest as e:
            if "wrong type of the web page content" in str(e):
                continue
            else:
                await callback.message.answer("Произошла ошибка.")
                break