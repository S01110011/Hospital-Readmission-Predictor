"""Tests for model training and prediction helpers."""

from pathlib import Path

from src.models.predict import classify_risk, predict_readmission
from src.models.train import train_models


def test_classify_risk_bands():
    assert classify_risk(0.1) == "baixo"
    assert classify_risk(0.4) == "medio"
    assert classify_risk(0.8) == "alto"


def test_train_and_predict_returns_probability(sample_patient):
    train_models(random_state=7)

    prediction = predict_readmission([sample_patient])[0]

    assert Path("artifacts/model.joblib").exists()
    assert 0 <= prediction["readmission_probability"] <= 1
    assert prediction["risk_class"] in {"baixo", "medio", "alto"}
