from sqlalchemy.ext.asyncio import AsyncSession

from users.database.repositories.user import UserRepository
from users.schemas.profile import ProfileInSchema, ProfileSchema


async def get_user_profile(session: AsyncSession, user_id: int):
    user = await UserRepository.get_user_profile(
        session=session, user_id=user_id
    )
    return ProfileSchema.model_validate(user, from_attributes=True)


async def update_user_profile(
    session: AsyncSession, user_id: int, profile_in: ProfileInSchema
):

    await UserRepository.update_object_by_params(
        session=session,
        update_data=profile_in.model_dump(),
        filter_data={"id": user_id},
    )
