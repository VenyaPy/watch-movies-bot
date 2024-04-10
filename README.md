**Название продукта:** ВсёКино

**Описание:** Телеграм-бот для просмотра фильмов, сериалов или аниме.

Ссылка на бот (возможно не актуальна, если сервер отключен): https://t.me/animefilms_bot

**Возможности:**

- Библиотека: Aiogram 3.x
- База данных: SQLite
- Кеширование: Redis, библиотека Aioredis
- Дополнительные библиотеки: YooMoney, SQLAlchemy


_1. Пользовательская сторона:_

- Поиск фильмов и сериалов через агрегаторы плееров и видеобалансеры. Поиск происходит через InlineQuery. Ссылка на просмотр формируется через хостинг на reg.ru и скрипт написанный на PHP (для актуализации ссылки).
- Функция случайный фильм. Категории: фильмы/сериалы/аниме. Всё это кешируется, чтобы не ждать ответа от API.
- Возможность оплатить VIP подписку для отключения рекламы в боте и обязательных подписок.

_2. Админ меню:_

- Добавление/удаление/просмотр обязательных подписок на каналы. Реализовано через SQLite и FSMcontext.
- Рассылка всем пользователям из базы данных. Также через через SQLite и FSMcontext.
- Добавление/удаление администраторов и VIP пользователей.
- Статистика с выгрузкой пользователей.
- Фильтрация функция на IsAdmin для предотвращения от случайного перехода в админ-меню.

