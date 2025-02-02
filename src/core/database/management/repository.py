"""
Модуль с абстрактными репозиториями для работы с таблицами базы данных.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from fastapi import HTTPException, status
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

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
        commit_need: bool = True,
    ) -> int:
        """
        Добавляет новый объект в базу данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, которые должны быть добавлены в базу

        exception_detail: Сообщение об ошибке, которое возникает во всех случаях,
        когда не удается создать объект

        exception_foreign_constraint_detail: Сообщение об ошибке,
        которое возникает из-за ограничений внешнего ключа

        commit_need: Принимает значения True или False.
        Если установлен в True, то изменения будут сохранены в базе. По умолчанию True.

        Возвращает идентификатор добавленной записи.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_object_by_params(
        self,
        session: AsyncSession,
        data: dict,
        commit_need=True,
    ) -> bool:
        """
        Удаляет объекты из базы данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, по которым будет осуществлен поиск объектов для удаления

        exception_detail: Сообщение об ошибке, которое возникает в случаях, когда объект не был удален

        commit_need: Принимает значения True или False.
        Если установлен в True, то изменения будут сохранены в базе. По умолчанию True.

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

    @abstractmethod
    async def get_object_id_by_params(
        self, session: AsyncSession, data: dict
    ) -> bool:
        """
        Ищет объект в базе данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, по которым будет осуществлен поиск объекта

        Возвращает True, если объект существует, и False в противном случае.
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
        self, session: AsyncSession, data: dict
    ) -> int:
        """
        Считает количество записей в таблице.

        Параметры:

        session: Сессия для асинхронной работы с базой данных

        Возвращает количество записей в таблице.
        """
        raise NotImplementedError


class ManagerRepository(AbstractRepository):
    """
    Класс - репозиторий, реализующий все методы абстрактного класса.
    """

    model = None  # Модель базы данных

    @classmethod
    async def create_object(
        cls,
        session: AsyncSession,
        data: dict,
        exception_detail: str = OBJECT_NOT_CREATED_ERROR,
        commit_need: bool = True,
    ) -> int:
        """
        Добавляет новый объект в базу данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, которые должны быть добавлены в базу

        exception_detail: Сообщение об ошибке, которое возникает во всех случаях,
        когда не удается создать объект

        exception_foreign_constraint_detail: Сообщение об ошибке,
        которое возникает из-за ограничений внешнего ключа

        commit_need: Принимает значения True или False.
        Если установлен в True, то изменения будут сохранены в базе. По умолчанию True.

        Возвращает идентификатор добавленной записи.
        """
        stmt = insert(cls.model).values(**data).returning(cls.model.id)
        try:
            result = await session.execute(stmt)
            if commit_need:
                await session.commit()
            return result.scalar_one()

        except IntegrityError as err:
            print(err)
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=exception_detail,
            )

    @classmethod
    async def delete_object_by_params(
        cls,
        session: AsyncSession,
        data: dict,
        commit_need=True,
    ) -> bool:
        """
        Удаляет объекты из базы данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, по которым будет осуществлен поиск объектов для удаления

        exception_detail: Сообщение об ошибке, которое возникает в случаях, когда объект не был удален

        commit_need: Принимает значения True или False.
        Если установлен в True, то изменения будут сохранены в базе. По умолчанию True.

        Возвращает True, если объекты были удалены и False в противном случае.
        """
        stmt = delete(cls.model).filter_by(**data).returning(cls.model.id)
        result = await session.execute(stmt)
        result = bool(result.fetchone())
        if commit_need:
            await session.commit()
        return result

    @classmethod
    async def update_object_by_params(
        cls, session: AsyncSession, filter_data: dict, update_data: dict
    ) -> bool:
        """
        Обновляет объекты по параметрам.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        filter_data: Словарь с данными для фильтрации
        update_data: Словарь с данными для обновления

        Возвращает None
        """
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
    ) -> Optional[model]:
        """
        Ищет объект в базе данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, по которым будет осуществлен поиск объекта

        Возвращает объект базы данных или None.
        """
        query = select(cls.model).filter_by(**data)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_object_id_by_params(
        cls, session: AsyncSession, data: dict
    ) -> int | None:
        """
        Ищет объект в базе данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, по которым будет осуществлен поиск объекта

        Возвращает True, если объект существует, и False в противном случае.
        """
        query = select(cls.model.id).filter_by(**data).limit(1)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def count_number_objects_by_params(
        cls, session: AsyncSession, data: dict
    ) -> int:
        """
        Считает количество записей в таблице.

        Параметры:

        session: Сессия для асинхронной работы с базой данных

        Возвращает количество записей в таблице.
        """
        query = select(func.count(cls.model.id)).filter_by(**data)
        return await session.scalar(query)

    @classmethod
    async def get_object_attrs_by_params(
        cls, *attrs: str, session: AsyncSession, data: dict
    ):
        query = select(
            *(getattr(cls.model, attr) for attr in attrs)
        ).filter_by(**data)
        result = await session.execute(query)
        return result.one_or_none()
