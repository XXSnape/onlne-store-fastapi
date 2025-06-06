from sqlalchemy import TEXT, CheckConstraint, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from catalog.database.models.mixins.product import ProductRelationshipMixin
from core import BaseModel, creation_time
from users.database.models.mixins.user import UserRelationshipMixin


class ReviewModel(
    ProductRelationshipMixin,
    UserRelationshipMixin,
    BaseModel,
):
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
    text: Mapped[str] = mapped_column(TEXT)
    date: Mapped[creation_time]

    @hybrid_property
    def author(self):
        return self.user.username

    @hybrid_property
    def email(self):
        return self.user.email
