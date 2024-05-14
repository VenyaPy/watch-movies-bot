from aiogram import Router
from aiogram.types import InlineKeyboardMarkup
from aiogram import types
import aiohttp
from uuid import uuid4
import re
from app.templates.text.user import instructions_b
from app.templates.keyboard.inline import again
from config import api_hbtv
from app.utils.model import KinopoiskCategory
from urllib.parse import urlparse

cdn_rou = Router()


async def fetch_movies(query):
    try:
        kp_link_match = re.match(r'https?://www\.kinopoisk\.ru/(series|film)/(\d+)', query)
        if kp_link_match:
            kp_id = kp_link_match.group(2)
            url = f"https://apivb.info/api/videos.json?id_kp={kp_id}&token={api_hbtv}"
        else:
            kp_match = re.match(r'kp(\d+)', query)
            if kp_match:
                kp_id = kp_match.group(1)
                url = f"https://apivb.info/api/videos.json?id_kp={kp_id}&token={api_hbtv}"
            else:
                url = f"https://apivb.info/api/videos.json?title={query}&token={api_hbtv}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    movies = await response.json(content_type=None)
                    return movies
        return []
    except Exception as e:
        print(e)
        return []


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


default_poster = "app/photo.png"


@cdn_rou.inline_query()
async def inline_query(inline: types.InlineQuery):
    query = inline.query.strip()

    # Минимальная длина запроса
    if len(query) < 3:
        await inline.answer([], cache_time=1, is_personal=True)
        return

    response = await fetch_movies(query)
    results = []

    # Определяем, есть ли фильмы в ответе
    if isinstance(response, list):
        films = response[:50]
    elif isinstance(response, dict):
        films = response.get('data', [])[:50]
    else:
        films = []

    # Создаем результаты для ответа
    for film in films:
        film_id = film.get("kinopoisk_id")
        title = film.get('title_ru') or film.get('title_en')
        year = film.get('year', '')
        trailer_url = film.get('trailer', '')

        movie = await KinopoiskCategory.kinopoisk_search(id=film_id)
        quality = movie.get('ratingKinopoisk')
        poster = movie.get('posterUrlPreview') or movie.get('posterUrl') or film.get('poster', '').replace('\\/', '/')
        poster = poster if is_valid_url(poster) else default_poster

        about = movie.get('description', '')

        shortDescription = movie.get('shortDescription', '') or movie.get('description', '')

        genres_list = movie.get('genres', [])
        genres = ', '.join([genre['genre'] for genre in genres_list])

        countries_list = movie.get('countries', [])
        countries = ', '.join([country['country'] for country in countries_list])

        my_site_url = f"https://kinowild.ru/player?{film_id}"

        unique_id = str(uuid4())

        # Создание клавиатуры для фильма
        keyboard_buttons = [
            [types.InlineKeyboardButton(text="🤗 Начать просмотр", url=my_site_url)]
        ]

        # Добавление кнопки трейлера, если он доступен
        if trailer_url:
            keyboard_buttons.insert(1, [types.InlineKeyboardButton(text="🎬 Посмотреть трейлер", url=trailer_url)])

        # Добавление кнопки для повторения поиска в конец списка кнопок
        keyboard_buttons.append(
            [types.InlineKeyboardButton(text='♻️ Повторить поиск', switch_inline_query_current_chat=""),
             types.InlineKeyboardButton(text='👈 В меню', callback_data='back_user_now')])

        # Создание клавиатуры с кнопками
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

        # Сообщение в результате поиска
        result_text = types.InputTextMessageContent(
            message_text=(
                f"🎬 <b>{title}</b> ({film.get('title_en')})\n\n"
                f"🗓 <b>Год выхода:</b> {year}\n"
                f"🌍 <b>Страна:</b> {countries}\n"
                f"🌟 <b>Рейтинг:</b> {quality}\n"
                f"🎭 <b>Жанры:</b> {genres}\n\n"
                f"🔎 <b>Описание:</b>\n{about}\n\n"
                f"⚠️ Отключите VPN перед началом просмотра!\n\n"
                f"🍿 Приятного просмотра! 🍿"
            ))

        results.append(types.InlineQueryResultArticle(
            id=unique_id,
            title=title,
            input_message_content=result_text,
            description=shortDescription,
            thumbnail_url=poster,
            reply_markup=keyboard,
        ))

    if not films:
        unique_id = str(uuid4())

        ag_but = InlineKeyboardMarkup(inline_keyboard=again)

        results.append(types.InlineQueryResultArticle(
            id=unique_id,
            title="Результаты не обнаружены 🫣",
            input_message_content=types.InputTextMessageContent(message_text=instructions_b),
            description="Нажми на меня, чтобы узнать почему",
            reply_markup=ag_but
        ))

    await inline.answer(results, cache_time=1, is_personal=True)
