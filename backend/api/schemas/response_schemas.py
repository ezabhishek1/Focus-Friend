"""
Focus Friend - API Response Schemas.
Type-safe schemas returned by REST API v1 endpoints.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class DistilledSignalResponse(BaseModel):
    """Structured response containing the 3 distilled data points."""

    vibe: str = Field(
        ...,
        description="One-sentence emotional tone assessment (The Vibe).",
        examples=["The boss is pleased with your progress and asking for a routine tweak."]
    )
    deadline: str = Field(
        ...,
        description="Target dates, timeframe, or delivery window (The Deadline).",
        examples=["End of Day Friday"]
    )
    action_item: str = Field(
        ...,
        description="Single imperative-verb action item (The Action Item).",
        examples=["Review the slide 7 metric and reply with confirmation."]
    )
    engine: str = Field(
        ...,
        description="Name of the inference engine or model used.",
        examples=["Ollama (phi3:mini)"]
    )
    latency_seconds: float = Field(
        ...,
        description="Processing latency in seconds.",
        examples=[0.42]
    )
    is_fallback: bool = Field(
        ...,
        description="True if processed via Zero-Cloud local heuristic fallback.",
        examples=[False]
    )


class HealthStatusResponse(BaseModel):
    """Health check and status response."""

    status: str = Field(default="ok", description="Service health state.")
    app: str = Field(default="Focus Friend", description="Application name.")
    version: str = Field(default="1.0.0", description="API version.")
    ollama_connected: bool = Field(..., description="Whether local Ollama daemon is reachable.")
    active_model: Optional[str] = Field(None, description="Active local LLM model.")
    fallback_engine_available: bool = Field(True, description="Availability of offline heuristic fallback.")


class ModelsResponse(BaseModel):
    """List of available local models in Ollama."""

    connected: bool = Field(..., description="Whether local Ollama daemon is connected.")
    models: List[str] = Field(default_factory=list, description="List of local model tags.")
    active_model: Optional[str] = Field(None, description="Currently selected default model.")


class PresetItem(BaseModel):
    """Individual overwhelm preset scenario."""

    id: str = Field(..., description="Unique preset identifier.")
    title: str = Field(..., description="Readable title.")
    category: str = Field(..., description="Communication channel or scenario type.")
    emoji: str = Field(..., description="Visual badge emoji.")
    text: str = Field(..., description="Sample communication wall of text.")


class PresetsResponse(BaseModel):
    """Response containing list of overwhelm preset scenarios."""

    count: int = Field(..., description="Total presets available.")
    presets: List[PresetItem] = Field(default_factory=list, description="Preset items list.")


class ErrorResponse(BaseModel):
    """Standardized error response envelope."""

    error: str = Field(..., description="High-level error category.")
    code: str = Field(..., description="Machine-readable error code.")
    detail: Optional[str] = Field(None, description="Human-readable explanation of error.")
    timestamp: str = Field(..., description="ISO8601 UTC timestamp of error event.")
