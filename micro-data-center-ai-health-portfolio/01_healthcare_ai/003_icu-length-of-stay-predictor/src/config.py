"""Configuration for ICU Length of Stay Predictor."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    app_name: str = "ICU Length of Stay Predictor"
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    model_version: str = Field(default="prototype", alias="MODEL_VERSION")
    prediction_threshold: float = Field(default=0.5, alias="PREDICTION_THRESHOLD")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings."""

    return Settings()


PROJECT_PACKAGE = "icu_length_of_stay_predictor"
