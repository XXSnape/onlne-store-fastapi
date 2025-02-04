from datetime import date


from sqlalchemy import Date, func, CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from core import BaseModel, price_decimal
from products.database.models.mixins.product import ProductRelationshipMixin


class SaleModel(ProductRelationshipMixin, BaseModel):
    _is_unique_product = True
    _back_populates = "sale"

    __table_args__ = (
        CheckConstraint("date_from < date_to"),
        CheckConstraint("sale_price >= 0"),
    )

    sale_price: Mapped[price_decimal]
    date_from: Mapped[date] = mapped_column(
        Date, default=date.today, server_default=func.current_date()
    )
    date_to: Mapped[date]

    @hybrid_property
    def images(self):
        return self.product.images

    @hybrid_property
    def price(self):
        return self.product.price_per_unit

    @hybrid_property
    def title(self):
        return self.product.title
