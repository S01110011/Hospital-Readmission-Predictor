"""Validation utilities for clinical tabular data."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


REQUIRED_COLUMNS = {
    "age",
    "gender",
    "length_of_stay",
    "num_prior_admissions",
    "num_medications",
    "num_lab_procedures",
    "comorbidity_score",
    "discharge_disposition",
    "primary_diagnosis",
    "has_diabetes",
    "has_hypertension",
    "has_ckd",
    "follow_up_scheduled",
}

TARGET_COLUMN = "readmitted_30_days"


@dataclass(frozen=True)
class ValidationResult:
    """Structured result returned by data validation."""

    is_valid: bool
    errors: list[str]


def validate_patient_dataframe(df: pd.DataFrame, require_target: bool = True) -> ValidationResult:
    """Validate schema and simple clinical ranges for patient records."""

    errors: list[str] = []
    if df.empty:
        return ValidationResult(False, ["Dataframe is empty"])

    expected = set(REQUIRED_COLUMNS)
    if require_target:
        expected.add(TARGET_COLUMN)

    missing = sorted(expected - set(df.columns))
    if missing:
        errors.append(f"Missing required columns: {missing}")
        return ValidationResult(False, errors)

    required_nulls = df[list(expected)].isna().sum()
    null_columns = required_nulls[required_nulls > 0].to_dict()
    if null_columns:
        errors.append(f"Required columns contain null values: {null_columns}")

    ranges = {
        "age": (18, 105),
        "length_of_stay": (1, 60),
        "num_prior_admissions": (0, 20),
        "num_medications": (0, 60),
        "num_lab_procedures": (0, 200),
        "comorbidity_score": (0, 15),
    }
    for column, (min_value, max_value) in ranges.items():
        if not pd.api.types.is_numeric_dtype(df[column]):
            errors.append(f"{column} must be numeric")
            continue
        invalid = ~df[column].between(min_value, max_value)
        if invalid.any():
            errors.append(f"{column} contains values outside [{min_value}, {max_value}]")

    allowed_values = {
        "gender": {"female", "male", "other"},
        "discharge_disposition": {"home", "home_health", "skilled_nursing", "rehab"},
        "primary_diagnosis": {
            "heart_failure",
            "diabetes",
            "copd",
            "pneumonia",
            "renal_disease",
            "other",
        },
    }
    for column, allowed in allowed_values.items():
        invalid_values = set(df[column].dropna().unique()) - allowed
        if invalid_values:
            errors.append(f"{column} contains unsupported values: {sorted(invalid_values)}")

    if require_target:
        invalid_target = set(df[TARGET_COLUMN].dropna().unique()) - {0, 1}
        if invalid_target:
            errors.append(f"{TARGET_COLUMN} must be binary 0/1")

    return ValidationResult(not errors, errors)
