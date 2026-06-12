"""FastAPI application for hospital readmission prediction."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.config import get_settings
from src.models.predict import load_model_package, predict_readmission
from src.utils.artifacts import sha256_file
from src.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__, settings.log_level)

app = FastAPI(
    title="Hospital Readmission Predictor",
    description=(
        "API for estimating 30-day hospital readmission risk. "
        "For clinical decision support only; not a medical device."
    ),
    version="0.1.0",
    docs_url="/docs" if settings.enable_docs else None,
    redoc_url="/redoc" if settings.enable_docs else None,
    openapi_url="/openapi.json" if settings.enable_docs else None,
)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "Authorization"],
    )


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add conservative HTTP security headers for API responses."""

    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


class PatientFeatures(BaseModel):
    """Validated patient input for readmission inference."""

    age: int = Field(..., ge=18, le=105)
    gender: Literal["female", "male", "other"]
    length_of_stay: int = Field(..., ge=1, le=60)
    num_prior_admissions: int = Field(..., ge=0, le=20)
    num_medications: int = Field(..., ge=0, le=60)
    num_lab_procedures: int = Field(..., ge=0, le=200)
    comorbidity_score: int = Field(..., ge=0, le=15)
    discharge_disposition: Literal["home", "home_health", "skilled_nursing", "rehab"]
    primary_diagnosis: Literal[
        "heart_failure", "diabetes", "copd", "pneumonia", "renal_disease", "other"
    ]
    has_diabetes: bool
    has_hypertension: bool
    has_ckd: bool
    follow_up_scheduled: bool


class PredictionResponse(BaseModel):
    """Prediction response returned by the API."""

    readmission_probability: float
    risk_class: Literal["baixo", "medio", "alto"]
    threshold: float
    model_version: str


class ReadinessResponse(BaseModel):
    """Readiness response with model artifact status."""

    status: Literal["ready", "not_ready"]
    model_loaded: bool


class ModelInfoResponse(BaseModel):
    """Non-sensitive model metadata for observability."""

    model_name: str
    model_version: str
    threshold: float
    model_sha256: str
    training_metadata: dict[str, object]


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health status."""

    return {"status": "ok", "environment": settings.app_env}


@app.get("/ready", response_model=ReadinessResponse)
def ready() -> ReadinessResponse:
    """Return readiness based on model artifact availability."""

    try:
        load_model_package()
    except Exception:
        return ReadinessResponse(status="not_ready", model_loaded=False)
    return ReadinessResponse(status="ready", model_loaded=True)


@app.get("/model-info", response_model=ModelInfoResponse)
def model_info() -> ModelInfoResponse:
    """Return non-sensitive model metadata for release review."""

    try:
        package = load_model_package()
        model_path = Path(settings.model_path)
        return ModelInfoResponse(
            model_name=package["model_name"],
            model_version=package["model_version"],
            threshold=float(package["threshold"]),
            model_sha256=sha256_file(model_path),
            training_metadata=package.get("training_metadata", {}),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/predict", response_model=PredictionResponse)
def predict(patient: PatientFeatures) -> PredictionResponse:
    """Predict 30-day readmission risk for a single patient."""

    try:
        result = predict_readmission([patient.model_dump()])[0]
        return PredictionResponse(**result)
    except FileNotFoundError as exc:
        logger.exception("Model artifact is unavailable")
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        logger.warning("Invalid prediction input: %s", exc)
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected prediction error")
        raise HTTPException(status_code=500, detail="Unexpected prediction error") from exc
