"""Generate a 100-project Micro Data Center AI and Health portfolio.

The generator is intentionally versioned so the portfolio can be recreated,
audited and evolved without hand-maintaining thousands of scaffold files.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent


ROOT = Path("micro-data-center-ai-health-portfolio")


@dataclass(frozen=True)
class Category:
    folder: str
    title: str
    description: str


@dataclass(frozen=True)
class Project:
    number: int
    name: str
    category: Category
    domain: str
    client: str
    dataset: str
    interface: str
    uses_ai: bool = True


CATEGORIES = [
    Category(
        "01_healthcare_ai",
        "Healthcare AI",
        "Clinical decision support prototypes using synthetic or public healthcare data.",
    ),
    Category(
        "02_clinical_data_science",
        "Clinical Data Science",
        "Analytics, forecasting and data quality systems for hospitals and care networks.",
    ),
    Category(
        "03_drug_discovery",
        "Drug Discovery",
        "Computational pipelines for molecular screening, QSAR, ADMET and repurposing.",
    ),
    Category(
        "04_pharmacovigilance",
        "Pharmacovigilance",
        "Drug safety signal detection, case prioritization and regulatory automation.",
    ),
    Category(
        "05_crystallography_hpc",
        "Crystallography and Scientific HPC",
        "Scientific computing workflows for crystallography, imaging and HPC operations.",
    ),
    Category(
        "06_bioinformatics",
        "Bioinformatics",
        "Genomic, transcriptomic, proteomic and multi-omics analysis workflows.",
    ),
    Category(
        "07_micro_datacenter_operations",
        "Micro Data Center Operations",
        "Monitoring, capacity, energy, SLA and infrastructure operations products.",
    ),
    Category(
        "08_cybersecurity_defensive",
        "Defensive Cybersecurity",
        "Defensive security analytics, compliance evidence and data access auditing.",
    ),
    Category(
        "09_mlops_devsecops",
        "MLOps and DevSecOps",
        "Model lifecycle, validation, drift, explainability and secure deployment systems.",
    ),
    Category(
        "10_business_intelligence",
        "Business Intelligence and Client Products",
        "Executive dashboards, client portals and commercial data products.",
    ),
]


PROJECT_NAMES = [
    "Hospital Readmission Predictor",
    "Patient Mortality Risk Predictor",
    "ICU Length of Stay Predictor",
    "Sepsis Early Warning System",
    "Emergency Department Triage AI",
    "Chronic Disease Risk Stratification",
    "Diabetes Complication Predictor",
    "Cardiovascular Risk AI",
    "Stroke Risk Prediction System",
    "Medical Appointment No-Show Predictor",
    "Clinical Data Quality Auditor",
    "Synthetic EHR Data Generator",
    "Patient Cohort Discovery Tool",
    "Clinical Outcome Analytics Platform",
    "Hospital Operations Dashboard",
    "Bed Occupancy Forecasting System",
    "Hospital Cost Prediction Model",
    "Clinical KPI Monitoring Platform",
    "Medical Claims Anomaly Detector",
    "Population Health Analytics System",
    "Adverse Drug Reaction Detector",
    "Pharmacovigilance Signal Detection System",
    "Drug Safety NLP Classifier",
    "Medication Error Detection Platform",
    "Drug Interaction Risk Engine",
    "Vaccine Adverse Event Analyzer",
    "Real-Time Safety Surveillance Dashboard",
    "Pharmacovigilance Case Prioritizer",
    "Drug Label Change Monitor",
    "Regulatory Safety Report Generator",
    "Molecular Property Predictor",
    "Drug-Likeness Screening Platform",
    "QSAR Modeling Pipeline",
    "Molecular Toxicity Predictor",
    "Virtual Screening Workflow",
    "Protein-Ligand Binding Predictor",
    "Compound Similarity Search Engine",
    "ADMET Prediction System",
    "Drug Repurposing Knowledge Graph",
    "Molecular Optimization Assistant",
    "X-Ray Diffraction Data Pipeline",
    "Crystal Structure Classification AI",
    "Polymorph Screening Data Manager",
    "Crystallographic Image Analyzer",
    "Powder Diffraction Pattern Matcher",
    "Scientific HPC Job Scheduler Dashboard",
    "Molecular Simulation Workflow Manager",
    "Cryo-EM Data Processing Assistant",
    "Materials Discovery AI Platform",
    "Scientific Experiment Tracking System",
    "Genomic Variant Classification Pipeline",
    "RNA-Seq Analysis Workflow",
    "Protein Sequence Classification AI",
    "Biomarker Discovery Platform",
    "Clinical Genomics Dashboard",
    "Microbiome Data Analysis Pipeline",
    "Cancer Mutation Profiling Tool",
    "Multi-Omics Integration Platform",
    "Genomic Data Privacy Framework",
    "Bioinformatics Workflow Automation",
    "Micro Data Center Monitoring Platform",
    "Rack Temperature Prediction System",
    "Energy Consumption Forecasting AI",
    "GPU Utilization Optimization Dashboard",
    "Customer Resource Billing System",
    "SLA Monitoring Platform",
    "Incident Management System",
    "Backup Validation Platform",
    "Capacity Planning AI",
    "Infrastructure Health Score Dashboard",
    "Security Event Log Analyzer",
    "Defensive SIEM Mini Platform",
    "Vulnerability Management Dashboard",
    "Cloud Misconfiguration Scanner",
    "API Security Testing Framework",
    "Data Access Audit Platform",
    "Ransomware Readiness Assessment Tool",
    "Zero Trust Policy Validator",
    "Healthcare Data Privacy Scanner",
    "Compliance Evidence Automation System",
    "Model Registry Platform",
    "ML Experiment Tracking System",
    "Automated Model Validation Pipeline",
    "Data Drift Detection Platform",
    "Model Bias Monitoring System",
    "Secure ML API Deployment Template",
    "CI/CD for Healthcare AI Models",
    "Feature Store Prototype",
    "Model Explainability Service",
    "AI Governance Documentation Generator",
    "Executive Healthcare BI Dashboard",
    "Laboratory Revenue Analytics Platform",
    "Client Portal for AI Services",
    "Research Project Management System",
    "Scientific Article Summarization Platform",
    "Grant Proposal Intelligence Assistant",
    "Laboratory Equipment Utilization Dashboard",
    "Customer Ticket Intelligence System",
    "Data Product Marketplace Prototype",
    "Micro Data Center Commercial Landing Page",
]


def slugify(value: str) -> str:
    """Convert a project name to a repository-safe slug."""

    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def python_package(value: str) -> str:
    """Convert a project name to a Python package-safe identifier."""

    return slugify(value).replace("-", "_")


def domain_for(number: int) -> tuple[str, str, str, str]:
    """Return domain-specific metadata for a project number."""

    if number <= 10:
        return (
            "Healthcare AI",
            "Hospitals, clinics, care management teams and healthtech startups",
            "Synthetic clinical EHR-style tabular dataset",
            "FastAPI clinical risk scoring API",
        )
    if number <= 20:
        return (
            "Clinical Data Science",
            "Hospital executives, clinical quality teams and operations leaders",
            "Synthetic hospital operations and clinical quality dataset",
            "FastAPI analytics API and dashboard-ready outputs",
        )
    if number <= 30:
        return (
            "Pharmacovigilance",
            "Pharmaceutical safety teams, CROs and regulatory affairs groups",
            "Synthetic FAERS-style adverse event and case narrative dataset",
            "FastAPI case triage and safety signal API",
        )
    if number <= 40:
        return (
            "Drug Discovery",
            "Biotech startups, medicinal chemistry teams and research labs",
            "Simulated molecular descriptors and public-ready compound metadata",
            "FastAPI molecular scoring API",
        )
    if number <= 50:
        return (
            "Crystallography and Scientific HPC",
            "Structural biology labs, crystallography groups and HPC users",
            "Simulated diffraction, image and HPC job telemetry dataset",
            "FastAPI scientific workflow API",
        )
    if number <= 60:
        return (
            "Bioinformatics",
            "Genomics labs, translational research teams and universities",
            "Synthetic omics matrix, variant or sequence metadata",
            "FastAPI bioinformatics workflow API",
        )
    if number <= 70:
        return (
            "Micro Data Center Operations",
            "Micro data center operators, MSPs and infrastructure customers",
            "Synthetic telemetry from racks, GPUs, energy and SLA systems",
            "FastAPI operational intelligence API",
        )
    if number <= 80:
        return (
            "Defensive Cybersecurity",
            "Security teams, compliance officers and healthcare IT departments",
            "Synthetic security logs, findings and access audit events",
            "FastAPI defensive security API",
        )
    if number <= 90:
        return (
            "MLOps and DevSecOps",
            "ML platform teams, regulated AI teams and DevSecOps engineers",
            "Synthetic model lifecycle, drift and validation metadata",
            "FastAPI model operations API",
        )
    return (
        "Business Intelligence and Client Products",
        "Executives, laboratories, researchers and commercial service customers",
        "Synthetic business, laboratory, customer and research operations dataset",
        "FastAPI BI and product backend API",
    )


def build_projects() -> list[Project]:
    """Build project metadata for all 100 requested projects."""

    category_by_block = {
        0: CATEGORIES[0],
        1: CATEGORIES[1],
        2: CATEGORIES[3],
        3: CATEGORIES[2],
        4: CATEGORIES[4],
        5: CATEGORIES[5],
        6: CATEGORIES[6],
        7: CATEGORIES[7],
        8: CATEGORIES[8],
        9: CATEGORIES[9],
    }
    projects: list[Project] = []
    for index, name in enumerate(PROJECT_NAMES, start=1):
        category = category_by_block[(index - 1) // 10]
        domain, client, dataset, interface = domain_for(index)
        projects.append(
            Project(
                number=index,
                name=name,
                category=category,
                domain=domain,
                client=client,
                dataset=dataset,
                interface=interface,
                uses_ai=index not in {30, 43, 46, 47, 50, 61, 65, 66, 67, 68, 76, 80, 93, 94, 100},
            )
        )
    return projects


def write_file(path: Path, content: str) -> None:
    """Write text content with normalized trailing newline."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def business_problem(project: Project) -> str:
    """Create a concise business or scientific problem statement."""

    return (
        f"{project.client} need a reliable, secure and explainable way to operationalize "
        f"{project.name.lower()} using data products hosted in a commercial Micro Data Center."
    )


