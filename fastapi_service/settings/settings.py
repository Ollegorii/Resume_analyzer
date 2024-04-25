__all__ = "settings"

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class S3(BaseSettings):
    class Config:
        env_prefix = "S3_"

    bucket_name: str = "hhbucket"


class Redis(BaseSettings):
    class Config:
        env_prefix = "REDIS_"

    host: str = "localhost"
    port: int = 6379
    db: int = 1


class UvicornURL(BaseSettings):
    """Represents Uvicorn settings"""

    class Config:
        env_prefix = "UVICORN_"

    host: str = "127.0.0.1"
    port: str = "8000"


class ProjectSettings(BaseSettings):
    """Represents Project settings"""

    class Config:
        env_prefix = "SETTINGS_"

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str = "fastapi_base"
    log_file: bool = False



class Settings(BaseSettings):
    api: UvicornURL = UvicornURL()
    project: ProjectSettings = ProjectSettings()
    redis: Redis = Redis()
    s3: S3 = S3()


@lru_cache
def get_settings() -> Settings:
    """Singleton"""
    return Settings()


settings = get_settings()
