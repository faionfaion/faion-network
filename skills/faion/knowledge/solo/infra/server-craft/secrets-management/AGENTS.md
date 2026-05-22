---
slug: secrets-management
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Secrets management for solo developer VPS platforms:.
content_id: "e83104b0ec0cd4f4"
tags: [secrets, env-files, 1password, systemd, security]
---
# Secrets Management

## Summary

**One-sentence:** Secrets management for solo developer VPS platforms:.

**One-paragraph:** Secrets management for solo developer VPS platforms: .env file hygiene, systemd EnvironmentFile integration, 1Password CLI (op) for programmatic secret injection, pre-commit hooks to block secret commits, file permission hardening, and secret rotation procedures. Defense-in-depth across file permissions, .gitignore, and git hooks.

## Applies If (ALL must hold)

- Setting up a new project requiring API keys, database credentials, or JWT secrets
- Deploying a service to production where .env must be generated from a secrets manager
- Rotating a compromised or expired credential across all services
- Auditing a codebase for hardcoded secrets or improper .env handling
- Configuring systemd EnvironmentFile for a new user service

## Skip If (ANY kills it)

- Compliance environments requiring HashiCorp Vault or AWS Secrets Manager with audit trails
- Short-lived ephemeral scripts that do not need persistent secrets
- Public configuration values (feature flags, log levels) that do not require protection

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/infra/server-craft/`
