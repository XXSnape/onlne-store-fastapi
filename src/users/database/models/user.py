from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import BaseModel

if TYPE_CHECKING:
    from catalog.database.models.review import ReviewModel
    from orders.database import OrderModel

    from .avatar import AvatarModel


class UserModel(BaseModel):
    fullname: Mapped[str]
    email: Mapped[str] = mapped_column(
        String(32), default="Не указано", server_default="Не указано"
    )
    phone: Mapped[str] = mapped_column(
        String(32), default="Не указано", server_default="Не указано"
    )
    username: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[bytes]
    is_admin: Mapped[bool] = mapped_column(default=False, server_default="0")
    avatar: Mapped["AvatarModel"] = relationship(back_populates="user")
    reviews: Mapped[list["ReviewModel"]] = relationship(back_populates="user")
    orders: Mapped[list["OrderModel"]] = relationship(back_populates="user")
