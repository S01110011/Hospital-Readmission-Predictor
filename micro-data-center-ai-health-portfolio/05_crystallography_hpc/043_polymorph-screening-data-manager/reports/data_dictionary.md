# Data Dictionary

Project: Polymorph Screening Data Manager

## Scope

This project uses deterministic analytics/automation scaffold logic.

## Data

Dataset strategy: Simulated diffraction, image and HPC job telemetry dataset.

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
