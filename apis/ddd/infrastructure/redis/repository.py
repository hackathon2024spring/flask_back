import aioredis
import os


class RedisRipository:
    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = os.getenv("PORT_REDIS", 6379)
        self.redis = aioredis.from_url(f"redis://{redis_host}:{redis_port}")

    async def get(self, key: str):
        value = await self.redis.get(key)
        return value.decode("utf-8") if value else None

    async def set(self, key: str, value: str, expire: int = None):
        await self.redis.set(key, value, ex=expire)

    async def delete(self, key: str):
        await self.redis.delete(key)
