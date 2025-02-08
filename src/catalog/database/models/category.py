from typing import TYPE_CHECKING, Final

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import BaseModel, ImageModelMixin

if TYPE_CHECKING:
    from .product import ProductModel
    from .tag import TagModel

DIRECTORY_OF_IMAGES: Final[str] = "categories"


class CategoryModel(BaseModel):
    __tablename__ = "categories"
    number_output_fields = 8

    title: Mapped[str]
    image: Mapped["CategoryImageModel"] = relationship(
        back_populates="category"
    )
    products: Mapped[list["ProductModel"]] = relationship(
        back_populates="category"
    )
    tags: Mapped[list["TagModel"]] = relationship(
        secondary="tags_categories_association", back_populates="categories"
    )

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), default=None
    )
    children: Mapped[list["CategoryModel"]] = relationship("CategoryModel")


class CategoryImageModel(BaseModel, ImageModelMixin):
    _directory = DIRECTORY_OF_IMAGES
    __tablename__ = "category_images"
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), unique=True
    )
    category: Mapped["CategoryModel"] = relationship(back_populates="image")
