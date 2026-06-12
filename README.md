# Hospital Readmission Predictor

End-to-end Machine Learning project for predicting 30-day hospital readmission risk using synthetic clinical tabular data, healthcare privacy practices, FastAPI inference, Docker, automated tests and model governance documentation.

> Clinical disclaimer: this project is for portfolio, education and technical demonstration only. It is not a medical device and does not replace healthcare professionals, clinical protocols or institutional decision-making.

## Why This Project Matters

Hospital readmissions can reflect clinical deterioration, fragmented discharge planning, medication complexity, chronic disease burden or barriers to follow-up care. A readmission risk model can help care teams prioritize post-discharge outreach, medication reconciliation and transition-of-care programs.

In healthcare, model evaluation must go beyond accuracy. For readmission prediction, a false negative may mean missing a patient who needs preventive follow-up. This project therefore emphasizes **recall**, while still reporting precision, F1-score, ROC-AUC, confusion matrix, ROC curve and Precision-Recall curve.

## What Is Included

- Synthetic clinical dataset generator with no real patient data.
- Data validation, cleaning and preprocessing pipeline.
- Feature engineering with clinically interpretable derived variables.
- Model comparison across Logistic Regression, Random Forest and Gradient Boosting.
- Recall-first model selection with ROC-AUC as tie-breaker.
- FastAPI service with `/health`, `/ready`, `/model-info` and `/predict`.
- Pydantic request validation and dataframe schema validation.
- Model artifact metadata with training timestamp, metrics and SHA-256 hash.
- Security headers, restricted CORS configuration and `.env.example`.
- Dockerfile, docker-compose, Makefile and GitHub Actions CI.
- Tests for preprocessing, validation, model inference and API endpoints.
- Documentation for architecture, methodology, deployment, security, governance, model card and data dictionary.

## Repository Structure

```text
Hospital-Readmission-Predictor/
|-- .github/workflows/ci.yml
|-- artifacts/README.md
|-- data/
|   |-- raw/
|   |-- processed/
|   `-- README.md
|-- docs/
|   |-- architecture.md
|   |-- deployment.md
|   |-- github_linkedin.md
|   |-- governance.md
|   |-- methodology.md
|   `-- security.md
|-- notebooks/
|   |-- 01_eda.ipynb
|   |-- 02_modeling.ipynb
|   `-- 03_explainability.ipynb
|-- reports/
|   |-- data_dictionary.md
|   |-- model_card.md
|   `-- risk_analysis.md
|-- scripts/
|   `-- generate_sample_data.py
|-- src/
|   |-- api/
|   |-- data/
|   |-- features/
|   |-- models/
|   `-- utils/
|-- tests/
|-- Dockerfile
|-- docker-compose.yml
|-- Makefile
|-- README.md
|-- requirements.txt
`-- SECURITY.md
```

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows PowerShell
pip install -r requirements.txt
python scripts/generate_sample_data.py
python -m src.models.train
pytest -q
```

## Run the API

```bash
uvicorn src.api.main:app --reload
```

Open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`
- Readiness check: `http://127.0.0.1:8000/ready`
- Model metadata: `http://127.0.0.1:8000/model-info`

## Prediction Example

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 72,
    "gender": "female",
    "length_of_stay": 8,
    "num_prior_admissions": 2,
    "num_medications": 11,
    "num_lab_procedures": 58,
    "comorbidity_score": 5,
    "discharge_disposition": "home_health",
    "primary_diagnosis": "heart_failure",
    "has_diabetes": true,
    "has_hypertension": true,
    "has_ckd": false,
    "follow_up_scheduled": false
  }'
```

Response:

```json
{
  "readmission_probability": 0.7421,
  "risk_class": "alto",
  "threshold": 0.5,
  "model_version": "local"
}
```

## Docker

```bash
docker compose up --build
```

The container generates synthetic data, trains the model and starts the API on port `8000`.

## Model Artifacts

Training writes local artifacts to `artifacts/`:

- `model.joblib`
- `metrics.json`
- `model_summary.json`
- `confusion_matrix.png`
- `roc_curve.png`
- `precision_recall_curve.png`

Generated artifacts are intentionally ignored by Git. In production, use a model registry with approval workflow, integrity hashes and rollback.

## Security and Privacy

This project uses synthetic data only. No real patient data, credentials or PHI should be committed. Security-oriented controls include `.env.example`, ignored `.env`, Pydantic validation, dataframe validation, CORS configuration, security headers and governance documentation.

For real use, the project would require LGPD/HIPAA review, data protection impact assessment, access controls, encryption, audit logs, monitoring, clinical validation and institutional approval.

## Key Documents

- [Architecture](docs/architecture.md)
- [Methodology](docs/methodology.md)
- [Security](docs/security.md)
- [Model Governance](docs/governance.md)
- [Deployment](docs/deployment.md)
- [Model Card](reports/model_card.md)
- [Data Dictionary](reports/data_dictionary.md)
- [GitHub and LinkedIn Guide](docs/github_linkedin.md)

## Related Portfolio Ecosystem

The 100-project Micro Data Center AI and Health commercial portfolio was transferred to its own dedicated repository:

[Micro Data Center AI Health Portfolio](https://github.com/S01110011/Micro-Data-Center-Ai-Health-Portfolio)

## Suggested GitHub Publication

```bash
git add .
git commit -m "Initial professional healthcare ML readmission predictor"
git branch -M main
git remote add origin https://github.com/<your-user>/Hospital-Readmission-Predictor.git
git push -u origin main
```

## Suggested Commits

1. `chore: scaffold healthcare ml repository`
2. `feat: add synthetic clinical data pipeline`
3. `feat: train and compare readmission models`
4. `feat: expose validated FastAPI inference service`
5. `test: cover preprocessing model and api behavior`
6. `docs: add security governance and model card`
7. `ci: add automated test workflow`

## Future Improvements

- Validate with a real public dataset under its license and governance constraints.
- Add probability calibration and threshold optimization by operational capacity.
- Add SHAP reports for model explainability.
- Add subgroup fairness analysis.
- Add authentication, authorization and audit logging.
- Add drift monitoring and model registry integration.
- Deploy with CI/CD, vulnerability scanning and observability.

## License

MIT. See [LICENSE](LICENSE).
