import redis.asyncio as redis
from app.core.config import settings

redis_client = None

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return redis_client

async def cache_get(key: str):
    client = await get_redis()
    return await client.get(key)

async def cache_set(key: str, value: str, expire: int = 300):
    client = await get_redis()
    await client.setex(key, expire, value)

async def cache_delete(key: str):
    client = await get_redis()
    await client.delete(key)
