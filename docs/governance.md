# Model Governance

## Decision Support Boundary

The model estimates readmission risk and should support prioritization, not automate clinical decisions. Final decisions remain with qualified healthcare professionals and institutional protocols.

## Approval Gates for Real Use

1. Data protection impact assessment.
2. Clinical validation with representative retrospective data.
3. Bias and subgroup performance review.
4. Prospective silent trial.
5. Human factors review with clinical teams.
6. Security review and operational readiness.
7. Formal approval by clinical, legal and technology governance.

## Monitoring Plan

- Input data drift by feature.
- Prediction distribution drift.
- Recall, precision and calibration when outcomes become available.
- False negative review for readmitted patients.
- Subgroup performance by age band, diagnosis and discharge disposition.
- Alert volume and clinical workflow impact.

## Retraining Criteria

Retraining should be considered when data drift is persistent, protocols change, performance drops below agreed thresholds, or new populations are added.

## Auditability

Each model artifact should have:

- model version;
- training timestamp;
- dataset reference;
- feature schema;
- metrics;
- approval owner;
- SHA-256 hash;
- rollback plan.
