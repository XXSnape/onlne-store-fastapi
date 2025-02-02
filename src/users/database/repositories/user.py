from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import ManagerRepository
from users.database import UserModel


class UserRepository(ManagerRepository):
    model = UserModel

    # @classmethod
    # def get_username(cls, session: AsyncSession, user_id: int):
    #     query = select(cls.model.username)
