"""Preprocessing pipeline definitions."""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = [
    "age",
    "length_of_stay",
    "num_prior_admissions",
    "num_medications",
    "num_lab_procedures",
    "comorbidity_score",
]

CATEGORICAL_FEATURES = ["gender", "discharge_disposition", "primary_diagnosis"]

BOOLEAN_FEATURES = ["has_diabetes", "has_hypertension", "has_ckd", "follow_up_scheduled"]

FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES + BOOLEAN_FEATURES


def cast_to_object(data):
    """Cast transformer input to object dtype for boolean imputation."""

    return data.astype(object)


def cast_to_int(data):
    """Cast transformer input to integer dtype after boolean imputation."""

    return data.astype(int)


def build_preprocessor(
    numeric_features: list[str] | None = None,
    categorical_features: list[str] | None = None,
    boolean_features: list[str] | None = None,
) -> ColumnTransformer:
    """Build a robust preprocessing transformer for mixed clinical features."""

    numeric_features = numeric_features or NUMERIC_FEATURES
    categorical_features = categorical_features or CATEGORICAL_FEATURES
    boolean_features = boolean_features or BOOLEAN_FEATURES

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    boolean_pipeline = Pipeline(
        steps=[
            ("to_object", FunctionTransformer(cast_to_object)),
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("to_int", FunctionTransformer(cast_to_int)),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
            ("bool", boolean_pipeline, boolean_features),
        ]
    )
