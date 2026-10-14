"""
Focus Friend - Presets Service.
Provides standardized overwhelm scenarios for UI testing and ADHD instant initiation.
"""

from typing import List, Dict, Any, Optional
from backend.constants import OVERWHELM_PRESETS


class PresetsService:
    """Service providing pre-configured communication overload scenarios."""

    @classmethod
    def get_all_presets(cls) -> List[Dict[str, Any]]:
        """Returns all registered overwhelm presets as a list."""
        return list(OVERWHELM_PRESETS.values())

    @classmethod
    def get_preset_by_id(cls, preset_id: str) -> Optional[Dict[str, Any]]:
        """Returns a single preset by key, or None if not found."""
        return OVERWHELM_PRESETS.get(preset_id)
