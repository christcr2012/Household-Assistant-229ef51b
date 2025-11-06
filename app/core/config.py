from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="assistant_", env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./assistant.db"
    openai_api_key: str | None = None
    default_provider_scopes: dict[str, list[str]] = {
        "google": [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.modify",
            "https://www.googleapis.com/auth/drive.file",
        ],
        "apple": [
            "caldav",
            "imap",
            "smtp",
        ],
    }
    token_refresh_margin_seconds: int = 300


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()
