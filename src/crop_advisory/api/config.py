"""
Typed Application Settings using Pydantic Settings.
Reads environment variables with prefix 'CROP_ADVISORY_' and fallback to .env.
"""

from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from crop_advisory.config import ARTIFACTS_DIR, BASE_DIR, DATASETS_DIR, MODELS_DIR


class APISettings(BaseSettings):
    """Configuration settings for the FastAPI backend service."""

    model_config = SettingsConfigDict(
        env_prefix="CROP_ADVISORY_",
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Core Application Metadata
    app_name: str = "Smart Crop Advisory API"
    app_version: str = "1.0.0"
    app_env: str = Field(
        default="development", description="Environment mode: development, testing, production"
    )
    debug: bool = Field(default=False, description="Enable debug mode and detailed traces")
    api_v1_prefix: str = "/api/v1"

    # Server Bind Settings
    host: str = "0.0.0.0"
    port: int = 8000

    # Security & CORS
    allowed_cors_origins: List[str] = Field(default_factory=lambda: ["*"])
    allowed_hosts: List[str] = Field(default_factory=lambda: ["*"])

    # Concurrency and Performance
    max_inference_concurrency: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum concurrent CPU-bound inference worker threads",
    )
    request_timeout_seconds: float = Field(
        default=30.0, description="Timeout for external network requests"
    )

    # Logging
    log_level: str = "INFO"

    # Filesystem Paths
    datasets_dir: Path = DATASETS_DIR
    artifacts_dir: Path = ARTIFACTS_DIR
    models_dir: Path = MODELS_DIR


# Cached settings instance
api_settings = APISettings()
