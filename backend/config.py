"""
Focus Friend - Centralized Configuration Module.
Type-safe environment management powered by Pydantic Settings.
Reads configuration from .env file or environment variables with resilient defaults.
"""

from pathlib import Path
from typing import List, Any
from pydantic import Field, field_validator

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseModel
    class BaseSettings(BaseModel):
        pass
    SettingsConfigDict = dict

# Base Directory Resolution
BASE_DIR: Path = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application settings schema, environment bindings, and default values."""

    # Application Identity & Lifecycle
    app_name: str = Field(
        default="Focus Friend",
        description="Public display name of the application."
    )
    app_env: str = Field(
        default="development",
        description="Runtime environment: development, staging, or production."
    )
    host: str = Field(
        default="127.0.0.1",
        description="Bind host address for the FastAPI / Uvicorn server."
    )
    port: int = Field(
        default=8501,
        description="Bind port for the FastAPI server and Web UI."
    )
    log_level: str = Field(
        default="INFO",
        description="Standard logger verbosity: DEBUG, INFO, WARNING, ERROR, CRITICAL."
    )

    # Local Ollama AI Settings (100% Local Inference)
    ollama_base_url: str = Field(
        default="http://127.0.0.1:11434",
        description="Base URL for the locally running Ollama inference daemon."
    )
    default_model: str = Field(
        default="phi3:mini",
        description="Default local model weights to use for distillation."
    )
    inference_timeout_seconds: int = Field(
        default=15,
        description="Maximum seconds to wait for local model generation before fallback."
    )
    enable_fallback_engine: bool = Field(
        default=True,
        description="Whether to permit zero-cloud local heuristic distillation if Ollama is unreachable."
    )

    # Security & Networking
    enable_cors: bool = Field(
        default=True,
        description="Enable cross-origin resource sharing headers."
    )
    cors_origins: List[str] = Field(
        default=["*"],
        description="Permitted origins for CORS headers."
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        """Supports comma-delimited strings, JSON arrays, or native Python lists."""
        if isinstance(v, str):
            v_trimmed = v.strip()
            if v_trimmed.startswith("[") and v_trimmed.endswith("]"):
                import json
                try:
                    return json.loads(v_trimmed)
                except Exception:
                    pass
            return [i.strip() for i in v_trimmed.split(",") if i.strip()]
        elif isinstance(v, list):
            return [str(item) for item in v]
        return ["*"]

    # Asset Directories
    frontend_dir: Path = Field(
        default=BASE_DIR / "frontend",
        description="Path to static frontend HTML/CSS/JS assets."
    )

    # Pydantic Settings Configuration
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    ) if SettingsConfigDict else {}


# Global Settings Singleton
settings: Settings = Settings()
