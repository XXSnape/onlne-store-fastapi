from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from core import BaseModel


if TYPE_CHECKING:
    from .user import UserModel


class AvatarModel(BaseModel):
    src: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped["UserModel"] = relationship(back_populates="avatar")
