"""
Focus Friend - REST API Integration Test Suite.
Validates all endpoints, timing middleware headers, schema validation, and error envelopes.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify liveness probe, app identity, and latency header."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "Focus Friend"
    assert "ollama_connected" in data
    assert "fallback_engine_available" in data
    assert "X-Process-Time" in response.headers


def test_models_endpoint():
    """Verify local models enumeration endpoint."""
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert "connected" in data
    assert "models" in data
    assert isinstance(data["models"], list)


def test_presets_endpoints():
    """Verify list presets and get single preset by ID."""
    # List all
    response = client.get("/api/v1/presets")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 4
    assert len(data["presets"]) == data["count"]

    # Specific preset
    single_resp = client.get("/api/v1/presets/manager_email")
    assert single_resp.status_code == 200
    item = single_resp.json()
    assert item["id"] == "manager_email"
    assert "Boss Email" in item["title"]

    # Not found scenario
    missing_resp = client.get("/api/v1/presets/non_existent_preset")
    assert missing_resp.status_code == 404
    err_data = missing_resp.json()
    assert "error" in err_data
    assert "code" in err_data


def test_extract_endpoint_success():
    """Verify successful distillation into Tone, Timeline, and Task."""
    payload = {
        "text": (
            "Hi Alex, please take a look at the staging deployment and verify login "
            "before 10:00 AM tomorrow. Thanks!"
        )
    }
    response = client.post("/api/v1/extract", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "vibe" in data
    assert "deadline" in data
    assert "action_item" in data
    assert "engine" in data
    assert data["latency_seconds"] > 0
    assert "X-Process-Time" in response.headers


def test_extract_endpoint_validation_error():
    """Verify Pydantic schema validation when input is below minimum character length."""
    payload = {"text": "hi"}
    response = client.post("/api/v1/extract", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert "code" in data
    assert "SCHEMA_VALIDATION_ERROR" in data["code"]


if __name__ == "__main__":
    test_health_endpoint()
    test_models_endpoint()
    test_presets_endpoints()
    test_extract_endpoint_success()
    test_extract_endpoint_validation_error()
    print("All REST API integration tests passed successfully!")
