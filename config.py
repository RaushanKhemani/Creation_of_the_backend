from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Hub Backend"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True

    api_prefix: str = "/api/v1"
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"])

    database_url: str = "sqlite:///./ai_hub.db"

    jwt_secret_key: str = "change-me-in-env"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14

    api_key_encryption_key: str = "vhVTTqUt--9I61dFmhehjpkr_8z_zXbpOQxrF7b2gwg="

    rate_limit_requests_per_minute: int = 60

    provider_timeout_seconds: int = 20
    provider_max_retries: int = 2

    openai_api_key: str | None = None
    google_api_key: str | None = None
    anthropic_api_key: str | None = None
    xai_api_key: str | None = None

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, str):
            if value.startswith("["):
                import json

                return json.loads(value)
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value: bool | str) -> bool:
        if isinstance(value, bool):
            return value
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on", "dev", "development"}:
            return True
        if lowered in {"0", "false", "no", "off", "prod", "production", "release"}:
            return False
        return False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
