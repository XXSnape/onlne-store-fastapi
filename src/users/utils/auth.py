import bcrypt


def get_hashed_password(
    password: str,
) -> bytes:
    """
    Хэширует пароль
    :param password: пароль
    :return: хэшированный пароль
    """
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    """
    Сравнивает пароли
    :param password: пароль
    :param hashed_password: хэшированный пароль
    :return: результат сравнения
    """
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
