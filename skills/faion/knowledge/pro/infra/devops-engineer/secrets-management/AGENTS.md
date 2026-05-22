---
slug: secrets-management
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Secrets management in 2025-2026 means eliminating static, long-lived credentials: apps authenticate via cloud identity (IRSA, Workload Identity, OIDC) and receive short-lived dynamic credentials from a secrets backend.
content_id: "e83104b0ec0cd4f4"
tags: [secrets, vault, kubernetes, oidc, eso]
---
# Secrets Management

## Summary

**One-sentence:** Secrets management in 2025-2026 means eliminating static, long-lived credentials: apps authenticate via cloud identity (IRSA, Workload Identity, OIDC) and receive short-lived dynamic credentials from a secrets backend.

**One-paragraph:** Secrets management in 2025-2026 means eliminating static, long-lived credentials: apps authenticate via cloud identity (IRSA, Workload Identity, OIDC) and receive short-lived dynamic credentials from a secrets backend. Kubernetes integration uses External Secrets Operator (ESO) as the standard bridge between any backend and pod-level secret injection. Rotation must be automated on a 30-day or shorter cycle.

## Applies If (ALL must hold)

- Application needs database credentials, API keys, or TLS certificates at runtime
- Kubernetes workloads require secrets without storing them as native K8s Secrets in plain base64
- CI/CD pipelines must authenticate to cloud providers without stored access keys
- Compliance requires secret rotation, audit logging, and access control (SOC2, HIPAA, PCI-DSS)

## Skip If (ANY kills it)

- Development-only local environment — .env files are acceptable; do not add Vault overhead
- Secrets that are truly public (public API keys, non-sensitive config values) — use ConfigMaps, not secrets backends
- Single-cloud project where the cloud provider's native secrets service (AWS Secrets Manager, GCP Secret Manager) covers all use cases — adding Vault is unnecessary operational overhead

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

- parent skill: `pro/infra/devops-engineer/`
