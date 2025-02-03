from typing import TYPE_CHECKING

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core import BaseModel, price_decimal, creation_time
from products.database.models.review import ReviewModel
from products.database.models.speciification import SpecificationModel

if TYPE_CHECKING:
    from .product_image import ProductImageModel
    from .category import CategoryModel
    from .sale import SaleModel
    from .speciification import SpecificationModel


class ProductModel(BaseModel):
    title: Mapped[str]
    price_per_unit: Mapped[price_decimal]
    count: Mapped[int]
    date: Mapped[creation_time]
    description: Mapped[str] = mapped_column(
        default="Нет описания", server_default="Нет описания"
    )
    full_description: Mapped[str] = mapped_column(
        Text,
        default="Нет полного описания",
        server_default="Нет полного описания",
    )
    free_delivery: Mapped[bool] = mapped_column(
        default=False, server_default="0"
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL")
    )
    images: Mapped[list["ProductImageModel"]] = relationship(
        back_populates="product"
    )
    category: Mapped["CategoryModel"] = relationship(back_populates="products")
    sale: Mapped["SaleModel"] = relationship(back_populates="product")
    specifications: Mapped[list["SpecificationModel"]] = relationship(
        back_populates="product"
    )
    reviews: Mapped[list["ReviewModel"]] = relationship(
        back_populates="product"
    )
