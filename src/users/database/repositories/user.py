from sqlalchemy import select, Row, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, load_only

from core import ManagerRepository
from users.database import UserModel


class UserRepository(ManagerRepository):
    model = UserModel

    @classmethod
    async def get_user_profile(
        cls, session: AsyncSession, user_id: int
    ) -> ScalarResult[UserModel]:
        query = (
            select(cls.model)
            .options(
                load_only(
                    cls.model.fullname,
                    cls.model.email,
                    cls.model.phone,
                    cls.model.username,
                ),
                joinedload(cls.model.avatar),
            )
            .filter_by(id=user_id)
        )
        result = await session.execute(query)
        # print(result.all())
        res = result.unique().scalars().one_or_none()
        print("res", res)
        return res
