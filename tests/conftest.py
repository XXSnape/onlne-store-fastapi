"""
Модуль с настройками для тестов.
"""

from typing import AsyncGenerator

import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from catalog.database import CategoryModel, TagModel
from core.utils.jwt import get_access_token
from src.core import settings
from src.main import app
from users.database import UserModel
from users.utils.auth import get_hashed_password

engine = create_async_engine(settings.db.url, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False
)


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    async with async_session_maker() as session:
        session.add_all(
            [
                UserModel(
                    fullname="Name Surname",
                    username="user1",
                    password=get_hashed_password("qwerty"),
                ),
                UserModel(
                    fullname="Name2 Surname2",
                    username="user2",
                    password=get_hashed_password("qwerty2"),
                ),
            ]
        )
        categories = [
            CategoryModel(title="Category1"),
            CategoryModel(title="Category2"),
            CategoryModel(title="Category3"),
            CategoryModel(title="Category4"),
            CategoryModel(title="Category5"),
            CategoryModel(title="Category6"),
        ]
        categories[3].children = [categories[4]]
        categories[2].children = [categories[3]]
        categories[0].children = [categories[1], categories[2]]

        tags = [
            TagModel(name="Tag1", categories=categories[:2]),
            TagModel(name="Tag2", categories=[categories[0]]),
            TagModel(name="Tag3"),
        ]
        session.add_all(categories + tags)

        await session.commit()


@pytest.fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генерирует сессию для асинхронного взаимодействия с тестовой базой данных внутри тестов.
    """
    async with async_session_maker() as session:  # type: AsyncSession
        yield session


@pytest.fixture(scope="session", autouse=True)
async def set_cache():
    redis = aioredis.from_url(settings.redis.url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """
    Возвращает клиента для асинхронного взаимодействия с приложением внутри тестов.
    """

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        cookies={
            "access-token": get_access_token(
                user_id=1, username="user1", is_admin=False
            )
        },
    ) as ac:
        yield ac
