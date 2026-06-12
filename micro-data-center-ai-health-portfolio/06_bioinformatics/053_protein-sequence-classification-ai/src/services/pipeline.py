"""Reusable pipeline logic for Protein Sequence Classification AI."""

from __future__ import annotations

from typing import Any


def classify_score(score: float) -> str:
    """Convert a normalized score into a business-friendly class."""

    if score < 0.33:
        return "low"
    if score < 0.66:
        return "medium"
    return "high"


def run_pipeline(payload: dict[str, Any]) -> dict[str, Any]:
    """Run deterministic baseline scoring for the portfolio scaffold.

    Production implementations should replace this baseline with a validated
    model or governed analytics workflow.
    """

    numeric_signal = float(payload["numeric_signal"])
    severity = int(payload["severity"])
    score = min(1.0, (numeric_signal / 1000.0) * 0.55 + (severity / 5.0) * 0.45)
    return {
        "entity_id": str(payload["entity_id"]),
        "risk_score": round(score, 4),
        "classification": classify_score(score),
        "disclaimer": "Decision support prototype only. Requires domain validation before production use.",
    }
