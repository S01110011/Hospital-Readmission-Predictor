# Security Policy

## Supported Use

This repository is a portfolio and educational project. It uses synthetic data and must not be used as a clinical system without formal security, legal, privacy and clinical validation.

## Reporting a Vulnerability

If this project is published publicly and you identify a security issue, open a private advisory in GitHub or contact the maintainer directly. Do not include real patient data in issue descriptions, screenshots or logs.

## Security Controls Included

- No real patient data is committed.
- `.env` is ignored and `.env.example` documents configuration only.
- API input is validated with Pydantic and dataframe validation.
- Model artifact metadata includes version, training timestamp and SHA-256 hash.
- API responses include conservative security headers.
- CORS is disabled by default unless explicit origins are configured.
- Docker image builds from reproducible project files.

## Production Requirements

Before real healthcare use, add authentication, authorization, TLS, centralized audit logging, vulnerability scanning, secret management, encrypted storage, access reviews, incident response, model monitoring and formal governance under LGPD/HIPAA or the applicable local regulation.
