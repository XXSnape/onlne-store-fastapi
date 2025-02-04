from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import BaseModel

if TYPE_CHECKING:
    from .product import ProductModel


class SpecificationModel(BaseModel):
    name: Mapped[str]
    value: Mapped[str]
    products: Mapped[list["ProductModel"]] = relationship(
        secondary="specifications_products_association",
        back_populates="specifications",
    )


class SpecificationProductModel(BaseModel):
    __tablename__ = "specifications_products_association"
    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "specification_id",
            name="idx_uniq_product_specification",
        ),
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE")
    )
    specification_id: Mapped[int] = mapped_column(
        ForeignKey("specifications.id", ondelete="CASCADE")
    )