def technical_objective(project: Project) -> str:
    """Create the technical objective."""

    if project.uses_ai:
        return (
            "Build a reproducible data pipeline, baseline machine learning model, validated "
            "inference API, monitoring hooks and governance documentation."
        )
    return (
        "Build a secure analytics and automation service with validated inputs, operational "
        "metrics, auditable logs and deployment-ready infrastructure."
    )


def revenue_model(project: Project) -> str:
    """Return a commercial packaging statement."""

    return (
        f"{project.name} can be sold as a paid discovery workshop, a fixed-scope MVP, "
        "a managed API, an executive dashboard add-on and a monthly compliance/monitoring retainer."
    )


def committee_review(project: Project) -> str:
    """Return a project-level review from the requested committee perspectives."""

    return f"""
    # Committee Review

    Project: {project.name}

    ## Solution Architect

    The project follows a layered architecture with ingestion, validation, service logic, API,
    tests, documentation and deploy assets. Production adoption requires tenant isolation,
    network segmentation and environment-specific deployment manifests.

    ## Senior Data Scientist

    The current implementation is a deterministic professional scaffold. Before client use,
    replace the baseline with a validated dataset, exploratory analysis, statistical validation,
    calibration where relevant and documented limitations.

    ## MLOps Engineer

    The repository includes CI, Docker and testable service boundaries. Production maturity
    should add artifact registry, model versioning, rollback, drift monitoring and release gates.

    ## Security Specialist

    The scaffold includes environment-based configuration, no committed secrets, security headers,
    validated requests and safe logging. Production requires IAM, secret management, vulnerability
    scanning, SAST/DAST and centralized audit logs.

    ## LGPD/HIPAA Specialist

    Synthetic data is used by default. Real deployments require DPIA/LIA or equivalent privacy
    assessment, data processing agreements, data minimization, retention policy and documented
    lawful basis.

    ## Digital Health Specialist

    This project is decision-support oriented. Clinical or laboratory decisions require human
    oversight, local protocol alignment and validation with domain experts.

    ## Micro Data Center CTO

    Commercial readiness depends on repeatable deployment, observability, SLA management,
    customer onboarding, support processes and a sustainable pricing model.
    """


