from aiogram import types

start_menu = [
    [
        types.InlineKeyboardButton(text='ℹ️ Видео-гайд', callback_data='video_guide'),
        types.InlineKeyboardButton(text='📖 Меню', callback_data='menu')
    ],
    [
        types.InlineKeyboardButton(text='🔍 Начать поиск', switch_inline_query_current_chat="")
    ]
]


again = [
    [
        types.InlineKeyboardButton(text='♻️ Повторить поиск', switch_inline_query_current_chat=""),
        types.InlineKeyboardButton(text='👈 В меню', callback_data='back_user_now')
    ]
]

menu_buttons = [
        [
            types.InlineKeyboardButton(text='💡 Инструкция', callback_data='instruction')
        ],
        [
            types.InlineKeyboardButton(text='💝 Поддержать', callback_data='vip_info'),
            types.InlineKeyboardButton(text='🔠 Промокоды', callback_data='promo'),

        ],
        [
            types.InlineKeyboardButton(text='↪️ Поделиться', url='https://t.me/WildKino_bot?startgroup=new'),
            types.InlineKeyboardButton(text='💁‍♂️ Владелец', callback_data='support')
        ],
        [
          types.InlineKeyboardButton(text="🎲 Случайный фильм", callback_data="random_film")
        ],
        [
            types.InlineKeyboardButton(text='🔍 Начать поиск', switch_inline_query_current_chat="")
        ]
    ]


admin_buttons = [
        [
            types.InlineKeyboardButton(text='📊 Статистика', callback_data='statistics'),
            types.InlineKeyboardButton(text='🗯️ Каналы', callback_data='channels')
        ],
        [
            types.InlineKeyboardButton(text='✉️ Рассылка', callback_data='newsletter'),
            types.InlineKeyboardButton(text='⚛️ Администраторы', callback_data='admins')
        ],
        [
            types.InlineKeyboardButton(text='⚙️ Настроить', callback_data='setting')
        ],
        [
            types.InlineKeyboardButton(text='👻 Пользовательское меню', callback_data='menu')
        ]
    ]


public_buttons = [
        [
            types.InlineKeyboardButton(text='🕝 Активные каналы', callback_data='active_pub')
        ],
        [
            types.InlineKeyboardButton(text='✅ Добавить канал', callback_data='add_pub'),
            types.InlineKeyboardButton(text='⛔ Удалить канал', callback_data='delete_pub')
        ],
        [
            types.InlineKeyboardButton(text='👈 Назад', callback_data='back_admin')
        ]
    ]

stat = [
    [
        types.InlineKeyboardButton(text='📤 Выгрузить пользователей', callback_data='users')
    ],
    [
        types.InlineKeyboardButton(text='👀 Просмотры', callback_data='views'),
        types.InlineKeyboardButton(text='🤑 Продажи', callback_data='money')
    ],
    [
        types.InlineKeyboardButton(text='👈 Назад', callback_data='back_admin')
    ]
]

news_menu = [
    [
        types.InlineKeyboardButton(text='✅ Добавить пост', callback_data='add_post')
    ],
    [
        types.InlineKeyboardButton(text='👈 Назад', callback_data='back_admin')
    ]
]


l_add_admin = [
    [
        types.InlineKeyboardButton(text="👑 Администраторы", callback_data='m_admins'),
        types.InlineKeyboardButton(text="🤑 VIP пользователи", callback_data='m_vip')
    ]
]

add_admin_b = [
    [
        types.InlineKeyboardButton(text="📖 Список админов", callback_data='list_admins')
    ],
    [
        types.InlineKeyboardButton(text="✅ Добавить админа", callback_data="add_admin"),
        types.InlineKeyboardButton(text="⛔ Удалить админа", callback_data="del_admin")
    ],
    [
        types.InlineKeyboardButton(text='👈 Назад', callback_data='back_admin')
    ]
]

add_vip = [
    [
        types.InlineKeyboardButton(text="📖 Список VIP", callback_data='list_vip')
    ],
    [
        types.InlineKeyboardButton(text="✅ Добавить VIP", callback_data="add_vip"),
        types.InlineKeyboardButton(text="⛔ Удалить VIP", callback_data="del_vip")
    ],
    [
        types.InlineKeyboardButton(text='👈 Назад', callback_data='back_admin')
    ]
]


back_admin = [
    [
        types.InlineKeyboardButton(text='👈 Вернуться в меню', callback_data='back_admin')
    ]
]


back_user = [
    [
        types.InlineKeyboardButton(text='👈 Вернуться в меню', callback_data='back_user')
    ]
]


back_user_new = [
    [
        types.InlineKeyboardButton(text='👈 Вернуться в меню', callback_data='back_user_now')
    ]
]


vip_user_menu = [
    [
        types.InlineKeyboardButton(text='👈 Вернуться в меню', callback_data='back_user')
    ]
]


promokode_m = [
    [
        types.InlineKeyboardButton(text='🚀 Ввести промокод', callback_data='promis_get'),
        types.InlineKeyboardButton(text='👈 Назад', callback_data='back_user')
    ]
]


chose = [
    [
        types.InlineKeyboardButton(text="Фильмы", callback_data='films'),
        types.InlineKeyboardButton(text="Сериалы", callback_data='tv_serials'),
    ],
    [
        types.InlineKeyboardButton(text='👈 Назад', callback_data='back_user')
    ]
]


