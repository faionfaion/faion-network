---
slug: cronjob-overrun-monitoring
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a monitoring config (Prometheus rules + metadata) that alerts on cron overlap, skip, and duration creep across the scheduler.
content_id: "c7d6884f8c5ce892"
complexity: medium
produces: config
est_tokens: 4500
tags: [cron, monitoring, alerting, scheduled-jobs]
---
# Cronjob Overrun Monitoring

## Summary

**One-sentence:** Produces a monitoring config (Prometheus rules + metadata) that alerts on cron overlap, skip, and duration creep across the scheduler.

**One-paragraph:** Solo-tier `cron-automation` covers schedule definition but not behavioural alerts. Pro-tier teams hit overlapping runs, silent skips, and duration creep that go unnoticed until a downstream consumer is starved. This methodology pins Prometheus alert rules and cron metadata that fire on (a) two consecutive runs overlapping in time, (b) a scheduled run missing its window by > N, (c) a job whose p95 duration drifts > 50% over a rolling window.

**Ефективно для:**

- monthly cron audit — потрібен alerting на overlap / skip / duration creep.
- коли solo-tier `cron-automation` є basic, а pro-tier хоче behavioural alerts.
- DevOps з write access до scheduler (k8s CronJob, systemd timer, classic cron).
- scheduled-jobs >=10 одиниць, де ручний моніторинг більше не масштабується.

## Applies If (ALL must hold)

- Scheduler (k8s CronJob, systemd timer, classic cron) has >=10 jobs the team owns.
- Prometheus or compatible metric backend is wired into the scheduler.
- Job start / end events emit a metric or log the alerter can consume.
- A named owner is accountable for tuning alert thresholds.

## Skip If (ANY kills it)

- Scheduler has < 5 jobs — manual review still scales.
- No metric backend (pure cron + email) — alerting infrastructure missing.
- Jobs already emit duration metrics and alerts — pick up tuning where it is, do not duplicate.
- Greenfield project — wait until job catalogue stabilises.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Job catalogue | YAML / spreadsheet | platform team |
| Metric backend | Prometheus or equivalent | ops |
| Existing alert routing | AlertManager / equivalent | on-call lead |
| Named owner | string | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/prometheus-monitoring` | metric backend assumed |
| `pro/infra/devops-engineer/oncall-rotation-design` | alerts feed an existing on-call rotation |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes r1-bound-scope) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `enumerate-jobs` | haiku | Catalogue extraction from scheduler |
| `derive-thresholds` | sonnet | Compute overlap / skip / duration thresholds |
| `compose-alert-rules` | sonnet | Emit Prometheus alert rules + metadata |

## Templates

| File | Purpose |
|------|---------|
| `templates/monitoring-config.yaml` | Prometheus alert rules + cron metadata |
| `templates/skeleton.json` | JSON schema for the overrun-monitoring artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cronjob-overrun-monitoring.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[prometheus-monitoring]]
- [[oncall-rotation-design]]
- [[alert-deduplication-playbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Cronjob Overrun Monitoring methodology when in doubt about scope or fit.