def architecture(project: Project) -> str:
    """Create a compact architecture narrative."""

    return (
        "Data ingestion -> validation -> preprocessing -> analytics/model service -> "
        "FastAPI interface -> logs/metrics -> dashboard or client integration."
    )


def project_readme(project: Project) -> str:
    """Return README content for a project."""

    return f"""
    # {project.name}

    Professional Micro Data Center portfolio project for **{project.domain}**.

    ## Business or Scientific Problem

    {business_problem(project)}

    ## Target Client

    {project.client}.

    ## Technical Objective

    {technical_objective(project)}

    ## Solution Architecture

    `{architecture(project)}`

    ## Executive Value

    - Demonstrates a sellable Micro Data Center service for {project.domain}.
    - Provides a secure starting point for client discovery and proof-of-concept delivery.
    - Separates code, data, documentation, tests and deployment assets.
    - Includes compliance, risk and governance documentation expected by enterprise clients.

    ## Technologies

    Python, FastAPI, Pydantic, pandas, NumPy, scikit-learn, pytest, Docker, GitHub Actions,
    structured logging and environment-based configuration.

    ## Dataset

    {project.dataset}. No real patient, customer, compound or infrastructure secrets are committed.

    ## API

    - `GET /health`
    - `GET /ready`
    - `GET /metrics`
    - `POST /predict` or `/analyze`

    ## Security and Privacy

    This project includes `.env.example`, input validation, synthetic data, safe logging,
    privacy-by-design notes, LGPD/HIPAA guidance when applicable and a production checklist.

    ## Run Locally

    ```bash
    python -m venv .venv
    pip install -r requirements.txt
    pytest -q
    uvicorn src.api.main:app --reload
    ```

    ## Docker

    ```bash
    docker compose up --build
    ```

    ## Monetization

    {revenue_model(project)}

    ## Roadmap

    1. Replace synthetic data with governed client data.
    2. Add authentication, authorization and tenant isolation.
    3. Add observability, drift monitoring and SLA reporting.
    4. Add client-specific dashboard and executive reports.
    5. Validate with domain experts before operational use.

    ## Committee Notes

    See `docs/committee_review.md` for a review from solution architecture, data science,
    MLOps, security, LGPD/HIPAA, digital health and Micro Data Center CTO perspectives.
    """


