"""Train and compare hospital readmission models."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.config import get_settings
from src.data.load_data import PROCESSED_DATA_PATH, load_dataset, save_dataset
from src.data.preprocessing import (
    BOOLEAN_FEATURES,
    CATEGORICAL_FEATURES,
    FEATURE_COLUMNS,
    NUMERIC_FEATURES,
    build_preprocessor,
)
from src.features.feature_engineering import add_clinical_features
from src.models.evaluate import evaluate_classifier, save_evaluation_plots, save_metrics
from src.models.predict import load_model_package
from src.utils.artifacts import sha256_file
from src.utils.logger import get_logger

TARGET = "readmitted_30_days"
ARTIFACT_DIR = Path("artifacts")


def _feature_columns() -> list[str]:
    return FEATURE_COLUMNS + [
        "medications_per_day",
        "high_utilization",
        "complex_chronic_condition",
    ]


def _build_models(random_state: int = 42) -> dict[str, Pipeline]:
    engineered_numeric = NUMERIC_FEATURES + ["medications_per_day"]
    engineered_boolean = BOOLEAN_FEATURES + ["high_utilization", "complex_chronic_condition"]

    def pipeline(estimator: object) -> Pipeline:
        local_preprocessor = build_preprocessor(
            numeric_features=engineered_numeric,
            categorical_features=CATEGORICAL_FEATURES,
            boolean_features=engineered_boolean,
        )
        return Pipeline(steps=[("preprocessor", local_preprocessor), ("classifier", estimator)])

    return {
        "logistic_regression": pipeline(
            LogisticRegression(max_iter=1000, class_weight="balanced", random_state=random_state)
        ),
        "random_forest": pipeline(
            RandomForestClassifier(
                n_estimators=250,
                min_samples_leaf=5,
                class_weight="balanced",
                random_state=random_state,
                n_jobs=-1,
            )
        ),
        "gradient_boosting": pipeline(
            GradientBoostingClassifier(n_estimators=160, learning_rate=0.05, random_state=random_state)
        ),
    }


def train_models(random_state: int = 42) -> dict[str, object]:
    """Train candidate models and persist the best model by recall then ROC-AUC."""

    settings = get_settings()
    logger = get_logger(__name__, settings.log_level)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    raw_df = load_dataset()
    df = add_clinical_features(raw_df)
    save_dataset(df, PROCESSED_DATA_PATH)

    x = df[_feature_columns()]
    y = df[TARGET]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, stratify=y, random_state=random_state
    )

    results: dict[str, dict[str, object]] = {}
    fitted_models: dict[str, Pipeline] = {}

    for name, model in _build_models(random_state).items():
        logger.info("Training model: %s", name)
        model.fit(x_train, y_train)
        results[name] = evaluate_classifier(model, x_test, y_test, settings.prediction_threshold)
        fitted_models[name] = model

    best_name = max(results, key=lambda item: (results[item]["recall"], results[item]["roc_auc"]))
    best_model = fitted_models[best_name]
    training_metadata = {
        "trained_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_rows": int(len(df)),
        "positive_rate": round(float(y.mean()), 4),
        "random_state": random_state,
        "selection_rule": "highest recall, then highest ROC-AUC",
        "clinical_rationale": (
            "Recall is prioritized because false negatives may miss patients who need "
            "post-discharge follow-up to prevent readmission."
        ),
    }
    model_package = {
        "model": best_model,
        "model_name": best_name,
        "feature_columns": _feature_columns(),
        "threshold": settings.prediction_threshold,
        "model_version": settings.model_version,
        "training_metadata": training_metadata,
        "metrics": results[best_name],
    }

    joblib.dump(model_package, settings.model_path)
    load_model_package.cache_clear()
    model_hash = sha256_file(settings.model_path)
    save_metrics({"best_model": best_name, "models": results}, settings.metrics_path)
    save_evaluation_plots(best_model, x_test, y_test, ARTIFACT_DIR, settings.prediction_threshold)

    summary = {
        "best_model": best_name,
        "model_sha256": model_hash,
        **training_metadata,
        "feature_columns": _feature_columns(),
    }
    (ARTIFACT_DIR / "model_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logger.info("Best model: %s", best_name)
    return model_package


if __name__ == "__main__":
    train_models()
