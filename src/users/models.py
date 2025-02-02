from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core import BaseModel


class UserModel(BaseModel):
    fullname: Mapped[str]
    email: Mapped[str] = mapped_column(String(32), default='Неуказано', server_default='Неуказано')
    phone: Mapped[str] = mapped_column(String(32), default='Неуказано', server_default='Неуказано')
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[bytes]
    is_admin: Mapped[bool] = mapped_column(default=False, server_default="0")
