"""
Focus Friend - Ollama Integration Service.
Manages communication with the local Ollama inference daemon with robust error handling.
Operates strictly over local loopback (localhost) with zero external network transmission.
"""

import json
import re
import socket
from typing import Dict, Any, List, Optional
import urllib.request
import urllib.error

from backend.config import settings
from backend.constants import PHI3_SYSTEM_PROMPT_TEMPLATE
from backend.exceptions import (
    OllamaConnectionError,
    InferenceTimeoutError,
    DistillationParsingError,
)
from backend.utils.logger import logger


class OllamaService:
    """Handles communication with the local Ollama daemon."""

    @classmethod
    def check_health(cls) -> Dict[str, Any]:
        """
        Checks if the local Ollama daemon is reachable and inspects downloaded models.
        Guarantees safe return without throwing unhandled network exceptions.
        """
        url = f"{settings.ollama_base_url}/api/tags"
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=2.5) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    models: List[str] = [
                        m.get("name", m.get("model", ""))
                        for m in data.get("models", [])
                        if m.get("name") or m.get("model")
                    ]
                    has_model = len(models) > 0
                    active_model = (
                        settings.default_model
                        if settings.default_model in models
                        else (models[0] if models else None)
                    )
                    return {
                        "connected": True,
                        "models": models,
                        "has_model": has_model,
                        "active_model": active_model,
                    }
        except (urllib.error.URLError, socket.timeout, ConnectionRefusedError) as net_err:
            logger.debug(f"Ollama daemon unreachable: {net_err}")
        except Exception as exc:
            logger.debug(f"Unexpected error inspecting Ollama: {exc}")

        return {
            "connected": False,
            "models": [],
            "has_model": False,
            "active_model": None,
        }

    @classmethod
    def extract_signal(cls, text: str, model: Optional[str] = None) -> Dict[str, Any]:
        """
        Invokes local Ollama inference to distill text into Tone, Timeline, and Task.
        
        Args:
            text: Raw message content.
            model: Optional model identifier override (defaults to settings.default_model).

        Returns:
            Dict containing 'vibe', 'deadline', 'action_item', 'engine'.

        Raises:
            InferenceTimeoutError: When generation exceeds timeout threshold.
            OllamaConnectionError: When the daemon drops connection.
            DistillationParsingError: When model response cannot be structured into JSON.
        """
        active_model = model or settings.default_model
        prompt = PHI3_SYSTEM_PROMPT_TEMPLATE.format(text=text)

        payload = json.dumps({
            "model": active_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9,
            }
        }).encode("utf-8")

        url = f"{settings.ollama_base_url}/api/generate"
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=settings.inference_timeout_seconds) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                raw_response = data.get("response", "").strip()

                parsed = cls._parse_json_payload(raw_response)
                return {
                    "vibe": parsed.get("vibe", "Neutral professional communication."),
                    "deadline": parsed.get("deadline", "No hard deadline specified."),
                    "action_item": parsed.get("action_item", "Review message details."),
                    "engine": f"Ollama ({active_model})",
                }

        except (socket.timeout, TimeoutError):
            raise InferenceTimeoutError(
                f"Ollama inference timed out after {settings.inference_timeout_seconds} seconds."
            )
        except urllib.error.URLError as net_err:
            if "timed out" in str(net_err).lower():
                raise InferenceTimeoutError("Ollama inference socket timed out.")
            raise OllamaConnectionError(f"Failed to connect to Ollama at {settings.ollama_base_url}: {net_err}")
        except json.JSONDecodeError as json_err:
            raise DistillationParsingError(f"Ollama returned non-JSON response payload: {json_err}")
        except Exception as exc:
            logger.error(f"Unexpected error during Ollama inference: {exc}", exc_info=True)
            raise

    @classmethod
    def _parse_json_payload(cls, raw_text: str) -> Dict[str, Any]:
        """Robustly extracts JSON object from raw LLM text output."""
        # 1. Direct parse attempt after trimming code fences
        cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text.strip(), flags=re.MULTILINE)
        cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # 2. Extract first matching JSON object {...}
        json_match = re.search(r"\{[\s\S]*\}", raw_text)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        raise DistillationParsingError("Model output did not contain a valid JSON object.")
