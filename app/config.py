from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


Base_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    # jwt
    ALGORITHM: str
    SECRET_KEY: str
    # app
    debug: bool = False
    app_name: str = "Blog platform"

    model_config = SettingsConfigDict(
        env_file=Base_DIR / ".env", env_file_encoding="utf-8", case_sensitive=False
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
