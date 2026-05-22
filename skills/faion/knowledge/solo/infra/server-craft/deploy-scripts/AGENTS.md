---
slug: deploy-scripts
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Bash-based deploy orchestrator for workspace/runtime separation: rsync source to runtime, manage Python virtualenvs with `pip install -e.
content_id: "eb38fbb6bc3c50aa"
tags: [deployment, bash, systemd, production, orchestration]
---
# Deploy Scripts

## Summary

**One-sentence:** Bash-based deploy orchestrator for workspace/runtime separation: rsync source to runtime, manage Python virtualenvs with `pip install -e.

**One-paragraph:** Bash-based deploy orchestrator for workspace/runtime separation: rsync source to runtime, manage Python virtualenvs with `pip install -e .`, restart systemd user services, and validate with a health check. A single `deploy.sh <service|all> [--rebuild-venv]` script handles the full lifecycle.

## Applies If (ALL must hold)

- Adding or changing a service on a VPS using workspace/runtime separation pattern
- Setting up initial deploy pipeline for a multi-service Python/Node platform
- Needing rollback capability (`rollback.sh service HEAD~1`)
- Post-deploy health validation before declaring success

## Skip If (ANY kills it)

- Docker-only deployments (use `docker compose up --pull` instead)
- CI/CD-managed deployments (GitHub Actions, GitLab CI)
- Monorepos where workspace and runtime are the same directory

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
