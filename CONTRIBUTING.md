# Contributing

## Development Setup

```bash
python -m venv .venv
pip install -r requirements.txt
python scripts/generate_sample_data.py
python -m src.models.train
pytest -q
```

## Pull Request Checklist

- Tests pass locally.
- No real patient data, credentials or PHI are committed.
- New features include tests or a documented reason for not adding them.
- Documentation is updated when behavior changes.
- Model changes include metrics and clinical rationale.

## Commit Style

Use clear conventional-style commits:

- `feat: add model readiness endpoint`
- `fix: validate null clinical inputs`
- `docs: expand LGPD and HIPAA governance`
- `test: cover model metadata endpoint`
