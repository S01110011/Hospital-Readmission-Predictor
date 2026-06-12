"""Tests for FastAPI endpoints."""

from fastapi.testclient import TestClient

from src.api.main import app
from src.models.train import train_models


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_ready_endpoint_after_training():
    train_models(random_state=5)
    client = TestClient(app)

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_model_info_endpoint_after_training():
    train_models(random_state=6)
    client = TestClient(app)

    response = client.get("/model-info")

    assert response.status_code == 200
    body = response.json()
    assert body["model_name"]
    assert len(body["model_sha256"]) == 64


def test_predict_endpoint(sample_patient):
    train_models(random_state=11)
    client = TestClient(app)

    response = client.post("/predict", json=sample_patient)

    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["readmission_probability"] <= 1
    assert body["risk_class"] in {"baixo", "medio", "alto"}


def test_predict_endpoint_rejects_invalid_payload(sample_patient):
    client = TestClient(app)
    sample_patient["age"] = 8

    response = client.post("/predict", json=sample_patient)

    assert response.status_code == 422
