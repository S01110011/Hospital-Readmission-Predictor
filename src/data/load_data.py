"""Data loading and synthetic data generation."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.utils.validation import validate_patient_dataframe


RAW_DATA_PATH = Path("data/raw/readmissions_synthetic.csv")
PROCESSED_DATA_PATH = Path("data/processed/readmissions_processed.csv")


def generate_synthetic_readmission_data(n_samples: int = 2500, seed: int = 42) -> pd.DataFrame:
    """Generate a reproducible synthetic dataset with plausible clinical signals."""

    rng = np.random.default_rng(seed)
    age = np.clip(rng.normal(64, 15, n_samples).round(), 18, 95).astype(int)
    gender = rng.choice(["female", "male", "other"], n_samples, p=[0.52, 0.46, 0.02])
    primary_diagnosis = rng.choice(
        ["heart_failure", "diabetes", "copd", "pneumonia", "renal_disease", "other"],
        n_samples,
        p=[0.18, 0.22, 0.16, 0.17, 0.12, 0.15],
    )

    has_diabetes = (primary_diagnosis == "diabetes") | (rng.random(n_samples) < 0.28)
    has_hypertension = rng.random(n_samples) < np.clip(0.35 + (age - 50) * 0.006, 0.2, 0.75)
    has_ckd = (primary_diagnosis == "renal_disease") | (rng.random(n_samples) < 0.11)

    comorbidity_score = np.clip(
        rng.poisson(2.2, n_samples)
        + has_diabetes.astype(int)
        + has_hypertension.astype(int)
        + 2 * has_ckd.astype(int)
        + (age > 75).astype(int),
        0,
        15,
    )
    num_prior_admissions = np.clip(
        rng.poisson(0.8 + 0.2 * comorbidity_score + 0.5 * has_ckd.astype(int), n_samples),
        0,
        20,
    )
    length_of_stay = np.clip(
        rng.poisson(3 + 0.5 * comorbidity_score + 0.4 * num_prior_admissions, n_samples) + 1,
        1,
        60,
    )
    num_medications = np.clip(
        rng.poisson(4 + 1.2 * comorbidity_score + 0.04 * age, n_samples),
        0,
        60,
    )
    num_lab_procedures = np.clip(
        rng.normal(35 + 2.5 * comorbidity_score + 0.7 * length_of_stay, 12, n_samples).round(),
        0,
        200,
    ).astype(int)
    discharge_disposition = rng.choice(
        ["home", "home_health", "skilled_nursing", "rehab"],
        n_samples,
        p=[0.62, 0.2, 0.11, 0.07],
    )
    follow_up_scheduled = rng.random(n_samples) < np.where(discharge_disposition == "home", 0.62, 0.74)

    diagnosis_risk = pd.Series(primary_diagnosis).map(
        {
            "heart_failure": 0.45,
            "diabetes": 0.2,
            "copd": 0.28,
            "pneumonia": 0.18,
            "renal_disease": 0.4,
            "other": 0.0,
        }
    ).to_numpy()
    disposition_risk = pd.Series(discharge_disposition).map(
        {"home": 0.0, "home_health": 0.2, "skilled_nursing": 0.4, "rehab": 0.15}
    ).to_numpy()

    logit = (
        -3.3
        + 0.025 * (age - 60)
        + 0.18 * comorbidity_score
        + 0.28 * num_prior_admissions
        + 0.045 * length_of_stay
        + 0.018 * num_medications
        + 0.012 * num_lab_procedures
        + 0.35 * has_ckd.astype(int)
        + diagnosis_risk
        + disposition_risk
        - 0.55 * follow_up_scheduled.astype(int)
    )
    probability = 1 / (1 + np.exp(-logit))
    readmitted = (rng.random(n_samples) < probability).astype(int)

    return pd.DataFrame(
        {
            "age": age,
            "gender": gender,
            "length_of_stay": length_of_stay,
            "num_prior_admissions": num_prior_admissions,
            "num_medications": num_medications,
            "num_lab_procedures": num_lab_procedures,
            "comorbidity_score": comorbidity_score,
            "discharge_disposition": discharge_disposition,
            "primary_diagnosis": primary_diagnosis,
            "has_diabetes": has_diabetes,
            "has_hypertension": has_hypertension,
            "has_ckd": has_ckd,
            "follow_up_scheduled": follow_up_scheduled,
            "readmitted_30_days": readmitted,
        }
    )


def save_dataset(df: pd.DataFrame, path: Path) -> None:
    """Persist dataset as CSV, creating parent directories when needed."""

    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def load_dataset(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load a patient dataset and validate its schema."""

    if not path.exists():
        df = generate_synthetic_readmission_data()
        save_dataset(df, path)
    df = pd.read_csv(path)
    validation = validate_patient_dataframe(df, require_target=True)
    if not validation.is_valid:
        raise ValueError("; ".join(validation.errors))
    return df
