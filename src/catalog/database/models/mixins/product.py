from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

if TYPE_CHECKING:
    from catalog.database.models.product import ProductModel


class ProductRelationshipMixin:
    _is_unique_product = False
    _on_delete_product = "CASCADE"
    _back_populates: str | None = None

    @declared_attr
    def product_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("products.id"),
            unique=cls._is_unique_product,
        )

    @declared_attr
    def product(cls) -> Mapped["ProductModel"]:
        return relationship(
            "ProductModel",
            back_populates=cls._back_populates,
        )
