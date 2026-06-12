# Model Artifacts

Training writes local artifacts here:

- `model.joblib`
- `metrics.json`
- `model_summary.json`
- `confusion_matrix.png`
- `roc_curve.png`
- `precision_recall_curve.png`

Generated artifacts are ignored by Git because trained models and metrics should be reproduced or stored in a controlled model registry. In production, use artifact versioning with integrity hashes, approval workflow and rollback capability.