def src_config(project: Project) -> str:
    package = python_package(project.name)
    return f'''
    """Configuration for {project.name}."""

    from functools import lru_cache

    from pydantic import Field
    from pydantic_settings import BaseSettings, SettingsConfigDict


    class Settings(BaseSettings):
        """Runtime settings loaded from environment variables."""

        app_name: str = "{project.name}"
        app_env: str = Field(default="development", alias="APP_ENV")
        log_level: str = Field(default="INFO", alias="LOG_LEVEL")
        model_version: str = Field(default="prototype", alias="MODEL_VERSION")
        prediction_threshold: float = Field(default=0.5, alias="PREDICTION_THRESHOLD")

        model_config = SettingsConfigDict(env_file=".env", extra="ignore")


    @lru_cache
    def get_settings() -> Settings:
        """Return cached settings."""

        return Settings()


    PROJECT_PACKAGE = "{package}"
    '''


def src_api(project: Project) -> str:
    action = "predict" if project.uses_ai else "analyze"
    response_field = "risk_score" if project.uses_ai else "health_score"
    return f'''
    """FastAPI application for {project.name}."""

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
        title="{project.name}",
        version="0.1.0",
        description="Commercial Micro Data Center portfolio API. Not for regulated production use without validation.",
    )

    SERVICE_METRICS = {{"requests_total": 0, "errors_total": 0, "last_latency_ms": 0.0}}


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
        {response_field}: float
        classification: str
        model_version: str
        disclaimer: str


    @app.get("/health")
    def health() -> dict[str, str]:
        """Return service health."""

        return {{"status": "ok", "project": settings.app_name, "environment": settings.app_env}}


    @app.get("/ready")
    def ready() -> dict[str, str]:
        """Return readiness for orchestration and client demos."""

        return {{"status": "ready", "project": settings.app_name}}


    @app.get("/metrics")
    def metrics() -> dict[str, float | int]:
        """Return minimal non-sensitive operational metrics."""

        return SERVICE_METRICS


    @app.post("/{action}", response_model=AnalysisResponse)
    def {action}(payload: AnalysisRequest) -> AnalysisResponse:
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
    '''


def pipeline(project: Project) -> str:
    response_field = "risk_score" if project.uses_ai else "health_score"
    return f'''
    """Reusable pipeline logic for {project.name}."""

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
        return {{
            "entity_id": str(payload["entity_id"]),
            "{response_field}": round(score, 4),
            "classification": classify_score(score),
            "disclaimer": "Decision support prototype only. Requires domain validation before production use.",
        }}
    '''


def logger_py() -> str:
    return '''
    """Logging utilities."""

    import logging
    import sys


    def get_logger(name: str, level: str = "INFO") -> logging.Logger:
        """Return a configured logger."""

        logger = logging.getLogger(name)
        if logger.handlers:
            return logger
        logger.setLevel(level.upper())
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
        logger.addHandler(handler)
        return logger
    '''


def tests(project: Project) -> str:
    action = "predict" if project.uses_ai else "analyze"
    score_field = "risk_score" if project.uses_ai else "health_score"
    return f'''
    """API and pipeline tests for {project.name}."""

    from fastapi.testclient import TestClient

    from src.api.main import app
    from src.services.pipeline import run_pipeline


    def test_health_endpoint():
        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert "X-Request-ID" in response.headers


    def test_ready_and_metrics_endpoints():
        client = TestClient(app)

        ready = client.get("/ready")
        metrics = client.get("/metrics")

        assert ready.status_code == 200
        assert ready.json()["status"] == "ready"
        assert metrics.status_code == 200
        assert "requests_total" in metrics.json()


    def test_pipeline_returns_valid_score():
        result = run_pipeline({{"entity_id": "demo-001", "numeric_signal": 500, "severity": 3}})

        assert 0 <= result["{score_field}"] <= 1
        assert result["classification"] in {{"low", "medium", "high"}}


    def test_{action}_endpoint():
        client = TestClient(app)
        response = client.post(
            "/{action}",
            json={{"entity_id": "demo-001", "numeric_signal": 500, "severity": 3, "context": "test"}},
        )

        assert response.status_code == 200
        assert 0 <= response.json()["{score_field}"] <= 1


    def test_{action}_endpoint_rejects_invalid_payload():
        client = TestClient(app)
        response = client.post(
            "/{action}",
            json={{"entity_id": "x", "numeric_signal": -1, "severity": 8, "context": "test"}},
        )

        assert response.status_code == 422
    '''


def test_conftest() -> str:
    return '''
    """Ensure project-local imports win inside the portfolio monorepo."""

    from __future__ import annotations

    import sys
    from pathlib import Path


    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(PROJECT_ROOT))
    '''


