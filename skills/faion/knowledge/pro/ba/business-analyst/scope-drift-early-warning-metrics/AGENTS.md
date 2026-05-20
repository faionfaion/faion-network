---
slug: scope-drift-early-warning-metrics
tier: pro
group: business-analyst
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "be8ce41f31483985"
summary: Five quantitative early-warning metrics — CR-volume velocity, AC-rewrite rate, story-split count, requirement-churn ratio, parking-lot age — with thresholds, dashboards, and trigger actions that catch scope drift weeks before a re-baseline becomes unavoidable.
tags: [scope-drift, ba-metrics, traceability, change-request, dashboards]
---

# Scope Drift Early-Warning Metrics

## Summary

**One-sentence:** Five quantitative metrics — CR-volume velocity, AC-rewrite rate, story-split count, requirement-churn ratio, parking-lot age — with thresholds and trigger actions that catch scope drift early, weeks before re-baseline becomes unavoidable.

**One-paragraph:** Requirements traceability is necessary but reactive — it tells you what changed, after the fact. Early-warning needs leading indicators. This methodology pins five metrics computable from existing artefacts (Jira/Linear/Azure-DevOps + the parking-lot from `scope-creep-parking-lot-protocol`): (1) Change-Request volume velocity (CRs/week trend), (2) Acceptance-Criteria rewrite rate (AC edited after sprint start), (3) Story-split count (stories split mid-sprint), (4) Requirement-churn ratio (requirements added + deleted ÷ total), (5) Parking-lot age (median age of open parking-lot items). Each has a green/amber/red threshold, a daily/weekly dashboard, and a named trigger action (e.g. amber → escalate to PM via `risk-threshold-policy`; red → mandatory re-baseline discussion). Mechanism: nightly batch compute → dashboard → email digest → triage action. Primary output: a `scope-drift-dashboard.md` (or Grafana / Looker board) refreshed daily, plus per-metric trigger logs.

## Applies If (ALL must hold)

- engagement uses a structured ticket system with versioned tickets (Jira, Linear, ADO)
- signed scope baseline exists and is referenceable
- engagement length ≥6 weeks (shorter ones don't accumulate enough signal)
- ≥1 BA + 1 PM in role
- traceability methodology already in use (`pro/ba/business-analyst/requirements-traceability-full-lifecycle` or equivalent)

## Skip If (ANY kills it)

- engagement &lt;6 weeks — drift accumulates faster than dashboards refresh
- tickets are kept outside the system (spreadsheets, email) — instrument first, measure after
- ticket history is not preserved (system without audit log) — fix the tooling first
- engagement is explicitly T&M open-scope — drift is the business model, metrics don't apply

## Prerequisites

- ticket-system API access with history endpoints
- baseline mapping: each ticket linked to a baseline requirement ID
- definition of "Change Request" status in the ticket system
- parking-lot dataset (CSV / API) for the parking-lot-age metric

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/requirements-traceability-full-lifecycle` | Provides the requirement → ticket mapping these metrics aggregate over |
| `pro/ba/business-analyst/scope-creep-parking-lot-protocol` | Parking-lot age feeds metric #5 |
| `pro/pm/project-manager/scope-change-vs-scope-creep-detection` | Classifier verdicts feed metric #1 (CR-volume) |
| `pro/pm/project-manager/risk-threshold-policy` | Red triggers route through the policy |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: five-metric coverage, thresholds in baseline-relative terms, daily refresh, trigger actions, dashboard owner | ~1100 |
| `content/02-output-contract.xml` | essential | Dashboard schema, metric definitions, trigger-log schema | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: vanity metrics, threshold staleness, dashboard alone, trigger ignored, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `nightly_metric_compute` | n/a | Deterministic |
| `daily_dashboard_summary` | sonnet | Translate metrics into PM-readable language |
| `red_trigger_action_draft` | sonnet | Draft the escalation message per the risk policy |
| `weekly_trend_commentary` | opus | Cross-metric trend analysis with framing |

## Templates

| File | Purpose |
|------|---------|
| `templates/scope-drift-dashboard.md` | Daily dashboard layout |
| `templates/metric-definitions.md` | Precise definitions and formulas |
| `templates/trigger-log.schema.yaml` | Schema for the trigger event log |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/compute-drift-metrics.py` | Nightly: pull tickets + parking lot, compute five metrics, persist | Cron 02:00 daily |
| `scripts/check-thresholds.py` | Compare metrics to thresholds, emit trigger events | Immediately after compute |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer methodologies: `requirements-traceability-full-lifecycle`, `scope-creep-parking-lot-protocol`, `scope-change-vs-scope-creep-detection`, `major-change-impact-assessment`
- external: [PMBOK 7 — performance domains](https://www.pmi.org/pmbok-guide-standards) · [Atlassian Jira Software analytics](https://www.atlassian.com/) · [BABOK v3 — RPM](https://www.iiba.org/standards-and-resources/babok/)
