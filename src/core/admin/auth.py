from jwt import InvalidTokenError
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from core import db_helper, logger, settings
from core.utils.jwt import decode_jwt, get_access_token
from users.database.repositories.user import UserRepository
from users.utils.auth import validate_password


class AdminAuth(AuthenticationBackend):
    async def login(
        self,
        request: Request,
    ) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        async with db_helper.session_factory() as session:
            user = await UserRepository.get_object_attrs_by_params(
                "id",
                "is_admin",
                "password",
                session=session,
                data={"username": username},
            )
            if (
                not user
                or not validate_password(
                    password=password, hashed_password=user.password
                )
                or not user.is_admin
            ):
                logger.warning(
                    "Попытка войти в административную панель не удалась",
                    extra={"username": username},
                )
                return False
            token = get_access_token(
                user_id=user.id, username=username, is_admin=user.is_admin
            )
            request.session.update({settings.auth_jwt.cookie_key_token: token})
            logger.info(
                "Выполнен вход в административную панель",
                extra={"username": username},
            )

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        logger.info("Выполнен выход их административной панели")
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get(settings.auth_jwt.cookie_key_token)
        if not token:
            logger.warning(
                "Попытка войти в административную панель без токена"
            )
            return False
        try:
            payload = decode_jwt(
                token=token,
            )
            if int(payload["is_admin"]) == 1:
                logger.info(
                    "Выполнен вход в административную панель",
                    extra={**payload},
                )
                return True
            logger.warning(
                "Попытка войти в административную панель не от админа",
                extra={**payload},
            )
            return False
        except InvalidTokenError as e:
            logger.exception(
                "Попытка войти в административную панель с невалидным токеном",
                extra={"token": token},
            )
            return False
