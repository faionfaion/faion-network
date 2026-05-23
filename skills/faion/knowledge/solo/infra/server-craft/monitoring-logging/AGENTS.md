---
slug: monitoring-logging
tier: solo
group: infra
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Monitoring + logging for solo VPS without Prometheus/Grafana: journald with log rotation, health-check scripts, Telegram digest, single-line summaries per service per day, alert-only on failure."
content_id: "6194411184922df4"
complexity: medium
produces: report
est_tokens: 6000
tags: [monitoring, logging, journald, health-check, alerting]
---
# Lightweight Monitoring + Logging

## Summary

**One-sentence:** Monitoring + logging for solo VPS without Prometheus/Grafana: journald with log rotation, health-check scripts, Telegram digest, single-line summaries per service per day, alert-only on failure.

**One-paragraph:** Prometheus + Grafana is overkill for 1-5 services; the operator-attention cost exceeds the value. This methodology produces a minimal stack: journald with rotation + per-service health-check + daily TG digest + alert-on-failure. The output is a verified config that emits one Telegram message per day with one line per service + one alert per incident.

## Applies If (ALL must hold)

- VPS with 1-10 services where Prometheus would be overkill.
- Operator wants a once-a-day digest, not a dashboard.
- Telegram bot configured for alerts.

## Skip If (ANY kills it)

- More than ~10 services or multiple hosts — graduate to Prometheus.
- Compliance requires structured metrics ingestion (Datadog, Splunk).
- Operator needs second-level granularity — journald digest is daily.

**Ефективно для:**

- Solo VPS-фаундери що не хочуть Grafana-stack.
- FLOW-style: hourly silent health + daily digest у TG.
- Indie hackers що читають один TG-feed замість трьох дашбордів.
- Compliance-light: 30-day log retention з journald rotation.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft/cron-automation` | Digest runs from cron. |
| `solo/infra/server-craft/health-checks-autoheal` | Health-check feeds the alert path. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology | 900 |
| `content/05-examples.xml` | essential | Worked example from input to verified artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from inventory. |
| `populate-evidence` | sonnet | Per-row evidence link + verification. |
| `outcome-synthesis` | opus | Cross-step synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Monitoring audit listing journald + digest + alert routing. |
| `templates/_smoke-test.md` | Minimum viable filled-in monitoring audit. |
| `templates/digest.sh` | Daily digest builder: one line per service, sent to TG at 07:00. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-monitoring-logging.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[cron-automation]]
- [[health-checks-autoheal]]
- [[secrets-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
