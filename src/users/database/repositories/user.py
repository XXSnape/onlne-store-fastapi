from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, defer

from core import ManagerRepository
from users.database import UserModel


class UserRepository(ManagerRepository):
    model = UserModel

    @classmethod
    async def get_user_profile(
        cls, session: AsyncSession, user_id: int
    ) -> UserModel | None:
        query = (
            select(cls.model)
            .options(
                defer(
                    cls.model.password,
                ),
                defer(
                    cls.model.is_admin,
                ),
                joinedload(cls.model.avatar),
            )
            .filter_by(id=user_id)
        )
        result = await session.execute(query)
        res = result.unique().scalars().one_or_none()
        return res
