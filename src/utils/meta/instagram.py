import time
import httpx
from ...exeptions import InstagramMediaException

cache = {
    "data": None,
    "timestamp": 0
}

CACHE_TTL = 60 * 30  # 30 minutos

async def get_media(access_token: str, url: str):
    current_time = time.time()
    # usar cache si existe
    if cache["data"] and current_time - cache["timestamp"] < CACHE_TTL:
        return cache["data"]
    params = {
        "fields": "id,caption,media_url,permalink,thumbnail_url,media_type",
        "access_token": access_token
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    data = response.json()

    if data.get("error"):
        raise InstagramMediaException(data.get('error').get('message'))

    media = [
        item for item in data.get("data", [])
        if item["media_type"] in ["IMAGE", "CAROUSEL_ALBUM"]
    ]
    # guardar cache
    cache["data"] = media
    cache["timestamp"] = current_time
    return media
