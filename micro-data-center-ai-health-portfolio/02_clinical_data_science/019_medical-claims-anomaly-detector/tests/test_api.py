"""API and pipeline tests for Medical Claims Anomaly Detector."""

from fastapi.testclient import TestClient

from src.api.main import app
from src.services.pipeline import run_pipeline


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_pipeline_returns_valid_score():
    result = run_pipeline({"entity_id": "demo-001", "numeric_signal": 500, "severity": 3})

    assert 0 <= result["risk_score"] <= 1
    assert result["classification"] in {"low", "medium", "high"}


def test_predict_endpoint():
    client = TestClient(app)
    response = client.post(
        "/predict",
        json={"entity_id": "demo-001", "numeric_signal": 500, "severity": 3, "context": "test"},
    )

    assert response.status_code == 200
    assert 0 <= response.json()["risk_score"] <= 1
