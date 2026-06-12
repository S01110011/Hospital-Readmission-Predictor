"""Feature engineering utilities."""

from __future__ import annotations

import pandas as pd


def add_clinical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add interpretable derived features for readmission modeling."""

    engineered = df.copy()
    engineered["medications_per_day"] = engineered["num_medications"] / engineered[
        "length_of_stay"
    ].clip(lower=1)
    engineered["high_utilization"] = (
        (engineered["num_prior_admissions"] >= 2) | (engineered["length_of_stay"] >= 7)
    )
    engineered["complex_chronic_condition"] = (
        engineered["has_ckd"].astype(bool)
        & engineered["has_diabetes"].astype(bool)
        & engineered["has_hypertension"].astype(bool)
    )
    return engineered