def security_policy(project: Project) -> str:
    return f"""
    # Security Policy

    ## Scope

    {project.name} is a professional portfolio scaffold for commercial Micro Data Center services.
    It uses synthetic or governed data only and must not process real sensitive data without
    security, privacy and contractual controls.

    ## Included Controls

    - `.env.example` with no secrets.
    - `.gitignore` blocking `.env`, generated data and artifacts.
    - Pydantic request validation.
    - HTTP security headers.
    - Non-sensitive metrics endpoint.
    - Safe logging without raw payloads.
    - Docker non-root user.
    - CI with pytest.

    ## Production Requirements

    - IAM and least privilege.
    - Secret manager.
    - TLS everywhere.
    - SAST, dependency scanning and container scanning.
    - Centralized audit logs.
    - Backup, restore and incident response.
    - Client data processing agreement.
    """


def contributing(project: Project) -> str:
    return f"""
    # Contributing

    ## Quality Bar

    Contributions to {project.name} must preserve a professional standard suitable for
    healthcare, science, security or commercial Micro Data Center clients.

    ## Checklist

    - Tests pass with `pytest -q`.
    - No secrets, PHI, PII or client data are committed.
    - API contracts remain backward compatible or are documented.
    - Security and compliance docs are updated when behavior changes.
    - New model logic includes validation notes and risk analysis.
    """


def pyproject(project: Project) -> str:
    return f"""
    [build-system]
    requires = ["setuptools>=68"]
    build-backend = "setuptools.build_meta"

    [project]
    name = "{slugify(project.name)}"
    version = "0.1.0"
    description = "{project.domain} Micro Data Center portfolio project."
    requires-python = ">=3.10"

    [tool.pytest.ini_options]
    testpaths = ["tests"]
    pythonpath = ["."]
    addopts = "-q"

    [tool.ruff]
    line-length = 100
    target-version = "py310"
    """


def dockerignore() -> str:
    return """
    .git
    .github
    .venv
    __pycache__
    .pytest_cache
    .env
    data/raw/*.csv
    data/processed/*.csv
    artifacts
    notebooks/.ipynb_checkpoints
    """


def common_docs(project: Project, doc_name: str) -> str:
    titles = {
        "architecture": "Architecture",
        "security": "Security and Privacy",
        "methodology": "Methodology",
        "deployment": "Deployment",
        "compliance": "Compliance",
    }
    title = titles[doc_name]
    return f"""
    # {title}

    Project: {project.name}

    ## Summary

    {business_problem(project)}

    ## Architecture

    {architecture(project)}

    ## Controls

    - Synthetic or governed data only.
    - Environment-based configuration.
    - Pydantic validation.
    - Logs without personal, clinical or commercial secrets.
    - Docker-ready deployment.
    - CI with pytest.

    ## Production Checklist

    - Identity and access management.
    - Tenant isolation.
    - Encrypted storage and transport.
    - Audit logging.
    - Backup and disaster recovery.
    - Monitoring and alerting.
    - Domain expert validation.
    - Legal, privacy and security review.
    """


def operations_doc(project: Project) -> str:
    return f"""
    # Operations Runbook

    Project: {project.name}

    ## Health Checks

    - `GET /health`: process-level health.
    - `GET /ready`: readiness for demos and orchestration.
    - `GET /metrics`: non-sensitive operational counters.

    ## Incident Response

    1. Confirm service health and recent deployment.
    2. Review logs using request IDs, not raw sensitive payloads.
    3. Roll back to last approved container image.
    4. Notify client stakeholders according to SLA.
    5. Document root cause and corrective actions.

    ## SLA Targets for Commercial Demo

    - API availability target: 99.5 percent for pilot.
    - Initial response time target: under 500 ms for synthetic demos.
    - Recovery time objective: 4 hours for pilot.
    - Recovery point objective: no committed sensitive data; client data governed separately.
    """


def monitoring_doc(project: Project) -> str:
    return f"""
    # Monitoring Plan

    Project: {project.name}

    ## Metrics

    - Request volume.
    - Error count and error rate.
    - Latency percentiles.
    - Classification distribution.
    - Data quality failures.
    - Drift indicators when a model is added.

    ## Alerts

    - Elevated 5xx errors.
    - Unexpected classification distribution shift.
    - Missing input fields or validation spikes.
    - Container restart loops.
    - Disk, CPU, memory or GPU saturation.
    """


def commercial_doc(project: Project) -> str:
    return f"""
    # Commercial Offer

    Project: {project.name}

    ## Offer

    {revenue_model(project)}

    ## Ideal Buyers

    {project.client}.

    ## Packaging

    - Discovery workshop.
    - Two-week proof of concept.
    - Managed API deployment.
    - Executive dashboard.
    - Monitoring and compliance retainer.

    ## Success Metrics

    - Reduced manual analysis time.
    - Faster operational decision-making.
    - Improved audit readiness.
    - Clear SLA and support boundaries.
    """


