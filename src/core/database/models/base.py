"""
Модуль с абстрактным классом Base.
"""

import datetime
from decimal import Decimal
from typing import TypeAlias

from sqlalchemy import Numeric, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)
from typing_extensions import Annotated

price_decimal: TypeAlias = Annotated[Decimal, mapped_column(Numeric(10, 4))]
creation_time: TypeAlias = Annotated[
    datetime.datetime,
    mapped_column(
        default=datetime.datetime.now,
        server_default=func.now(),
    ),
]


class BaseModel(DeclarativeBase):
    """
    Абстрактный класс для работы с моделями.
    """

    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

    number_output_fields = 3

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Возвращает название таблицы по имени модели.
        """
        return f"{cls.__name__.lower()[:-len('Model')]}s"

    def __repr__(self) -> str:
        """
        Возвращает строку с первыми 3 колонками и значениями.
        """
        cols = [
            f"{field}={getattr(self, field)}"
            for field in self.__table__.columns.keys()[
                : self.number_output_fields
            ]
        ]

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
