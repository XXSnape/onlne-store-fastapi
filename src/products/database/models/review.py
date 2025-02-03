from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped

from core import BaseModel
from products.database.models.mixins.product import ProductRelationshipMixin
from users.database.models.mixins.user import UserRelationshipMixin


class ReviewModel(
    ProductRelationshipMixin,
    UserRelationshipMixin,
    BaseModel,
):
    _on_delete_user = "SET NULL"
    __table_args__ = (
        CheckConstraint("rate >= 1 and rate <= 5"),
        UniqueConstraint(
            "user_id",
            "product_id",
            name="idx_uniq_user_product",
        ),
    )

    _back_populates = "reviews"
    rate: Mapped[int]
