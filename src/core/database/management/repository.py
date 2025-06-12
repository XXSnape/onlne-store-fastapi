"""
Модуль с абстрактными репозиториями для работы с таблицами базы данных.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from fastapi import HTTPException, status
from sqlalchemy import Row, delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core import BaseModel, logger

OBJECT_NOT_CREATED_ERROR = "The object has not been created"


class AbstractRepository(ABC):
    """
    Абстрактный класс - репозиторий.
    """

    @abstractmethod
    async def create_object(
        self,
        session: AsyncSession,
        data: dict,
        exception_detail: str = OBJECT_NOT_CREATED_ERROR,
    ) -> int:
        """
        Добавляет новый объект в базу данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, которые должны быть добавлены в базу

        exception_detail: Сообщение об ошибке, которое возникает во всех случаях,
        когда не удается создать объект


        Возвращает идентификатор добавленной записи.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_object_by_params(
        self,
        session: AsyncSession,
        data: dict,
    ) -> bool:
        """
        Удаляет объекты из базы данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, по которым будет осуществлен поиск объектов для удаления

        Возвращает True, если объекты были удалены и False в противном случае.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_object_by_params(
        self, session: AsyncSession, data: dict
    ) -> Optional[Any]:
        """
        Ищет объект в базе данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, по которым будет осуществлен поиск объекта

        Возвращает объект базы данных или None.
        """
        raise NotImplementedError

    @classmethod
    async def update_object_by_params(
        cls, session: AsyncSession, filter_data: dict, update_data: dict
    ) -> None:
        """
        Обновляет объекты по параметрам.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        filter_data: Словарь с данными для фильтрации
        update_data: Словарь с данными для обновления

        Возвращает None
        """
        raise NotImplementedError

    @abstractmethod
    async def count_number_objects_by_params(
        self, session: AsyncSession, data: dict | None
    ) -> int:
        """
        Считает количество записей в таблице по параметрам.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Данные для фильтрации

        Возвращает количество записей в таблице.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_object_attrs_by_params(
        self, *attrs: str, session: AsyncSession, data: dict
    ) -> Row[tuple[Any]] | None:
        """
        Делает запрос только на запрашиваемые аттрибуты объекта

        attrs: Аттрибуты
        session: Сессия для асинхронной работы с базой данных
        data: Данные для фильтрации

        Возвращает аттрибуты объекта

        """
        raise NotImplementedError


class ManagerRepository(AbstractRepository):

    model: type[BaseModel] | None = None  # Модель базы данных

    @classmethod
    async def create_object(
        cls,
        session: AsyncSession,
        data: dict,
        exception_detail: str = OBJECT_NOT_CREATED_ERROR,
    ) -> int:

        stmt = insert(cls.model).values(**data).returning(cls.model.id)
        try:
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

        except IntegrityError as err:
            logger.exception(exception_detail)
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=exception_detail,
            )

    @classmethod
    async def update_object_by_params(
        cls, session: AsyncSession, filter_data: dict, update_data: dict
    ) -> bool:
        stmt = (
            update(cls.model)
            .filter_by(**filter_data)
            .values(**update_data)
            .returning(cls.model.id)
        )
        result = await session.execute(stmt)
        result = bool(result.fetchone())
        if result:
            await session.commit()
        return result

    @classmethod
    async def get_object_by_params(
        cls, session: AsyncSession, data: dict
    ) -> Optional[BaseModel]:
        query = select(cls.model).filter_by(**data)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_object_attrs_by_params(
        cls, *attrs: str, session: AsyncSession, data: dict
    ) -> Row[tuple[Any]] | None:
        query = select(
            *(getattr(cls.model, attr) for attr in attrs)
        ).filter_by(**data)
        result = await session.execute(query)
        return result.one_or_none()

    @classmethod
    async def count_number_objects_by_params(
        cls, session: AsyncSession, data: dict | None
    ) -> int:
        if data is None:
            data = {}
        query = select(func.count(cls.model.id)).filter_by(**data)
        return await session.scalar(query)

    @classmethod
    async def delete_object_by_params(
        cls,
        session: AsyncSession,
        data: dict,
    ) -> bool:
        stmt = delete(cls.model).filter_by(**data).returning(cls.model.id)
        result = await session.execute(stmt)
        result = bool(result.fetchone())
        if result is False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await session.commit()
        return result
