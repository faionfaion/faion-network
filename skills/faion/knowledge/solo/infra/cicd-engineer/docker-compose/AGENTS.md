---
slug: docker-compose
tier: solo
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Docker Compose patterns for CI/CD pipelines: compose.
content_id: "c73dda5c7f775d91"
tags: [docker, compose, ci, github-actions, integration-testing]
---
# Docker Compose (CI/CD)

## Summary

**One-sentence:** Docker Compose patterns for CI/CD pipelines: compose.

**One-paragraph:** Docker Compose patterns for CI/CD pipelines: compose.ci.yaml override that removes port bindings, sets generous start_period for slow CI runners, uses docker compose up -d --wait to block until all health checks pass, and always tears down with docker compose down -v --remove-orphans in an if: always() cleanup step. CI secrets come from environment variables, not .env files.

## Applies If (ALL must hold)

- Spinning up integration test stacks in CI (app + DB + dependencies)
- Building application images in CI with docker compose build before pushing to registry
- Running database migrations and smoke tests against a freshly composed stack
- Parameterizing compose files with override files for local dev vs CI vs production configurations

## Skip If (ANY kills it)

- Production deployments where zero-downtime is required — use Kubernetes rolling updates
- Multi-host deployments in CI — use Kubernetes test clusters or Testcontainers
- Pipelines needing only a single container — docker run in the pipeline is simpler
- Teams with Kubernetes already in production — align CI with prod using helm/kubectl

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

- parent skill: `solo/infra/cicd-engineer/`
