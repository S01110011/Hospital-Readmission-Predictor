# Security Policy

## Scope

Pharmacovigilance Case Prioritizer is a professional portfolio scaffold for commercial Micro Data Center services.
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
