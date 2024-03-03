import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

form_router = Router()


class Form(StatesGroup):
    id_pub = State()
    url_pub = State()


@form_router.message()
async def begin_add(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.id_pub)
    await message.answer("Введите ID паблика")


@form_router.message(Form.id_pub)
async def process_id(message: Message, state: FSMContext):
    await state.update_data(id_pub=message.text)
    await state.set_state(Form.url_pub)
    await message.answer("Теперь введите URL паблика")

@form_router.message(Form.url_pub)
async def process_url(message: Message, state: FSMContext):
    await state.update_data(url_pub=message.text)
    await





