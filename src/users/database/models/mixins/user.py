from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

if TYPE_CHECKING:
    from users.database.models.user import UserModel


class UserRelationshipMixin:
    _is_unique_user: bool = False
    _back_populates: str | None = None
    _on_delete_user: str = "CASCADE"

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("users.id", ondelete=cls._on_delete_user),
            unique=cls._is_unique_user,
        )

    @declared_attr
    def user(cls) -> Mapped["UserModel"]:
        return relationship(
            "UserModel",
            back_populates=cls._back_populates,
        )
