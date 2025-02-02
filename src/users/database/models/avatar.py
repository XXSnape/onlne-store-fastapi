from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from core import BaseModel


if TYPE_CHECKING:
    from .user import UserModel


class AvatarModel(BaseModel):
    src: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    user: Mapped["UserModel"] = relationship(back_populates="avatar")

    @hybrid_property
    def alt(self) -> str:
        filename = self.src.split("/")[-1]
        return f"{self.user_id}_{filename}"
