from core import db_helper, logger, settings
from users.database.repositories.user import UserRepository
from users.utils.auth import get_hashed_password


async def create_admin_if_not_exists():
    async with db_helper.session_factory() as session:
        user = await UserRepository.get_object_by_params(
            session=session, data={"username": settings.app.admin_login}
        )
        if not user:
            logger.info("Админ не был создан")
            result = await UserRepository.create_object(
                session=session,
                data={
                    "fullname": settings.app.admin_name,
                    "username": settings.app.admin_login,
                    "password": get_hashed_password(
                        password=settings.app.admin_password
                    ),
                    "is_admin": True,
                },
            )
            if result:
                logger.info("Админ успешно создан")
                return
            logger.info("Админ не был успешно создан")
            return
        logger.info("Админ уже был создан")
