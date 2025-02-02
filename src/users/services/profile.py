from sqlalchemy.ext.asyncio import AsyncSession

from users.database.repositories.user import UserRepository
from users.schemas.profile import ProfileSchema


async def get_user_profile(session: AsyncSession, user_id: int):
    user = await UserRepository.get_user_profile(
        session=session, user_id=user_id
    )
    return ProfileSchema.model_validate(user, from_attributes=True)
