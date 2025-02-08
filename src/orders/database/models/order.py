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

    def __getattr__(self, item: str):
        if item.startswith("_"):
            return super().getattr(item)
        if item == "category":
            return getattr(super().__getattribute__("product"), "category_id")
        if item == "reviews":
            return getattr(
                super().__getattribute__("product"), "reviews_count"
            )
        return getattr(super().__getattribute__("product"), item)
