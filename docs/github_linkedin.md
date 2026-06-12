# GitHub and LinkedIn Presentation Guide

## GitHub Repository Description

Machine Learning project for hospital readmission risk prediction with synthetic clinical data, reproducible training pipeline, FastAPI inference service, Docker, tests, model governance and healthcare privacy documentation.

## Suggested GitHub Topics

`machine-learning`, `healthcare`, `fastapi`, `scikit-learn`, `clinical-decision-support`, `model-governance`, `lgpd`, `hipaa`, `python`, `data-science`

## LinkedIn Post Draft

I built a professional healthcare ML portfolio project: Hospital Readmission Predictor.

The project demonstrates an end-to-end workflow for predicting 30-day hospital readmission risk using synthetic clinical tabular data. It includes data validation, feature engineering, model comparison, recall-oriented evaluation, FastAPI deployment, Docker, automated tests, model card, security documentation and LGPD/HIPAA-oriented governance notes.

The most important technical lesson: in healthcare, model selection cannot rely on accuracy alone. For readmission risk, false negatives may mean missing patients who need post-discharge support, so recall, calibration, operational capacity and clinical review must be considered together.

## Portfolio Talking Points

- Built a reproducible ML pipeline with three model families.
- Prioritized recall because false negatives carry clinical risk.
- Added privacy-by-design documentation and no real patient data.
- Exposed inference through validated FastAPI endpoints.
- Included CI, Docker and automated tests.
- Documented limitations and governance before real-world use.
