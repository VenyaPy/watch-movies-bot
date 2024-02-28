from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import random

start_menu = [
    [
        types.InlineKeyboardButton(text='ℹ️ Видео-гайд', callback_data='video_guide'),
        types.InlineKeyboardButton(text='📖 Меню', callback_data='menu')
    ],
    [types.InlineKeyboardButton(text='🔍 Начать поиск', callback_data='search')]
]

menu_buttons = [
        [
            types.InlineKeyboardButton(text='💡 Инструкция', callback_data='instruction'),
            types.InlineKeyboardButton(text='⭐ Избранное', callback_data='favorites')
        ],
        [
            types.InlineKeyboardButton(text='🎲 Рандом', callback_data='random'),
            types.InlineKeyboardButton(text='⚙️ Фильтр', callback_data='filter')
        ],
        [
            types.InlineKeyboardButton(text='🔠 Промокоды', callback_data='promo'),
            types.InlineKeyboardButton(text='↪️ Поделиться', callback_data='share')
        ],
        [
            types.InlineKeyboardButton(text='💝 VIP инфо', callback_data='vip_info'),
            types.InlineKeyboardButton(text='💁‍♂️ Поддержка', callback_data='support')
        ],
        [types.InlineKeyboardButton(text='🔍 Начать поиск', callback_data='search')]
    ]


