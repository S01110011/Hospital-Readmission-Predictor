"""Model evaluation and reporting utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate_classifier(
    model: Any,
    x_test: pd.DataFrame,
    y_test: pd.Series,
    threshold: float = 0.5,
) -> dict[str, Any]:
    """Evaluate a fitted binary classifier."""

    probabilities = model.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= threshold).astype(int)
    return {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
    }


def save_metrics(metrics: dict[str, Any], output_path: Path) -> None:
    """Save metrics as formatted JSON."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


def save_evaluation_plots(
    model: Any,
    x_test: pd.DataFrame,
    y_test: pd.Series,
    output_dir: Path,
    threshold: float = 0.5,
) -> None:
    """Save confusion matrix, ROC curve and Precision-Recall curve."""

    output_dir.mkdir(parents=True, exist_ok=True)
    probabilities = model.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    ConfusionMatrixDisplay.from_predictions(y_test, predictions)
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(output_dir / "confusion_matrix.png", dpi=160)
    plt.close()

    RocCurveDisplay.from_predictions(y_test, probabilities)
    plt.title("ROC Curve")
    plt.tight_layout()
    plt.savefig(output_dir / "roc_curve.png", dpi=160)
    plt.close()

    PrecisionRecallDisplay.from_predictions(y_test, probabilities)
    plt.title("Precision-Recall Curve")
    plt.tight_layout()
    plt.savefig(output_dir / "precision_recall_curve.png", dpi=160)
    plt.close()
