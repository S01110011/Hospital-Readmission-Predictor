"""Tests for data validation and preprocessing."""

from src.data.preprocessing import FEATURE_COLUMNS, build_preprocessor
from src.utils.validation import validate_patient_dataframe


def test_validate_patient_dataframe_accepts_valid_data(sample_dataframe):
    result = validate_patient_dataframe(sample_dataframe, require_target=True)

    assert result.is_valid is True
    assert result.errors == []


def test_validate_patient_dataframe_rejects_invalid_age(sample_dataframe):
    sample_dataframe.loc[0, "age"] = 130

    result = validate_patient_dataframe(sample_dataframe, require_target=True)

    assert result.is_valid is False
    assert any("age" in error for error in result.errors)


def test_validate_patient_dataframe_rejects_nulls(sample_dataframe):
    sample_dataframe.loc[0, "primary_diagnosis"] = None

    result = validate_patient_dataframe(sample_dataframe, require_target=True)

    assert result.is_valid is False
    assert any("null" in error for error in result.errors)


def test_preprocessor_transforms_expected_rows(sample_dataframe):
    preprocessor = build_preprocessor()
    transformed = preprocessor.fit_transform(sample_dataframe[FEATURE_COLUMNS])

    assert transformed.shape[0] == len(sample_dataframe)
    assert transformed.shape[1] > len(FEATURE_COLUMNS)
