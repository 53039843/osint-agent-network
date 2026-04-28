import json
import asyncio
from typing import Optional, Any
from core.config import settings
from utils.logger import setup_logger

logger = setup_logger("redis_cache")

class RedisCache:
    """
    Async wrapper for Redis caching.
    Used to avoid redundant API calls to external services (Shodan, VT, etc.)
    for the same IoCs within a short timeframe.
    """
    def __init__(self):
        try:
            import redis.asyncio as redis
            self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.enabled = True
        except ImportError:
            logger.warning("redis-py not installed. Caching disabled.")
            self.enabled = False
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}. Caching disabled.")
            self.enabled = False

    async def get(self, key: str) -> Optional[Any]:
        if not self.enabled:
            return None
        try:
            val = await self.client.get(key)
            if val:
                return json.loads(val)
        except Exception as e:
            logger.error(f"Redis get error: {e}")
        return None

    async def set(self, key: str, value: Any, expire_sec: int = 3600):
        if not self.enabled:
            return
        try:
            await self.client.set(key, json.dumps(value), ex=expire_sec)
        except Exception as e:
            logger.error(f"Redis set error: {e}")

    async def close(self):
        if self.enabled:
            await self.client.close()

# Singleton instance
cache = RedisCache()
