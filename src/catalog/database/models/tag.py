from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import BaseModel

if TYPE_CHECKING:
    from .category import CategoryModel


class TagModel(BaseModel):
    name: Mapped[str]
    categories: Mapped[list["CategoryModel"]] = relationship(
        secondary="tags_categories_association", back_populates="tags"
    )


class TagCategoryModel(BaseModel):
    __tablename__ = "tags_categories_association"
    __table_args__ = (
        UniqueConstraint(
            "category_id",
            "tag_id",
            name="idx_uniq_category_tag",
        ),
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE")
    )
