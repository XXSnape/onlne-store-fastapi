from decimal import Decimal

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from catalog.database.models.mixins.product import ProductRelationshipMixin
from core import BaseModel, creation_time, price_decimal
from orders.utils.constants import (
    DeliveryTypeEnum,
    PaymentTypeEnum,
    OrderStatusEnum,
)


from users.database.models.mixins.user import UserRelationshipMixin


class OrderModel(UserRelationshipMixin, BaseModel):
    _back_populates = "orders"
    created_at: Mapped[creation_time]
    delivery_type: Mapped[DeliveryTypeEnum | None] = mapped_column(
        default=None
    )
    payment_type: Mapped[PaymentTypeEnum | None] = mapped_column(default=None)
    status: Mapped[OrderStatusEnum] = mapped_column(
        default=OrderStatusEnum.unpaid, server_default=OrderStatusEnum.unpaid
    )
    city: Mapped[str | None] = mapped_column(default=None)
    address: Mapped[str | None] = mapped_column(default=None)
    products: Mapped[list["OrderProductModel"]] = relationship(
        back_populates="order"
    )
    total_cost: Mapped[price_decimal | None] = mapped_column(default=None)

    @hybrid_property
    def fullname(self):
        return self.user.fullname

    @hybrid_property
    def email(self):
        return self.user.email

    @hybrid_property
    def phone(self):
        return self.user.phone


class OrderProductModel(ProductRelationshipMixin, BaseModel):
    _back_populates = "orders"

    __tablename__ = "orders_products_association"
    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "order_id",
            name="idx_uniq_order_product",
        ),
    )
    count: Mapped[int]
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE")
    )
    order: Mapped["OrderModel"] = relationship(back_populates="products")

    @hybrid_property
    def price(self) -> Decimal:
        return self.product.price

    @hybrid_property
    def rating(self) -> float:
        return self.product.rating

    @hybrid_property
    def tags(self):
        return self.product.tags

    @hybrid_property
    def reviews(self):
        return self.product.reviews_count

    @hybrid_property
    def title(self):
        return self.product.title

    @hybrid_property
    def date(self):
        return self.product.date

    @hybrid_property
    def description(self):
        return self.product.description

    @hybrid_property
    def free_delivery(self):
        return self.product.free_delivery

    @hybrid_property
    def category(self):
        return self.product.category_id

    @hybrid_property
    def images(self):
        return self.product.images