def production_checklist(project: Project) -> str:
    return f"""
    # Production Checklist

    Project: {project.name}

    - [ ] Client owner and technical owner assigned.
    - [ ] Data classification completed.
    - [ ] LGPD/HIPAA or applicable privacy review completed.
    - [ ] Secrets moved to a managed secret store.
    - [ ] Authentication and authorization enabled.
    - [ ] TLS configured.
    - [ ] Logs centralized and scrubbed.
    - [ ] Backups and restore tested.
    - [ ] Monitoring and alerts enabled.
    - [ ] Security scans completed.
    - [ ] Domain expert validation completed.
    - [ ] Rollback plan documented.
    """


def reports(project: Project, report_name: str) -> str:
    titles = {
        "model_card": "Model Card",
        "data_dictionary": "Data Dictionary",
        "risk_analysis": "Risk Analysis",
        "validation_report": "Validation Report",
    }
    title = titles[report_name]
    model_text = "This project uses an AI/ML baseline scaffold." if project.uses_ai else "This project uses deterministic analytics/automation scaffold logic."
    return f"""
    # {title}

    Project: {project.name}

    ## Scope

    {model_text}

    ## Data

    Dataset strategy: {project.dataset}.

    ## Key Fields

    - `entity_id`: synthetic identifier.
    - `numeric_signal`: normalized operational or scientific signal.
    - `severity`: ordinal priority from 1 to 5.
    - `context`: non-sensitive scenario label.

    ## Risks

    - Synthetic data may not represent production distributions.
    - Unvalidated models can create operational or clinical harm.
    - Poor access control can expose sensitive client data.
    - Alert fatigue can reduce operational value.

    ## Mitigations

    - Human review for all high-impact decisions.
    - Privacy review before real data use.
    - Monitoring, audit trails and rollback.
    - Client-specific validation before launch.
    """


def notebook() -> str:
    return json.dumps(
        {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["# Portfolio Notebook\n", "\n", "Starter notebook for exploration, modeling and validation."],
                }
            ],
            "metadata": {
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python"},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        },
        indent=2,
    )


def generate_project(project: Project) -> None:
    """Generate a single project directory."""

    slug = f"{project.number:03d}_{slugify(project.name)}"
    base = ROOT / project.category.folder / slug
    package = python_package(project.name)

    write_file(base / "README.md", project_readme(project))
    write_file(base / "SECURITY.md", security_policy(project))
    write_file(base / "CONTRIBUTING.md", contributing(project))
    write_file(base / "LICENSE", "MIT License\n\nCopyright (c) 2026 Micro Data Center Portfolio")
    write_file(
        base / ".gitignore",
        ".env\n.venv/\n__pycache__/\n.pytest_cache/\ndata/raw/*.csv\ndata/processed/*.csv\nartifacts/\n",
    )
    write_file(base / ".dockerignore", dockerignore())
    write_file(
        base / ".env.example",
        f"APP_ENV=development\nLOG_LEVEL=INFO\nMODEL_VERSION={slug}\nPREDICTION_THRESHOLD=0.50\n",
    )
    write_file(
        base / "requirements.txt",
        "fastapi>=0.111.0\nuvicorn[standard]>=0.30.0\npydantic>=2.7.0\npydantic-settings>=2.2.0\npytest>=8.2.0\nhttpx>=0.27.0\npandas>=2.2.0\nnumpy>=1.26.0\nscikit-learn>=1.4.0\n",
    )
    write_file(base / "pyproject.toml", pyproject(project))
    write_file(
        base / "Dockerfile",
        'FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nRUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app\nUSER appuser\nEXPOSE 8000\nCMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]',
    )
    write_file(
        base / "docker-compose.yml",
        "services:\n  api:\n    build: .\n    ports:\n      - \"8000:8000\"\n    env_file:\n      - .env.example\n",
    )
    write_file(
        base / "Makefile",
        ".PHONY: install test api docker\n\ninstall:\n\tpip install -r requirements.txt\n\ntest:\n\tpytest -q\n\napi:\n\tuvicorn src.api.main:app --reload\n\ndocker:\n\tdocker compose up --build\n",
    )
    write_file(base / "data" / "README.md", "Synthetic or governed client data only. Do not commit sensitive data.")
    write_file(base / "data" / "raw" / ".gitkeep", "")
    write_file(base / "data" / "processed" / ".gitkeep", "")
    for notebook_name in ["01_exploration.ipynb", "02_modeling.ipynb", "03_validation.ipynb"]:
        write_file(base / "notebooks" / notebook_name, notebook())
    write_file(base / "src" / "__init__.py", f'"""Package for {project.name}."""')
    write_file(base / "src" / "config.py", src_config(project))
    write_file(base / "src" / "api" / "__init__.py", '"""API package."""')
    write_file(base / "src" / "api" / "main.py", src_api(project))
    write_file(base / "src" / "services" / "__init__.py", '"""Services package."""')
    write_file(base / "src" / "services" / "pipeline.py", pipeline(project))
    write_file(base / "src" / "utils" / "__init__.py", '"""Utilities package."""')
    write_file(base / "src" / "utils" / "logger.py", logger_py())
    write_file(base / "src" / "data" / "__init__.py", '"""Data package."""')
    write_file(base / "src" / "features" / "__init__.py", '"""Feature package."""')
    write_file(base / "src" / "models" / "__init__.py", '"""Models package."""')
    write_file(base / "tests" / "conftest.py", test_conftest())
    write_file(base / "tests" / "test_api.py", tests(project))
    for doc_name in ["architecture", "security", "methodology", "deployment", "compliance"]:
        write_file(base / "docs" / f"{doc_name}.md", common_docs(project, doc_name))
    write_file(base / "docs" / "committee_review.md", committee_review(project))
    write_file(base / "docs" / "operations_runbook.md", operations_doc(project))
    write_file(base / "docs" / "monitoring.md", monitoring_doc(project))
    write_file(base / "docs" / "commercial_offer.md", commercial_doc(project))
    write_file(base / "docs" / "production_checklist.md", production_checklist(project))
    for report_name in ["model_card", "data_dictionary", "risk_analysis", "validation_report"]:
        write_file(base / "reports" / f"{report_name}.md", reports(project, report_name))
    write_file(
        base / ".github" / "workflows" / "ci.yml",
        "name: CI\n\non: [push, pull_request]\n\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with:\n          python-version: '3.11'\n      - run: pip install -r requirements.txt\n      - run: pytest -q\n",
    )
    write_file(base / "project_metadata.json", json.dumps(project.__dict__ | {"package": package}, indent=2, default=str))


