"""
Модуль с настройками для тестов.
"""

from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.utils.jwt import get_access_token
from src.core import db_helper, settings
from src.main import app
from users.database import UserModel
from users.utils.auth import get_hashed_password

engine = create_async_engine(settings.db.url, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False
)


@pytest.fixture(scope="session", autouse=True)
async def create_users():
    async with async_session_maker() as session:
        session.add(
            UserModel(
                fullname="Name Surname",
                username="user1",
                password=get_hashed_password("qwerty"),
            )
        )
        await session.commit()


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генерирует сессию для асинхронного взаимодействия с тестовой базой данных внутри приложения.
    """
    async with async_session_maker() as session:  # type: AsyncSession
        yield session


@pytest.fixture()
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генерирует сессию для асинхронного взаимодействия с тестовой базой данных внутри тестов.
    """
    async with async_session_maker() as session:  # type: AsyncSession
        yield session


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """
    Возвращает клиента для асинхронного взаимодействия с приложением внутри тестов.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
def access_token():
    return get_access_token(user_id=1, username="user1", is_admin=False)


app.dependency_overrides[db_helper.get_async_session] = (
    override_get_async_session
)
