import os
from typing import ClassVar

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class ApiV1Prefix(BaseModel):
    prefix: str = ""
    auth: str = "/auth"
    users: str = "/users"
    send_coin: str = "/sendCoin"
    buy: str = "/buy"
    info: str = "/info"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def bearer_token_url(self) -> str:
        # api/auth/login
        parts = (
            self.prefix,
            self.v1.prefix,
            self.v1.auth,
            "/login",
        )
        path = "".join(parts)
        return path.removeprefix("/")


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    pool_recycle: int = 1800

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class Settings(BaseSettings):
    # Определяем, какой .env использовать
    env_file: ClassVar[str] = (
        ".env.docker" if os.getenv("DOCKER_ENV") == "true" else ".env"
    )
    # Логирование того, какой файл .env будет использоваться
    print(f"Using environment file: {env_file}")
    model_config = SettingsConfigDict(
        # env_file=(".env", "avito/.env"),
        env_file=env_file,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    access_token: AccessToken
    jwt_secret_key: str


settings = Settings()
print(f"Using database: {settings.db.url}")  # Для проверки, какой URL загрузился
