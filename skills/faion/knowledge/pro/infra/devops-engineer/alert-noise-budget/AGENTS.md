---
slug: alert-noise-budget
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Per-service alert noise budget (max pages per shift, max non-actionable alerts per week) with enforcement workflow that retires or tunes any alert that exceeds it.
content_id: "48a31784fb88cd16"
tags: [infra, devops, alerting, sre, noise-budget, oncall, sentry, datadog, grafana]
---

# Alert Noise Budget

## Summary

**One-sentence:** A per-service noise budget (e.g., max 2 pages per on-call shift, max 5 non-actionable alerts per week) and an enforcement workflow that mutes / tunes / retires any alert that pushes the service over budget.

**One-paragraph:** Solves the firefighting spiral: alerting works in theory (alerts exist), but in practice on-call is flooded with non-actionable noise until pages get ignored or filtered to `/dev/null`. Mechanism: define a noise budget per service (page-rate + non-actionable-rate), instrument each alert with `actionable` outcome at acknowledgment time, weekly review consumes the metric and triggers tuning actions (raise threshold, add hysteresis, add suppression window, delete alert) when a service exceeds budget. Primary output: a noise-budget dashboard + a list of alerts requiring tuning this week.

## Applies If (ALL must hold)

- service has at least one alerting platform configured (Sentry, Datadog, Grafana, PagerDuty, OpsGenie)
- on-call rotation exists OR a solo founder gets paged
- alerts have produced >= 10 events over the past 4 weeks (enough data to budget against)
- team can mark alerts actionable / non-actionable at ack time

## Skip If (ANY kills it)

- pre-launch service with no users — no real alerting yet; establish alerts first
- monitoring is "logs only, no alerts" — budget is moot until alerts exist
- on-call practice does not exist (no one carries the pager) — fix that first
- team unwilling to retire alerts — budget will be permanently exceeded and ignored

## Prerequisites

- alerting platform with event history (4+ weeks)
- alert acknowledgment workflow that captures: who acked, when, was it actionable
- per-service ownership defined (each alert maps to a service with an owner)
- weekly review meeting (30 min) OR async review channel where tuning decisions are made

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/incident-response-rotation` | Defines on-call structure; budget is per-shift, so rotation cadence matters |
| `pro/infra/devops-engineer/sli-slo-definition` | Alerts should fire on SLO burn; consume the SLO definition to scope alerts |
| `pro/infra/devops-engineer/api-monitoring-alerting` | Existing methodology; budget runs on TOP of that — does not replace |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: per-service-budget, actionable-flag-at-ack, weekly-review-triggers-tuning, deletion-default-action, executive-escalation-on-chronic-breach | ~1000 |
| `content/02-output-contract.xml` | essential | Budget report schema + tuning action contract + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (filter-everything, false-actionable, missing-suppression, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `alert_event_ingestion` | haiku | Pull events from platform API, normalize schema |
| `actionable_classification_review` | sonnet | Sanity-check responder's actionable flag against incident notes |
| `tuning_action_proposal` | sonnet | For over-budget alerts, propose threshold change / hysteresis / suppression |
| `chronic_breach_synthesis` | opus | Cross-service synthesis when budget breach is systemic |

## Templates

| File | Purpose |
|------|---------|
| `templates/noise-budget.json` | Per-service budget config (page_max_per_shift, non_actionable_max_per_week) |
| `templates/alert-ack-record.json` | Per-event ack record (actionable yes/no, why) |
| `templates/tuning-action-record.md` | Tuning decision log (alert id, action, expected impact, follow-up date) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/compute-budget-status.py` | Computes events vs budget per service, returns over/under/at-budget | Weekly review prep |
| `scripts/audit-actionable-flags.py` | Spot-checks actionable flags vs incident notes for honesty | Monthly |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodologies: `incident-response-rotation`, `sli-slo-definition`, `runbook-link-from-alert`
- external: [Google SRE Book chapter 6: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) · [Honeycomb on alert fatigue](https://www.honeycomb.io/blog/alert-fatigue) · [Rob Ewaschuk — My Philosophy on Alerting](https://docs.google.com/document/d/199PqyG3UsyXlwieHaqbGiWVa8eMWi8zzAn0YfcApr8Q/preview)
