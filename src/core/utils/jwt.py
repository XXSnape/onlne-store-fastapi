from datetime import UTC, datetime, timedelta

import jwt

from core import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
) -> str:
    """
    Кодирует jwt-токен
    :param payload: полезная нагрузка в токене
    :param private_key: закрытый ключ
    :param algorithm: алгоритм шифрования
    :param expire_minutes: действие токена в минутах
    :return: токен доступа
    """
    to_encode = payload.copy()
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    """
    Декодирует jwt-токен
    :param token: токен доступа
    :param public_key: публичный ключ
    :param algorithm: алгоритм шифрования
    :return: данные токена
    """
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def get_access_token(user_id: int, username: str, is_admin: bool) -> str:
    """
    Создает токен доступа с полезной нагрузкой в виде id,
    username и статуса is_admin пользователя,
    которому принадлежит токен
    :param user_id: id пользователя
    :param username: username пользователя
    :param is_admin: является ли пользователь админом
    :return: токен доcтупа
    """
    payload = {
        "sub": str(user_id),
        "username": username,
        "is_admin": str(int(is_admin)),
    }
    token = encode_jwt(payload=payload)
    return token
