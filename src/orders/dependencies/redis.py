from collections.abc import AsyncGenerator
from typing import Annotated, TypeAlias

from fastapi import Depends
from redis import asyncio as aioredis

from core import settings


async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    redis = aioredis.from_url(settings.redis.url, decode_responses=True)
    yield redis
    await redis.close()


RedisDep: TypeAlias = Annotated[aioredis.Redis, Depends(get_redis)]
