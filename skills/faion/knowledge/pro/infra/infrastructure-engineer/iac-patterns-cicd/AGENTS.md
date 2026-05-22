---
slug: iac-patterns-cicd
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: CI/CD pipeline patterns for Terraform: a six-stage GitHub Actions workflow (fmt/validate/lint/security/plan/apply), OIDC for credential-free cloud authentication, PR plan comments for review, environment-specific apply jobs with approval gates, and scheduled drift detection.
content_id: "609858eba8a6614b"
tags: [terraform, cicd, github-actions, iac, drift-detection]
---
# IaC CI/CD Integration Patterns

## Summary

**One-sentence:** CI/CD pipeline patterns for Terraform: a six-stage GitHub Actions workflow (fmt/validate/lint/security/plan/apply), OIDC for credential-free cloud authentication, PR plan comments for review, environment-specific apply jobs with approval gates, and scheduled drift detection.

**One-paragraph:** CI/CD pipeline patterns for Terraform: a six-stage GitHub Actions workflow (fmt/validate/lint/security/plan/apply), OIDC for credential-free cloud authentication, PR plan comments for review, environment-specific apply jobs with approval gates, and scheduled drift detection.

## Applies If (ALL must hold)

- Any Terraform project with more than one contributor — enforce plan-before-apply via CI.
- Infrastructure with compliance or audit requirements — CI provides an immutable apply log.
- Multi-environment deployments (dev/staging/prod) — use matrix strategy to plan all environments on PR.
- Production infrastructure — add approval gates before apply on merge to main.
- Long-lived infrastructure — add scheduled drift detection to catch out-of-band changes.

## Skip If (ANY kills it)

- Throwaway or one-time environments — pipeline setup overhead exceeds value for ephemeral infra.
- Local development inner loop — run fmt/validate locally; reserve CI for pre-merge gates.
- Drift detection when environment changes are expected (active development phase) — generates false-positive noise.

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

- parent skill: `pro/infra/infrastructure-engineer/`
