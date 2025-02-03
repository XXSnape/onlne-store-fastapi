from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .product import ProductModel


class ProductRelationshipMixin:
    _is_unique = False
    _back_populates_value = None

    @declared_attr
    def product_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("products.id"),
            unique=cls._is_unique,
        )

    @declared_attr
    def product(cls) -> Mapped["ProductModel"]:
        return relationship(
            "ProductModel",
            back_populates=cls._back_populates_value,
        )
