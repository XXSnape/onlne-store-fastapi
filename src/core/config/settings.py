from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()
BASE_DIR = Path(__file__).parent.parent


class RedisSettings(BaseSettings):
    """
    redis_host - хост редиса
    """

    redis_host: str

    @property
    def url(self) -> str:
        """
        Возвращает строку для подключения к редису.
        """
        return f"redis://{self.redis_host}"


class AppSettings(BaseSettings):
    cookie_key_card: str = "card-id"
    limit: int = 2


class AuthJWTSettings(BaseSettings):
    """
    private_key_path - путь к закрытому ключу
    public_key_path - путь к открытому ключу
    access_token_expire_minutes - действие токена в минутах
    algorithm - алгоритм шифрования
    """

    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    access_token_expire_minutes: int = 30
    algorithm: str = "RS256"
    cookie_key_token: str = "access-token"


class DBSettings(BaseSettings):
    """
    db_host: хост базы
    db_port: порт базы
    postgres_user: логин пользователя
    postgres_password: пароль пользователя
    postgres_db: название базы
    echo: bool = True, если нужно, чтобы запросы выводились в консоль, иначе False
    """

    db_host: str
    db_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    echo: bool = True

    @property
    def url(self) -> str:
        """
        Возвращает строку для подключения к базе данных.
        """
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.db_host}:{self.db_port}/{self.postgres_db}"
        )


class Settings(BaseSettings):
    """
    Настройки приложения
    """

    model_config = SettingsConfigDict(
        case_sensitive=False,
    )
    db: DBSettings = DBSettings()
    auth_jwt: AuthJWTSettings = AuthJWTSettings()
    app: AppSettings = AppSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
