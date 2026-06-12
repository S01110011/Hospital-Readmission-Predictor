# Operations Runbook

Project: Defensive SIEM Mini Platform

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
