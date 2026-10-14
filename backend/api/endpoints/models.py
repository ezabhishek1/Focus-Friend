"""
Focus Friend - Models Endpoint Router.
Enumerates local open-weight model weights installed in local Ollama daemon.
"""

from fastapi import APIRouter
from backend.api.schemas.response_schemas import ModelsResponse
from backend.services.ollama_service import OllamaService

router = APIRouter(prefix="/models", tags=["Models"])


@router.get(
    "",
    response_model=ModelsResponse,
    summary="List installed local models from Ollama"
)
def list_models():
    """Lists local models downloaded on the host machine."""
    ollama_info = OllamaService.check_health()
    return ModelsResponse(
        connected=ollama_info["connected"],
        models=ollama_info["models"],
        active_model=ollama_info["active_model"],
    )
