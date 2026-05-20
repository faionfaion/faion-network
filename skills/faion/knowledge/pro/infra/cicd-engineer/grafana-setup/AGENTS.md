---
slug: grafana-setup
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Grafana setup methodology covering Docker Compose, Kubernetes Helm, and High Availability deployment patterns, with configuration-as-code provisioning for data sources, dashboards, and alerting.
content_id: "a6454c9fb651061e"
tags: [grafana, monitoring, provisioning, observability, kubernetes]
---
# Grafana Setup and Provisioning

## Summary

**One-sentence:** Grafana setup methodology covering Docker Compose, Kubernetes Helm, and High Availability deployment patterns, with configuration-as-code provisioning for data sources, dashboards, and alerting.

**One-paragraph:** Grafana setup methodology covering Docker Compose, Kubernetes Helm, and High Availability deployment patterns, with configuration-as-code provisioning for data sources, dashboards, and alerting. Grafana Agent reached EOL on November 1, 2025 — all new deployments must use Grafana Alloy. HA requires PostgreSQL or MySQL (SQLite is single-node only); no session affinity needed since sessions are stored in the database.

## Applies If (ALL must hold)

- Deploying Grafana for the first time in any environment (Docker, K8s, VM)
- Migrating from Grafana Agent to Grafana Alloy (mandatory — Agent EOL Nov 2025)
- Setting up HA Grafana for production with PostgreSQL backend
- Configuring alerting pipelines with contact points and notification policies
- Managing Grafana infrastructure as code with Terraform or Helm

## Skip If (ANY kills it)

- Quick local exploration with no persistence requirement — use `docker run grafana/grafana` directly
- When Grafana Cloud is available and operational complexity must be zero
- When the only requirement is viewing existing dashboards — no setup needed, just access

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

- parent skill: `pro/infra/cicd-engineer/`
