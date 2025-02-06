import statistics
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Text,
    ForeignKey,
    CheckConstraint,
    type_coerce,
    ColumnElement,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core import BaseModel, price_decimal, creation_time
from catalog.database.models.review import ReviewModel
from catalog.database.models.speciification import SpecificationModel
from sqlalchemy import Numeric

if TYPE_CHECKING:
    from .product_image import ProductImageModel
    from .category import CategoryModel
    from .sale import SaleModel
    from .speciification import SpecificationModel


class ProductModel(BaseModel):
    __table_args__ = (
        CheckConstraint("count >= 0"),
        CheckConstraint("price_per_unit >= 0"),
    )
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
        secondary="specifications_products_association",
        back_populates="products",
    )
    reviews: Mapped[list["ReviewModel"]] = relationship(
        back_populates="product"
    )

    @hybrid_property
    def price(self) -> Decimal:
        if self.sale:
            return self.sale.sale_price
        return self.price_per_unit

    @hybrid_property
    def rating(self) -> float:
        if not self.reviews:
            return 0
        return statistics.mean(review.rate for review in self.reviews)

    @hybrid_property
    def tags(self):
        return [tag for tag in self.category.tags]

    @hybrid_property
    def reviews_count(self):
        return len(self.reviews)
