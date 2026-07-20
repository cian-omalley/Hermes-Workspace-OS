"""Application configuration (12-factor, environment-driven).

Only the settings needed for the Milestone 1 skeleton are defined here; later
milestones extend this with database, provider, and secret configuration. See
``docs/PROJECT_BIBLE/08_Development/Deployment.md``.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings, populated from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    hermes_env: str = Field(default="development")
    log_level: str = Field(default="info")

    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    # Comma-separated origins; parsed into a list by ``cors_origins``.
    api_cors_origins: str = Field(default="http://localhost:3000")

    # Database connection. Defaults to a local SQLite file so the API can boot with
    # zero external services in development; the compose stack overrides this with the
    # PostgreSQL DSN (the production source of record). See Database_Architecture.md.
    database_url: str = Field(default="sqlite+pysqlite:///./hermes.db")

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.api_cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()
