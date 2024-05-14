import aiohttp
import datetime
import aioredis
import json

from config import api_keys, api


def get_api_key():
    now = datetime.datetime.now()
    minutes = now.hour * 60 + now.minute
    key_index = (minutes // 30) % len(api_keys)
    return api_keys[key_index]


class Category:
    headers = {'accept': 'application/json', 'X-API-KEY': api}

    @classmethod
    async def fetch_data(cls, url, types):
        async with aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True) as redis:
            cache_key = f"{types}_data_{url}"
            cached_data = await redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=url, headers=cls.headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            await redis.set(cache_key, json.dumps(data), ex=86400)
                            return data
                        else:
                            return {}

    @classmethod
    async def kinopoisk_search(cls, url, types):
        return await cls.fetch_data(url, types)


class CategoryFilm:
    headers = {'accept': 'application/json', 'X-API-KEY': api}

    @classmethod
    async def fetch_data(cls, url, types):
        async with aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True) as redis:
            cache_key = f"{types}_data_{url}"
            cached_data = await redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=url, headers=cls.headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            await redis.set(cache_key, json.dumps(data), ex=86400)
                            return data
                        else:
                            return {}

    @classmethod
    async def kinopoisk_search(cls, url, types):
        return await cls.fetch_data(url, types)


class CategorySerial:
    headers = {'accept': 'application/json', 'X-API-KEY': api}

    @classmethod
    async def fetch_data(cls, url, types):
        async with aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True) as redis:
            cache_key = f"{types}_data_{url}"
            cached_data = await redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=url, headers=cls.headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            await redis.set(cache_key, json.dumps(data), ex=86400)
                            return data
                        else:
                            return {}

    @classmethod
    async def kinopoisk_search(cls, url, types):
        return await cls.fetch_data(url, types)


class KinopoiskCategory:

    @classmethod
    async def fetch_data(cls, url):
        redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
        cache_key = f"kinopoisk_data_{url}"
        cached_data = await redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as response:
                    if response.status == 200:
                        data = await response.json()
                        await redis.set(cache_key, json.dumps(data), ex=86400)  # Кешируем на сутки
                        return data
                    else:
                        return {}

    @classmethod
    async def kinopoisk_api(cls, url):
        return await cls.fetch_data(url)

    @classmethod
    async def kinopoisk_search(cls, id):
        try:
            current_api_key = get_api_key()
            url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}"
            headers = {
                'accept': 'application/json',
                'X-API-KEY': current_api_key,
            }

            redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
            cache_key = f"kinopoisk_film_{id}"

            cached_data = await redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)

            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        await redis.set(cache_key, json.dumps(data), ex=86400)
                        return data
                    else:
                        return {}

        except Exception as e:
            print(e)
            return []