def generate_root(projects: list[Project]) -> None:
    """Generate root portfolio files."""

    write_file(
        ROOT / "README.md",
        """
        # Micro Data Center AI Health Portfolio

        Commercial-grade portfolio with 100 professional project blueprints for a Micro Data Center focused on AI, healthcare, clinical data science, pharmacovigilance, drug discovery, crystallography, bioinformatics, HPC, cybersecurity, MLOps, DevSecOps and executive analytics.

        ## Value Proposition

        This ecosystem demonstrates how a specialized Micro Data Center can offer secure, governed and reproducible data products to hospitals, laboratories, universities, biotechnology companies, pharmaceutical teams, startups and enterprise clients.

        ## Portfolio Contents

        - 100 project repositories organized into 10 business categories.
        - Shared templates for README, security, compliance and model governance.
        - Reusable FastAPI scaffold with Pydantic validation and security headers.
        - Docker, docker-compose, Makefile and GitHub Actions CI in every project.
        - Documentation for commercialization, LinkedIn presentation and service roadmap.

        ## Commercial Positioning

        The portfolio can be presented as a catalog of proof-of-concept services that evolve into managed APIs, dashboards, compliance packages, hosted workloads, research support and long-term managed data products.
        """,
    )
    lines = [
        "# Portfolio Index",
        "",
        "| # | Project | Category | Target Client | Dataset | Interface |",
        "|---|---|---|---|---|---|",
    ]
    for project in projects:
        slug = f"{project.number:03d}_{slugify(project.name)}"
        path = f"{project.category.folder}/{slug}"
        lines.append(
            f"| {project.number} | [{project.name}]({path}) | {project.category.title} | {project.client} | {project.dataset} | {project.interface} |"
        )
    write_file(ROOT / "portfolio_index.md", "\n".join(lines))
    write_file(
        ROOT / "docs" / "micro_datacenter_commercial_strategy.md",
        """
        # Micro Data Center Commercial Strategy

        ## Offers

        - Managed AI inference APIs.
        - Clinical analytics dashboards.
        - Pharmacovigilance automation.
        - Scientific HPC workflow hosting.
        - Bioinformatics pipelines as a service.
        - Security and compliance evidence automation.
        - MLOps and model governance platforms.

        ## Buyer Personas

        Hospitals, laboratories, universities, pharmaceutical companies, biotech startups,
        research groups, clinics, managed service providers and healthcare technology companies.

        ## Revenue Models

        - Proof-of-concept project fee.
        - Monthly managed service.
        - Usage-based compute billing.
        - Premium support and compliance documentation.
        - Custom dashboard and API integration.
        """,
    )
    write_file(
        ROOT / "docs" / "github_publication_plan.md",
        """
        # GitHub Publication Plan

        1. Publish the root portfolio repository.
        2. Pin the README and portfolio index.
        3. Add GitHub topics: healthcare-ai, micro-datacenter, mlops, hpc, bioinformatics, cybersecurity.
        4. Use releases for portfolio milestones.
        5. Convert the strongest projects into standalone repositories.
        6. Add screenshots and demo videos for dashboard projects.
        """,
    )
    write_file(
        ROOT / "docs" / "linkedin_presentation_plan.md",
        """
        # LinkedIn Presentation Plan

        ## Short Post

        I built a 100-project professional portfolio for a Micro Data Center specialized in AI for healthcare, clinical data science, pharmacovigilance, drug discovery, crystallography, bioinformatics, HPC, cybersecurity, MLOps and executive analytics.

        The ecosystem includes APIs, Docker, CI, security documentation, LGPD/HIPAA guidance, model cards, risk analysis and commercialization roadmaps.

        ## Weekly Content Series

        - Week 1: Micro Data Center vision.
        - Week 2: Healthcare AI and clinical risk models.
        - Week 3: Pharmacovigilance and drug safety.
        - Week 4: Drug discovery and bioinformatics.
        - Week 5: HPC, crystallography and scientific workflows.
        - Week 6: Cybersecurity, compliance and MLOps.
        """,
    )
    write_file(
        ROOT / "docs" / "service_roadmap.md",
        """
        # Roadmap to Real Client Services

        1. Select 10 flagship projects for deeper implementation.
        2. Add authentication, tenant isolation and observability.
        3. Build demo dashboards and hosted API demos.
        4. Define pricing packages and SLAs.
        5. Validate regulated use cases with domain experts.
        6. Add model registry, audit evidence and incident response.
        7. Convert recurring client needs into managed products.
        """,
    )
    write_file(
        ROOT / "docs" / "committee_review_summary.md",
        """
        # Committee Review Summary

        ## Solution Architecture

        The ecosystem is organized as a portfolio of 100 reproducible project repositories,
        each with API, tests, Docker, CI, documentation, compliance notes and commercial framing.

        ## Senior Data Science

        Projects are professional starter blueprints. Client conversion requires real data
        discovery, statistical validation, model cards, uncertainty analysis and domain review.

        ## MLOps

        The portfolio demonstrates CI and containerized delivery. Production services should add
        model registry, release approvals, drift monitoring, rollback and performance SLOs.

        ## Security

        Baseline controls include no committed secrets, safe logging, validated APIs, Docker
        non-root execution and security documentation. Production must add IAM, scanning, secret
        management and centralized audit trails.

        ## LGPD/HIPAA

        Synthetic data is used by default. Regulated deployments require privacy impact review,
        client agreements, minimization, retention policy, subject rights process and breach response.

        ## Digital Health

        Healthcare projects are decision-support demonstrations and require clinician review,
        workflow design and local protocol alignment before patient-impacting use.

        ## Micro Data Center CTO

        The portfolio is commercially useful as a service catalog. Priority next steps are flagship
        demos, pricing, onboarding workflow, SLA templates and observability.
        """,
    )
    write_file(
        ROOT / "docs" / "client_presentation_checklist.md",
        """
        # Client Presentation Checklist

        - Open with the Micro Data Center value proposition.
        - Show the 100-project portfolio index.
        - Pick 3 flagship projects aligned to the client's industry.
        - Demonstrate `/health`, `/ready`, `/metrics` and the main API endpoint.
        - Explain synthetic data and privacy-by-design.
        - Walk through security, compliance and production checklist.
        - Offer a paid discovery workshop and a two-week proof of concept.
        - Close with roadmap, SLA assumptions and next steps.
        """,
    )
    write_file(
        ROOT / "docs" / "data_governance_framework.md",
        """
        # Data Governance Framework

        ## Principles

        - Data minimization.
        - Purpose limitation.
        - Synthetic data for public demos.
        - Explicit client approval for real data.
        - Role-based access control.
        - Auditability and retention management.

        ## Data Lifecycle

        1. Intake and classification.
        2. Contract and lawful basis review.
        3. Secure transfer.
        4. Processing in isolated environment.
        5. Monitoring and audit logging.
        6. Retention or deletion according to policy.

        ## Prohibited in Public Repositories

        - PHI, PII, credentials, private keys, client contracts, proprietary datasets and raw logs.
        """,
    )
    write_file(ROOT / "templates" / "README_TEMPLATE.md", project_readme(projects[0]))
    write_file(ROOT / "templates" / "SECURITY_TEMPLATE.md", common_docs(projects[0], "security"))
    write_file(ROOT / "templates" / "MODEL_CARD_TEMPLATE.md", reports(projects[0], "model_card"))
    write_file(
        ROOT / "shared" / "README.md",
        "Shared utilities and patterns for portfolio projects: validation, logging, model governance, API security and deployment checklists.",
    )
    write_file(
        ROOT / "infrastructure" / "README.md",
        "Infrastructure blueprints for Micro Data Center deployments: Docker, reverse proxy, monitoring, backup, IAM, network segmentation and evidence collection.",
    )


def main() -> None:
    """Generate the complete portfolio."""

    projects = build_projects()
    for category in CATEGORIES:
        write_file(ROOT / category.folder / "README.md", f"# {category.title}\n\n{category.description}")
    for project in projects:
        generate_project(project)
    generate_root(projects)
    print(f"Generated {len(projects)} projects under {ROOT}")


if __name__ == "__main__":
    main()
