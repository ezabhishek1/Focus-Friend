"""
Focus Friend - Presets Endpoint Router.
Provides overwhelm scenarios for rapid testing and demonstrations.
"""

from fastapi import APIRouter, HTTPException, status
from backend.api.schemas.response_schemas import PresetsResponse, PresetItem, ErrorResponse
from backend.services.presets_service import PresetsService

router = APIRouter(prefix="/presets", tags=["Presets"])


@router.get(
    "",
    response_model=PresetsResponse,
    summary="List all overwhelm presets"
)
def get_presets():
    """Returns pre-configured realistic communication scenarios (Boss email, Slack thread, etc.)."""
    raw_presets = PresetsService.get_all_presets()
    items = [PresetItem(**p) for p in raw_presets]
    return PresetsResponse(count=len(items), presets=items)


@router.get(
    "/{preset_id}",
    response_model=PresetItem,
    responses={404: {"model": ErrorResponse, "description": "Preset not found."}},
    summary="Get a specific overwhelm preset by ID"
)
def get_preset_by_id(preset_id: str):
    """Returns a single scenario by its ID key."""
    preset = PresetsService.get_preset_by_id(preset_id)
    if not preset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Preset with ID '{preset_id}' was not found."
        )
    return PresetItem(**preset)
