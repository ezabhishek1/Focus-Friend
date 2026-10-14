"""
Focus Friend - API Request Schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class ExtractRequest(BaseModel):
    """Payload schema for message distillation."""

    text: str = Field(
        ...,
        min_length=5,
        max_length=20000,
        description="The raw message or wall of text to distill into Tone, Timeline, and Task.",
        examples=["Hey team, please review the updated retro slides and verify the metrics before Friday 5 PM."]
    )
    model: Optional[str] = Field(
        default=None,
        description="Optional Ollama model identifier to override default (e.g. 'phi3:mini')."
    )
