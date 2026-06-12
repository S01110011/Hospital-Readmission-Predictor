"""API and pipeline tests for Security Event Log Analyzer."""

from fastapi.testclient import TestClient

from src.api.main import app
from src.services.pipeline import run_pipeline


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "X-Request-ID" in response.headers


def test_ready_and_metrics_endpoints():
    client = TestClient(app)

    ready = client.get("/ready")
    metrics = client.get("/metrics")

    assert ready.status_code == 200
    assert ready.json()["status"] == "ready"
    assert metrics.status_code == 200
    assert "requests_total" in metrics.json()


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


def test_predict_endpoint_rejects_invalid_payload():
    client = TestClient(app)
    response = client.post(
        "/predict",
        json={"entity_id": "x", "numeric_signal": -1, "severity": 8, "context": "test"},
    )

    assert response.status_code == 422
