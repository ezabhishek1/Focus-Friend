"""
Focus Friend - Services Unit Test Suite.
Validates business logic, heuristic extraction patterns, JSON parsing resilience, and presets provider.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from backend.services.heuristic_service import HeuristicExtractionService
from backend.services.extraction_service import ExtractionService
from backend.services.presets_service import PresetsService
from backend.services.ollama_service import OllamaService
from backend.exceptions import InputValidationError, DistillationParsingError


def test_heuristic_extraction_returns_tone_timeline_task():
    """Verify regex-based NLP heuristic accurately extracts Vibe, Deadline, and Action Item."""
    text = (
        "Hey Alex, hope your week is wrapping up nicely! Overall leadership loved the retro slides. "
        "Could you just review the updated deck and fix the slide 7 metric before end of day Friday? Thanks!"
    )
    result = HeuristicExtractionService.extract(text)

    assert "vibe" in result
    assert "deadline" in result
    assert "action_item" in result
    assert result["deadline"] == "End of Day Friday"
    assert "review" in result["action_item"].lower() or "fix" in result["action_item"].lower()
    assert "Focus Friend" in result["engine"]


def test_heuristic_extraction_default_deadline():
    """Verify graceful handling when no explicit deadline is mentioned."""
    text = "Hey Alex, could you review the documentation when you get a chance?"
    result = HeuristicExtractionService.extract(text)
    assert "No hard deadline specified" in result["deadline"]
    assert "Review" in result["action_item"]


def test_extraction_service_validation():
    """Verify input validation triggers for empty or short messages."""
    with pytest.raises(InputValidationError):
        ExtractionService.distill("")

    with pytest.raises(InputValidationError):
        ExtractionService.distill("   ab  ")


def test_extraction_service_fallback_distill():
    """Verify ExtractionService successfully falls back to offline heuristic engine."""
    text = "Team, please review the latest sprint deliverables before tomorrow at 5:00 PM."
    result = ExtractionService.distill(text)

    assert "vibe" in result
    assert "deadline" in result
    assert "action_item" in result
    assert result["latency_seconds"] >= 0
    assert "engine" in result


def test_ollama_json_payload_parser():
    """Verify Ollama JSON response parser handles plain JSON and markdown-wrapped blocks."""
    # 1. Plain clean JSON
    clean_json = '{"vibe": "Friendly", "deadline": "Friday", "action_item": "Review slides"}'
    parsed = OllamaService._parse_json_payload(clean_json)
    assert parsed["vibe"] == "Friendly"

    # 2. Wrapped in Markdown ```json ... ```
    wrapped_json = '```json\n{"vibe": "Reassuring", "deadline": "Tomorrow", "action_item": "Test login"}\n```'
    parsed = OllamaService._parse_json_payload(wrapped_json)
    assert parsed["vibe"] == "Reassuring"

    # 3. Invalid non-JSON payload raises DistillationParsingError
    with pytest.raises(DistillationParsingError):
        OllamaService._parse_json_payload("Sorry, I cannot distill this text.")


def test_presets_service():
    """Verify presets service loads all scenario items with required fields."""
    presets = PresetsService.get_all_presets()
    assert len(presets) >= 4
    for p in presets:
        assert "id" in p
        assert "title" in p
        assert "text" in p
        assert len(p["text"]) > 20

    # Individual preset lookup
    single = PresetsService.get_preset_by_id("manager_email")
    assert single is not None
    assert single["id"] == "manager_email"

    # Non-existent preset
    assert PresetsService.get_preset_by_id("unknown_id") is None


if __name__ == "__main__":
    pytest.main([__file__])
