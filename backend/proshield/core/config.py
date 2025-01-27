import enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class ENVIROMENT(enum.StrEnum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # api version
    API_V1_STR: str = "/api/v1"

    # environment
    ENVIRONMENT: str = ENVIROMENT.DEVELOPMENT

    # database settings
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@database:5432"


settings = Settings()
