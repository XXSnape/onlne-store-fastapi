from datetime import date


from sqlalchemy import Date, func, CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from core import BaseModel, price_decimal
from .product_mixin import ProductRelationshipMixin


class SaleModel(ProductRelationshipMixin, BaseModel):
    _is_unique = True
    _back_populates_value = "sale"

    sale_price: Mapped[price_decimal]
    date_from: Mapped[date] = mapped_column(
        Date, server_default=func.current_date()
    )
    date_to: Mapped[date]

    __table_args__ = (CheckConstraint("date_from < date_to"),)

    @hybrid_property
    def images(self):
        return self.product.images
