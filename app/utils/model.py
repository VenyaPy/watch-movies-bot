import aiohttp
import datetime


api_keys = ["15858539-fb77-44ef-9565-8b965954ebb3",
            "b96ac5f5-3bf5-42ae-b90e-1c6dd15cef5a",
            "441451fe-c5d1-46d7-aae8-a6f80580220d"]

def get_api_key():
    now = datetime.datetime.now()
    minutes = now.hour * 60 + now.minute
    key_index = (minutes // 30) % len(api_keys)
    return api_keys[key_index]


class KinopoiskCategory:

    @classmethod
    async def fetch_data(cls, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {}

    @classmethod
    async def kinopoisk_api(cls, url):
        data = await cls.fetch_data(url)
        return data


    @classmethod
    async def kinopoisk_search(cls, id):
        try:
            current_api_key = get_api_key()
            url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}"
            headers = {
                'accept': 'application/json',
                'X-API-KEY': current_api_key,
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {}
        except Exception as e:
            print(e)
            return []

