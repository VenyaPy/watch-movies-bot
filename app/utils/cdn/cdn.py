import asyncio
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery
from app.templates.keyboard.button import find
from aiogram import types
import json
from app.templates.keyboard.inline import chose
import aiohttp
from uuid import uuid4
from typing import List, Dict, Union
import urllib.parse


cdn_rou = Router()



# FILMS

class FormSearch(StatesGroup):
    waiting_for_movie_name = State()
    search_result = State()


async def fetch_movies(query):
    try:
        url = f"https://apivb.info/api/videos.json?title={query}&token=0befa987b7d85bcdad0b31e2e7c3f4ec"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    movies = await response.json(content_type=None)
                    return movies
                return []
    except Exception as e:
        print(e)
        return []



@cdn_rou.inline_query()
async def inline_query(inline_query: types.InlineQuery):
    query = inline_query.query.replace(" ", "_")
    response = await fetch_movies(query)
    results = []

    if isinstance(response, list):
        films = response[:50]
    elif isinstance(response, dict):
        films = response.get('data', [])[:50]
    else:
        films = []

    for film in films:
        if 'title_en' in film and film['title_en']:
            corrected_url = film.get('iframe_url', '').replace('\\/', '/')
            unique_id = str(uuid4())
            results.append(types.InlineQueryResultArticle(
                id=unique_id,
                title=film['title_ru'],
                input_message_content=types.InputTextMessageContent(message_text=film['title_ru']),
                description=f"{film.get('year', 'Год не указан')}",
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text="🤗 Ссылка на просмотр",
                                                url=corrected_url)]
                ])
            ))

    if not films:
        # Обработка случая, когда фильмы не найдены
        unique_id = str(uuid4())
        results.append(types.InlineQueryResultArticle(
            id=unique_id,
            title="Фильм не найден",
            input_message_content=types.InputTextMessageContent(message_text="Фильмы не найдены. Попробуйте изменить запрос."),
            description="Попробуйте другой запрос"
        ))

    await inline_query.answer(results, cache_time=1, is_personal=True)
