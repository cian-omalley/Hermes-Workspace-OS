"""Worker configuration (environment-driven)."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkerSettings(BaseSettings):
    """Celery/worker runtime settings from the environment."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    celery_broker_url: str = Field(default="redis://localhost:6379/1")
    celery_result_backend: str = Field(default="redis://localhost:6379/2")


@lru_cache
def get_worker_settings() -> WorkerSettings:
    return WorkerSettings()
