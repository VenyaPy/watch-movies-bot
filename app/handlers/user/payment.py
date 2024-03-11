from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from yoomoney import Authorize
from yoomoney import Quickpay
from config import PAYMENTS_TOKEN
from yoomoney import Client

pay = Router()


token = PAYMENTS_TOKEN
client = Client(token)
user = client.account_info()
print("Account number:", user.account)
print("Account balance:", user.balance)
print("Account currency code in ISO 4217 format:", user.currency)
print("Account status:", user.account_status)
print("Account type:", user.account_type)
print("Extended balance information:")
for pair in vars(user.balance_details):
    print("\t-->", pair, ":", vars(user.balance_details).get(pair))
print("Information about linked bank cards:")
cards = user.cards_linked
if len(cards) != 0:
    for card in cards:
        print(card.pan_fragment, " - ", card.type)
else:
    print("No card is linked to the account")


@pay.callback_query(F.data == "1_VIP")
async def base_vip(callback: CallbackQuery):
    await callback.message.delete()

    user_id = callback.from_user.id

    quickpay = Quickpay(
        receiver="4100118593083880",
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        label=f"{user_id}",
        sum=100,
    )

    url = quickpay.base_url

    pay_k = [
        [
            InlineKeyboardButton(text="💳 Оплатить", url=url)
        ],
        [
            InlineKeyboardButton(text='👈 Назад', callback_data='back_user')
        ]
    ]

    pay_button = InlineKeyboardMarkup(inline_keyboard=pay_k)

    await callback.message.answer(text="✅ Сформирована кнопка для оплаты ✅", reply_markup=pay_button)


@pay.callback_query(F.data == "2_VIP")
async def base_vip(callback: CallbackQuery):
    await callback.message.delete()

    user_id = callback.from_user.id

    quickpay = Quickpay(
        receiver="4100118593083880",
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        label=f"{user_id}",
        sum=300,
    )

    url = quickpay.base_url

    pay_k = [
        [
            InlineKeyboardButton(text="💳 Оплатить", url=url)
        ],
        [
            InlineKeyboardButton(text='👈 Назад', callback_data='back_user')
        ]
    ]

    pay_button = InlineKeyboardMarkup(inline_keyboard=pay_k)

    await callback.message.answer(text="✅ Сформирована кнопка для оплаты ✅", reply_markup=pay_button)


@pay.callback_query(F.data == "3_VIP")
async def base_vip(callback: CallbackQuery):
    await callback.message.delete()

    user_id = callback.from_user.id

    quickpay = Quickpay(
        receiver="4100118593083880",
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        label=f"{user_id}",
        sum=300,
    )

    url = quickpay.base_url

    pay_k = [
        [
            InlineKeyboardButton(text="💳 Оплатить", url=url)
        ],
        [
            InlineKeyboardButton(text='👈 Назад', callback_data='back_user')
        ]
    ]

    pay_button = InlineKeyboardMarkup(inline_keyboard=pay_k)

    await callback.message.answer(text="✅ Сформирована кнопка для оплаты ✅", reply_markup=pay_button)


@pay.callback_query(F.data == "6_VIP")
async def base_vip(callback: CallbackQuery):
    await callback.message.delete()

    user_id = callback.from_user.id

    quickpay = Quickpay(
        receiver="4100118593083880",
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        label=f"{user_id}",
        sum=700,
    )

    url = quickpay.base_url

    pay_k = [
        [
            InlineKeyboardButton(text="💳 Оплатить", url=url)
        ],
        [
            InlineKeyboardButton(text='👈 Назад', callback_data='back_user')
        ]
    ]

    pay_button = InlineKeyboardMarkup(inline_keyboard=pay_k)

    await callback.message.answer(text="✅ Сформирована кнопка для оплаты ✅", reply_markup=pay_button)


@pay.callback_query(F.data == "Always_VIP")
async def base_vip(callback: CallbackQuery):
    await callback.message.delete()

    user_id = callback.from_user.id

    quickpay = Quickpay(
        receiver="4100118593083880",
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        label=f"{user_id}",
        sum=3000,
    )

    url = quickpay.base_url

    pay_k = [
        [
            InlineKeyboardButton(text="💳 Оплатить", url=url)
        ],
        [
            InlineKeyboardButton(text='👈 Назад', callback_data='back_user')
        ]
    ]

    pay_button = InlineKeyboardMarkup(inline_keyboard=pay_k)

    await callback.message.answer(text="✅ Сформирована кнопка для оплаты ✅", reply_markup=pay_button)