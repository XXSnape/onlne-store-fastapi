from sqlalchemy.ext.asyncio import AsyncSession

from users.database.repositories.user import UserRepository
from users.exceptions.auth import unauthorized_error
from users.schemas.password import ChangePasswordSchema
from users.utils.auth import validate_password, get_hashed_password


async def change_user_password(
    session: AsyncSession,
    user_id: int,
    change_password_in: ChangePasswordSchema,
) -> None:
    password = await UserRepository.get_object_attrs_by_params(
        "password", session=session, data={"id": user_id}
    )
    if (
        validate_password(
            password=change_password_in.current_password,
            hashed_password=password[0],
        )
        is False
    ):
        raise unauthorized_error
    await UserRepository.update_object_by_params(
        session=session,
        filter_data={"id": user_id},
        update_data={
            "password": get_hashed_password(change_password_in.new_password)
        },
    )
