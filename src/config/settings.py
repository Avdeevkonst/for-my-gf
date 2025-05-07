from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PG_HOST: str = "postgres"
    PG_PORT: str = "5432"
    PG_NAME: str = ""
    PG_USER: str = "postgres"
    PG_PASS: str = ""

    REDIS_HOST: str = "redis"
    REDIS_PORT: str = "6379"

    MINIO_ENDPOINT: str = "minio"
    MINIO_ACCESS_KEY: str = "minio"
    MINIO_SECRET_KEY: str = "minio"  # noqa: S105

    MINIO_SECURE: bool = True

    ADMIN_SECRET_KEY: str = ""

    MINIO_PUBLIC_BUCKET: str = "public"

    BOT_TOKEN: str = ""

    ECHO: bool = True

    @property
    def db_url_postgresql(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}"

    @property
    def db_url_redis(self) -> str:
        return f"redis://@{self.REDIS_HOST}:{self.REDIS_PORT}/"


settings = Settings()  # pyright: ignore[reportCallIssue]
