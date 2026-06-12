"""FastAPI application for Compound Similarity Search Engine."""

from __future__ import annotations

from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from src.config import get_settings
from src.services.pipeline import run_pipeline
from src.utils.logger import get_logger


settings = get_settings()
logger = get_logger(__name__, settings.log_level)

app = FastAPI(
    title="Compound Similarity Search Engine",
    version="0.1.0",
    description="Commercial Micro Data Center portfolio API. Not for regulated production use without validation.",
)

SERVICE_METRICS = {"requests_total": 0, "errors_total": 0, "last_latency_ms": 0.0}


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Attach conservative HTTP security headers."""

    request_id = str(uuid4())
    start = perf_counter()
    SERVICE_METRICS["requests_total"] += 1
    try:
        response = await call_next(request)
    except Exception:
        SERVICE_METRICS["errors_total"] += 1
        raise
    SERVICE_METRICS["last_latency_ms"] = round((perf_counter() - start) * 1000, 3)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Request-ID"] = request_id
    return response


class AnalysisRequest(BaseModel):
    """Validated request payload."""

    entity_id: str = Field(..., min_length=3, max_length=80)
    numeric_signal: float = Field(..., ge=0, le=1_000_000)
    severity: int = Field(default=1, ge=1, le=5)
    context: str = Field(default="synthetic", max_length=120)


class AnalysisResponse(BaseModel):
    """Validated response payload."""

    project: str
    entity_id: str
    risk_score: float
    classification: str
    model_version: str
    disclaimer: str


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health."""

    return {"status": "ok", "project": settings.app_name, "environment": settings.app_env}


@app.get("/ready")
def ready() -> dict[str, str]:
    """Return readiness for orchestration and client demos."""

    return {"status": "ready", "project": settings.app_name}


@app.get("/metrics")
def metrics() -> dict[str, float | int]:
    """Return minimal non-sensitive operational metrics."""

    return SERVICE_METRICS


@app.post("/predict", response_model=AnalysisResponse)
def predict(payload: AnalysisRequest) -> AnalysisResponse:
    """Run validated portfolio pipeline."""

    try:
        result = run_pipeline(payload.model_dump())
        logger.info("Processed request for project=%s classification=%s", settings.app_name, result["classification"])
        return AnalysisResponse(project=settings.app_name, model_version=settings.model_version, **result)
    except ValueError as exc:
        SERVICE_METRICS["errors_total"] += 1
        logger.warning("Invalid request: %s", exc)
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        SERVICE_METRICS["errors_total"] += 1
        logger.exception("Unexpected service error")
        raise HTTPException(status_code=500, detail="Unexpected service error") from exc
