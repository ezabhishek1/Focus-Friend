"""
Focus Friend - Primary Extraction Business Logic Orchestrator.
Orchestrates Ollama model inference with graceful zero-cloud heuristic fallback.
"""

import time
from typing import Dict, Any, Optional

from backend.config import settings
from backend.exceptions import (
    InputValidationError,
    FocusFriendError,
)
from backend.services.ollama_service import OllamaService
from backend.services.heuristic_service import HeuristicExtractionService
from backend.utils.logger import logger


class ExtractionService:
    """Business logic coordinator for message distillation."""

    @classmethod
    def distill(cls, text: str, model: Optional[str] = None) -> Dict[str, Any]:
        """
        Distills raw unstructured text into Tone, Timeline, and Task.
        Guarantees a safe, deterministic output structure.

        Args:
            text: Raw message string to distill.
            model: Optional model identifier override for Ollama.

        Returns:
            Dict containing vibe, deadline, action_item, engine, latency_seconds, and is_fallback.

        Raises:
            InputValidationError: If input is empty or insufficient.
            FocusFriendError: If both Ollama and fallback engine are unavailable.
        """
        clean_text = text.strip() if text else ""
        if len(clean_text) < 5:
            raise InputValidationError("Input text must contain at least 5 characters.")

        start_time = time.perf_counter()

        # Step 1: Attempt local Ollama inference if daemon is connected
        ollama_status = OllamaService.check_health()
        if ollama_status["connected"] and ollama_status["has_model"]:
            try:
                target_model = model or ollama_status["active_model"]
                logger.info(f"Attempting local AI distillation via Ollama ({target_model})...")
                result = OllamaService.extract_signal(clean_text, model=target_model)
                elapsed = round(time.perf_counter() - start_time, 3)
                result["latency_seconds"] = elapsed
                result["is_fallback"] = False
                logger.info(f"Local AI distillation succeeded in {elapsed}s.")
                return result
            except Exception as exc:
                logger.warning(f"Ollama inference attempt failed ({exc}). Falling back to Heuristic Engine.")

        # Step 2: Fall back to Zero-Cloud Heuristic Engine
        if settings.enable_fallback_engine:
            logger.info("Distilling via Focus Friend Zero-Cloud Heuristic Engine...")
            result = HeuristicExtractionService.extract(clean_text)
            elapsed = round(time.perf_counter() - start_time, 3)
            result["latency_seconds"] = elapsed
            result["is_fallback"] = True
            return result

        raise FocusFriendError(
            message="Inference engine is unavailable and fallback engine is disabled.",
            code="ENGINE_UNAVAILABLE"
        )
