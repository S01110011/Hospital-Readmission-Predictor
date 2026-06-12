"""Application configuration."""

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    app_env: str = Field(default="development", alias="APP_ENV")
    model_path: Path = Field(default=Path("artifacts/model.joblib"), alias="MODEL_PATH")
    metrics_path: Path = Field(default=Path("artifacts/metrics.json"), alias="METRICS_PATH")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    prediction_threshold: float = Field(default=0.5, alias="PREDICTION_THRESHOLD", ge=0, le=1)
    model_version: str = Field(default="local", alias="MODEL_VERSION")
    allowed_origins: str = Field(default="", alias="ALLOWED_ORIGINS")
    enable_docs: bool = Field(default=True, alias="ENABLE_DOCS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        """Return configured CORS origins as a list."""

        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
