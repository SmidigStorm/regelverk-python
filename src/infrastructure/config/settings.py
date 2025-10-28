"""
Application settings using Pydantic Settings.

Loads configuration from environment variables with type safety and validation.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    # Environment
    ENV: str = "development"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./regelverk.db"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Singleton settings instance
settings = Settings()
