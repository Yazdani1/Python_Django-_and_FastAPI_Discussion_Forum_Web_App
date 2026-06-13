import json
import logging
from typing import Any

import redis.asyncio as aioredis

from fastapi_app.core.config import settings

logger = logging.getLogger(__name__)

_redis: aioredis.Redis | None = None


async def connect_redis() -> None:
    global _redis
    _redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    await _redis.ping()
    logger.info("Redis connected at %s", settings.REDIS_URL)


async def disconnect_redis() -> None:
    global _redis
    if _redis:
        await _redis.aclose()
        _redis = None


async def cache_get(key: str) -> Any | None:
    if not _redis:
        return None
    try:
        value = await _redis.get(key)
        return json.loads(value) if value else None
    except Exception:
        logger.warning("Redis cache_get failed for key: %s", key)
        return None


async def cache_set(key: str, value: Any, ttl: int = 60) -> None:
    if not _redis:
        return
    try:
        await _redis.setex(key, ttl, json.dumps(value, default=str))
    except Exception:
        logger.warning("Redis cache_set failed for key: %s", key)


async def cache_delete(key: str) -> None:
    if not _redis:
        return
    try:
        await _redis.delete(key)
    except Exception:
        logger.warning("Redis cache_delete failed for key: %s", key)


async def cache_delete_pattern(pattern: str) -> None:
    if not _redis:
        return
    try:
        # KEYS is O(N) — fine for dev; use SCAN in production with large keyspaces
        keys = await _redis.keys(pattern)
        if keys:
            await _redis.delete(*keys)
    except Exception:
        logger.warning("Redis cache_delete_pattern failed for pattern: %s", pattern)
