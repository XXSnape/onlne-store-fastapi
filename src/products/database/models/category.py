from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import BaseModel
from products.database.models.product import ProductModel

if TYPE_CHECKING:
    from .product import ProductModel


class CategoryModel(BaseModel):
    __tablename__ = "categories"
    title: Mapped[str]
    image: Mapped["CategoryImageModel"] = relationship(
        back_populates="category"
    )
    products: Mapped[list["ProductModel"]] = relationship(
        back_populates="category"
    )


class CategoryImageModel(BaseModel):
    __tablename__ = "category_images"
    src: Mapped[str]
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), unique=True
    )
    category: Mapped["CategoryModel"] = relationship(back_populates="image")
