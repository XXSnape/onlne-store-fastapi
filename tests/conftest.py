"""
Модуль с настройками для тестов.
"""

import shutil
from datetime import date
from os import getenv
from pathlib import Path
from typing import AsyncGenerator

import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import ASGITransport, AsyncClient
from redis import asyncio as aioredis
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from catalog.database import (
    CategoryModel,
    ProductModel,
    ReviewModel,
    SaleModel,
    SpecificationModel,
    TagModel,
)
from core import BaseModel, db_helper
from core.utils.jwt import get_access_token
from orders.database import OrderModel, OrderProductModel
from orders.utils.constants import (
    DeliveryTypeEnum,
    OrderStatusEnum,
    PaymentTypeEnum,
)
from src.core import settings
from src.main import app
from users.database import UserModel
from users.utils.auth import get_hashed_password

engine = create_async_engine(settings.db.url, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False
)


@pytest.fixture(scope="session", autouse=True)
def check_testing_env() -> None:
    if getenv("LIMIT") != "5" or getenv("TESTING").lower() != "true":
        pytest.exit(
            "Environment is not ready for testing",
        )


@pytest.fixture(scope="session", autouse=True)
def delete_uploads():
    yield
    uploads = Path(__file__).resolve().parent / "uploads"
    shutil.rmtree(uploads)


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)
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
                UserModel(
                    fullname="Name3 Surname3",
                    username="user3",
                    password=get_hashed_password("qwerty3"),
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
        order1 = OrderModel(
            delivery_type=DeliveryTypeEnum.ordinary,
            payment_type=PaymentTypeEnum.online,
            status=OrderStatusEnum.paid,
            city="city 1",
            address="address 1",
            total_cost=800,
            user_id=1,
        )
        order2 = OrderModel(
            delivery_type=DeliveryTypeEnum.ordinary,
            payment_type=PaymentTypeEnum.online,
            status=OrderStatusEnum.paid,
            city="city 2",
            address="address 2",
            total_cost=400,
            user_id=2,
        )
        order3 = OrderModel(
            delivery_type=DeliveryTypeEnum.ordinary,
            payment_type=PaymentTypeEnum.online,
            status=OrderStatusEnum.unpaid,
            city="city 1",
            address="address 1",
            total_cost=200,
            user_id=1,
        )
        session.add_all([order1, order2, order3])
        tags = [
            TagModel(name="Tag1", categories=[categories[0], categories[1]]),
            TagModel(name="Tag2", categories=[categories[0]]),
            TagModel(name="Tag3"),
        ]
        products = [
            ProductModel(
                id=1,
                title="Product1",
                price_per_unit=100,
                count=0,
                category_id=1,
                orders=[OrderProductModel(count=2, order=order3)],
            ),
            ProductModel(
                id=2,
                title="Product2",
                price_per_unit=200,
                count=10,
                category_id=2,
                orders=[OrderProductModel(count=2, order=order1)],
            ),
            ProductModel(
                id=3,
                title="Product3",
                price_per_unit=300,
                count=0,
                category_id=3,
                reviews=[ReviewModel(rate=1, text="Some text", user_id=1)],
            ),
        ]
        session.add_all(categories + tags + products)
        products = [
            ProductModel(
                id=4,
                title="Product4",
                price_per_unit=400,
                count=4,
                category_id=2,
                reviews=[
                    ReviewModel(rate=1, text="Some text", user_id=1),
                    ReviewModel(rate=1, text="Some2 text", user_id=2),
                ],
                orders=[
                    OrderProductModel(count=1, order=order1),
                    OrderProductModel(count=1, order=order2),
                ],
            ),
            ProductModel(
                id=5,
                title="Product5",
                price_per_unit=500,
                count=5,
                category_id=2,
                reviews=[ReviewModel(rate=2, text="Some text", user_id=1)],
            ),
            ProductModel(
                id=6,
                title="Product6",
                price_per_unit=600,
                count=6,
                category_id=1,
                reviews=[ReviewModel(rate=5, text="Some text", user_id=1)],
            ),
            ProductModel(
                id=7,
                title="Product7",
                price_per_unit=700,
                count=7,
                category_id=1,
                free_delivery=True,
                reviews=[ReviewModel(rate=4, text="Some text", user_id=1)],
                sale=SaleModel(sale_price=50, date_to=date(2030, 9, 6)),
            ),
            ProductModel(
                id=8,
                title="Product8",
                price_per_unit=800,
                count=8,
                category_id=3,
                reviews=[ReviewModel(rate=5, text="Some text", user_id=1)],
                sale=SaleModel(sale_price=700, date_to=date(2030, 9, 7)),
                specifications=[
                    SpecificationModel(
                        name="Spec1",
                        value="Value1",
                    ),
                    SpecificationModel(
                        name="Spec2",
                        value="Value2",
                    ),
                ],
            ),
        ]
        session.add_all(products)
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


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генерирует сессию для асинхронного взаимодействия с тестовой базой данных внутри приложения.
    """
    async with async_session_maker() as session:  # type: AsyncSession
        yield session


app.dependency_overrides[db_helper.get_async_session] = (
    override_get_async_session
)
