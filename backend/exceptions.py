"""
Focus Friend - Custom Domain Exceptions.
Provides structured, predictable error types for the entire backend.
"""

from typing import Optional, Dict, Any


class FocusFriendError(Exception):
    """Base exception for all Focus Friend domain errors."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class InputValidationError(FocusFriendError):
    """Raised when the user message fails basic input criteria."""

    def __init__(self, message: str = "Invalid input message.", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="INVALID_INPUT", details=details)


class OllamaConnectionError(FocusFriendError):
    """Raised when local Ollama daemon cannot be reached."""

    def __init__(self, message: str = "Could not connect to local Ollama daemon.", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="OLLAMA_UNREACHABLE", details=details)


class InferenceTimeoutError(FocusFriendError):
    """Raised when model inference exceeds the maximum timeout window."""

    def __init__(self, message: str = "Inference exceeded maximum timeout window.", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="INFERENCE_TIMEOUT", details=details)


class ModelNotFoundError(FocusFriendError):
    """Raised when the requested model is not downloaded locally."""

    def __init__(self, model_name: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Model '{model_name}' is not installed in local Ollama.",
            code="MODEL_NOT_FOUND",
            details=details or {"model_name": model_name}
        )


class DistillationParsingError(FocusFriendError):
    """Raised when LLM output cannot be parsed into structured Tone/Timeline/Task."""

    def __init__(self, message: str = "Failed to parse model response into structured signal.", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="PARSING_ERROR", details=details)
