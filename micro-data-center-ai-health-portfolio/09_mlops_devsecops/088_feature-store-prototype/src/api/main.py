"""FastAPI application for Feature Store Prototype."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from src.config import get_settings
from src.services.pipeline import run_pipeline
from src.utils.logger import get_logger


settings = get_settings()
logger = get_logger(__name__, settings.log_level)

app = FastAPI(
    title="Feature Store Prototype",
    version="0.1.0",
    description="Commercial Micro Data Center portfolio API. Not for regulated production use without validation.",
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Attach conservative HTTP security headers."""

    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
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


@app.post("/predict", response_model=AnalysisResponse)
def predict(payload: AnalysisRequest) -> AnalysisResponse:
    """Run validated portfolio pipeline."""

    try:
        result = run_pipeline(payload.model_dump())
        return AnalysisResponse(project=settings.app_name, model_version=settings.model_version, **result)
    except ValueError as exc:
        logger.warning("Invalid request: %s", exc)
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected service error")
        raise HTTPException(status_code=500, detail="Unexpected service error") from exc
