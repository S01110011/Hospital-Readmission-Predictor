"""Shared test fixtures."""

from __future__ import annotations

import pytest

from src.data.load_data import generate_synthetic_readmission_data


@pytest.fixture()
def sample_patient() -> dict[str, object]:
    """Return a valid patient payload for API and prediction tests."""

    return {
        "age": 72,
        "gender": "female",
        "length_of_stay": 8,
        "num_prior_admissions": 2,
        "num_medications": 11,
        "num_lab_procedures": 58,
        "comorbidity_score": 5,
        "discharge_disposition": "home_health",
        "primary_diagnosis": "heart_failure",
        "has_diabetes": True,
        "has_hypertension": True,
        "has_ckd": False,
        "follow_up_scheduled": False,
    }


@pytest.fixture()
def sample_dataframe():
    """Return a small valid synthetic dataset."""

    return generate_synthetic_readmission_data(n_samples=120, seed=123)
