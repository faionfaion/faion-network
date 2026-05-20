---
slug: slo-burn-decision-matrix
tier: pro
group: devops-engineer
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "269f2ccca90ce28c"
summary: Decision matrix mapping fast-burn vs slow-burn SLO error-budget patterns to specific operational actions (canary halt, ship freeze, focus shift, accept) so error-budget burn becomes deterministic rather than rhetorical.
tags: [slo, error-budget, burn-rate, devops-engineer, decision-matrix, canary]
---

# SLO Burn Decision Matrix

## Summary

**One-sentence:** Decision matrix that maps fast-burn vs slow-burn error-budget patterns to specific operational actions — canary halt, ship freeze, focus shift, accept — so burn-rate alerts produce deterministic decisions, not rhetoric.

**One-paragraph:** DORA / SRE methodology defines fast-burn (e.g. 14.4 hours to exhaust budget) and slow-burn (e.g. 6 hours over 30 days) as alert categories but stops short of the operational decision. Teams without the matrix end up debating "what does this mean for us" every time, producing inconsistent responses. This methodology pins a matrix: each burn category × service-class (user-facing critical, async worker, batch, internal tool) maps to a named action (halt canary, freeze ship, focus shift to reliability, accept and continue). Actions have explicit owner, SLA, and revert criteria. Mechanism: burn alert fires → matrix lookup → action triggered → audit log. Primary output: a `slo-burn-matrix.yaml` per portfolio (or per service if heterogeneous) + per-event audit log.

## Applies If (ALL must hold)

- SLOs are defined with explicit objective + window (e.g. 99.9% availability over 30 days)
- error-budget burn-rate alerting in place (Prometheus + multi-window multi-burn-rate, Datadog, Honeycomb)
- service catalog with service classes defined
- the team commits to act on burn alerts (not just observe)

## Skip If (ANY kills it)

- no SLOs defined — define them first (`pro/infra/devops-engineer/slo-definition-template-per-service-class`)
- SLOs are aspirational and never hit thresholds — fix the SLO calibration before defining matrix
- single-service shop — overhead exceeds value; use a 3-row simplified table
- team explicitly accepts SRE burn alerts as informational only — culture mismatch; matrix is futile

## Prerequisites

- SLO definitions per service
- service-class taxonomy (user-facing critical, async worker, batch, internal)
- burn-rate alert thresholds set (Google SRE multi-window multi-burn-rate or equivalent)
- on-call rotation in place

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/slo-definition-template-per-service-class` | Defines the SLOs this matrix consumes |
| `pro/infra/devops-engineer/slo-burn-rate-review-protocol` (geek peer) | Weekly review ritual that uses this matrix |
| `pro/infra/devops-engineer/canary-deploy-promote-rollback-decision` | Canary halt action references this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: explicit categories, action per cell, named owner, revert criteria, audit log | ~1000 |
| `content/02-output-contract.xml` | essential | slo-burn-matrix.yaml schema, action enum, audit-event shape | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: action paralysis, alert ignoring, accept-by-default, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `matrix_lookup` | n/a | Deterministic table lookup |
| `action_message_draft` | sonnet | Compose the action notification with context |
| `revert_criteria_check` | n/a | Deterministic when criteria are met |
| `weekly_matrix_audit` | sonnet | Summarise the past week's matrix-triggered actions for review |

## Templates

| File | Purpose |
|------|---------|
| `templates/slo-burn-matrix.schema.yaml` | Matrix schema |
| `templates/matrix-default.yaml` | Sensible defaults to fork |
| `templates/action-notification.md` | Format for the action-triggered message |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/route-burn-alert.py` | Receive Prometheus alert, look up action, post to on-call channel | Webhook from alert manager |
| `scripts/check-revert-criteria.py` | Evaluate whether an active action can be reverted | Hourly during active action |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodologies: `slo-definition-template-per-service-class`, `slo-burn-rate-review-protocol`, `canary-deploy-promote-rollback-decision`, `dora-metrics`
- external: [Google SRE Workbook — Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/) · [DORA Accelerate](https://dora.dev/) · [Honeycomb — Multi-window burn rate](https://www.honeycomb.io/)
