"""
Модуль с настройками для тестов.
"""

from datetime import date
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

from catalog.database import (
    CategoryModel,
    TagModel,
    ProductModel,
    ReviewModel,
    SaleModel,
)
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
            CategoryModel(title="Category1", id=1),
            CategoryModel(title="Category2", id=2),
            CategoryModel(title="Category3", id=3),
            CategoryModel(title="Category4", id=4),
            CategoryModel(title="Category5", id=5),
            CategoryModel(title="Category6", id=6),
        ]
        categories[3].children = [categories[4]]
        categories[2].children = [categories[3]]
        categories[0].children = [categories[1], categories[2]]

        tags = [
            TagModel(name="Tag1", categories=[categories[0], categories[1]]),
            TagModel(name="Tag2", categories=[categories[0]]),
            TagModel(name="Tag3"),
        ]
        products = [
            ProductModel(
                title="Product1", price_per_unit=100, count=0, category_id=1
            ),
            ProductModel(
                title="Product2", price_per_unit=200, count=10, category_id=2
            ),
            ProductModel(
                title="Product3",
                price_per_unit=300,
                count=0,
                category_id=3,
                reviews=[ReviewModel(rate=1, text="Some text", user_id=1)],
            ),
            ProductModel(
                title="Product4",
                price_per_unit=400,
                count=4,
                category_id=2,
                reviews=[
                    ReviewModel(rate=1, text="Some text", user_id=1),
                    ReviewModel(rate=1, text="Some text", user_id=2),
                ],
            ),
            ProductModel(
                title="Product5",
                price_per_unit=500,
                count=5,
                category_id=2,
                reviews=[ReviewModel(rate=2, text="Some text", user_id=1)],
            ),
            ProductModel(
                title="Product6",
                price_per_unit=600,
                count=6,
                category_id=1,
                reviews=[ReviewModel(rate=5, text="Some text", user_id=1)],
            ),
            ProductModel(
                title="Product7",
                price_per_unit=700,
                count=7,
                category_id=1,
                free_delivery=True,
                reviews=[ReviewModel(rate=4, text="Some text", user_id=1)],
                sale=SaleModel(sale_price=50, date_to=date(2030, 9, 6)),
            ),
            ProductModel(
                title="Product8",
                price_per_unit=800,
                count=8,
                category_id=3,
                reviews=[ReviewModel(rate=5, text="Some text", user_id=1)],
                sale=SaleModel(sale_price=700, date_to=date(2030, 9, 7)),
            ),
        ]
        session.add_all(categories + tags + products)

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
