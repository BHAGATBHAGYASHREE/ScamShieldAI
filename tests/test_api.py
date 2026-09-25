"""
test_api.py - Integration and unit tests for ScamShield AI FastAPI microservice
"""
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from app.main import app, load_artifacts


@pytest.fixture(scope="session")
def client():
    # Trigger startup event to load model and metadata
    load_artifacts()
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert "accuracy" in data
    assert data["accuracy"] > 0.90


def test_analyze_endpoint_real_fake_order(client):
    payload = {
        "message": "Your order #AMZ-99381 of Rs. 14,999 has been placed. Call fraud desk immediately at +919876543210 or cancel at bit.ly/cancel-order-now"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["is_scam"] is True
    assert data["risk_score"] >= 80.0
    assert data["risk_level"] in ["HIGH RISK", "CRITICAL RISK"]
    assert data["category"] == "Fake Order"
    assert data["trigger_count"] > 0
    assert len(data["safety_recommendations"]) > 0
    assert data["latency_ms"] >= 0.0


def test_analyze_endpoint_legitimate_message(client):
    payload = {
        "message": "Hey friend, are we still meeting for the study session today?"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["is_scam"] is False
    assert data["risk_score"] < 40.0
    assert data["risk_level"] in ["SAFE", "SUSPICIOUS"]


def test_analyze_batch_endpoint(client):
    payload = {
        "messages": [
            "Your order has been shipped via BlueDart.",
            "URGENT! Send OTP to verify bank account immediately."
        ]
    }
    response = client.post("/analyze-batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_analyze_validation_error(client):
    # Empty message should fail Pydantic min_length=1 validation
    response = client.post("/analyze", json={"message": ""})
    assert response.status_code == 422


def test_demo_samples_endpoint(client):
    response = client.get("/demo-samples")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 4
    sample_ids = [s["id"] for s in data]
    assert "demo_real_fake_order" in sample_ids
