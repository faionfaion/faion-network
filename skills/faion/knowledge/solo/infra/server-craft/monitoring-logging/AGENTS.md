---
slug: monitoring-logging
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Lightweight monitoring and logging for solo developer VPS platforms using journald, health-check scripts, and Telegram alerts without Prometheus/Grafana.
content_id: "6194411184922df4"
tags: [monitoring, logging, journald, health-check, alerting]
---
# Monitoring and Logging

## Summary

**One-sentence:** Lightweight monitoring and logging for solo developer VPS platforms using journald, health-check scripts, and Telegram alerts without Prometheus/Grafana.

**One-paragraph:** Lightweight monitoring and logging for solo developer VPS platforms using journald, health-check scripts, and Telegram alerts without Prometheus/Grafana. Provides journalctl query patterns, log rotation config, FLOW-style autonomous hourly/daily reports, and status dashboard.

## Applies If (ALL must hold)

- Setting up observability from scratch on a solo-developer VPS
- A service went down silently and you need alerting before it happens again
- Writing a health-check script for a cron job or FLOW guardian
- Building an autonomous monitoring loop that sends Telegram alerts on anomalies
- Investigating a production incident retroactively via journalctl

## Skip If (ANY kills it)

- Multi-server environments where Prometheus/Grafana/Loki is justified (use pro/infra/devops-engineer)
- Kubernetes clusters (use Datadog, Grafana Loki, or similar)
- Compliance-heavy environments requiring tamper-proof audit-trail log storage
- High-frequency trading or sub-second SLOs where journald latency is unacceptable

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
