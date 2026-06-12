"""Prediction utilities used by the API and tests."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.config import get_settings
from src.features.feature_engineering import add_clinical_features
from src.utils.validation import validate_patient_dataframe


def classify_risk(probability: float) -> str:
    """Classify readmission risk from calibrated-like probability bands."""

    if probability < 0.30:
        return "baixo"
    if probability < 0.60:
        return "medio"
    return "alto"


@lru_cache
def load_model_package(model_path: str | Path | None = None) -> dict[str, Any]:
    """Load trained model package from disk."""

    settings = get_settings()
    path = Path(model_path or settings.model_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Model artifact not found at {path}. Run `python -m src.models.train` first."
        )
    package = joblib.load(path)
    required_keys = {"model", "model_name", "feature_columns", "threshold", "model_version"}
    missing = required_keys - set(package)
    if missing:
        raise ValueError(f"Model artifact is missing required metadata: {sorted(missing)}")
    return package


def predict_readmission(records: list[dict[str, Any]], model_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Predict readmission probability and risk class for one or more records."""

    settings = get_settings()
    package = load_model_package(model_path)
    df = pd.DataFrame(records)
    validation = validate_patient_dataframe(df, require_target=False)
    if not validation.is_valid:
        raise ValueError("; ".join(validation.errors))

    df = add_clinical_features(df)
    features = df[package["feature_columns"]]
    probabilities = package["model"].predict_proba(features)[:, 1]
    threshold = float(package.get("threshold", settings.prediction_threshold))

    return [
        {
            "readmission_probability": round(float(probability), 4),
            "risk_class": classify_risk(float(probability)),
            "threshold": threshold,
            "model_version": package.get("model_version", settings.model_version),
        }
        for probability in probabilities
    ]
