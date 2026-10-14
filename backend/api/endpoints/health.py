"""
Focus Friend - Health & System Status Endpoint Router.
Scalable probe for backend availability and local inference status.
"""

from fastapi import APIRouter
from backend.api.schemas.response_schemas import HealthStatusResponse
from backend.services.ollama_service import OllamaService
from backend.config import settings

router = APIRouter(prefix="/health", tags=["Health & Status"])


@router.get(
    "",
    response_model=HealthStatusResponse,
    summary="Get Focus Friend health and local inference daemon status"
)
def get_health_status():
    """Returns local service status, active model, and engine availability."""
    ollama_info = OllamaService.check_health()
    return HealthStatusResponse(
        status="ok",
        app=settings.app_name,
        version="1.0.0",
        ollama_connected=ollama_info["connected"],
        active_model=ollama_info["active_model"],
        fallback_engine_available=settings.enable_fallback_engine,
    )
