# Scope Drift Early-Warning Metrics

## Summary

**One-sentence:** Five quantitative metrics with thresholds and trigger actions that catch scope drift early — weeks before re-baseline becomes unavoidable.

**One-paragraph:** Traceability is reactive; early warning needs leading indicators. This methodology pins five metrics computable from existing ticket-system + parking-lot data: CR-volume velocity, AC-rewrite rate, story-split count, requirement-churn ratio, parking-lot age. Each has baseline-relative green/amber/red thresholds, daily refresh, and a named trigger action owned by a named human. Primary output: a daily-refreshed `scope-drift-dashboard.md` plus per-metric trigger logs feeding `risk-threshold-policy` on red.

**Ефективно для:**

- Engagements ≥6 weeks with signed baseline + structured tickets.
- Programs where re-baseline cost is high (regulated, fixed-bid, multi-vendor).
- Teams already practising requirements traceability + parking-lot protocol.
- PM↔BA pairs that want a shared dashboard rather than separate spreadsheets.

## Applies If (ALL must hold)

- engagement uses a structured ticket system with versioned tickets (Jira, Linear, ADO)
- signed scope baseline exists and is referenceable
- engagement length ≥6 weeks (shorter ones don't accumulate enough signal)
- ≥1 BA + 1 PM in role
- traceability methodology already in use (`requirements-traceability-full-lifecycle` or equivalent)

## Skip If (ANY kills it)

- engagement <6 weeks — drift accumulates faster than dashboards refresh
- tickets are kept outside the system (spreadsheets, email) — instrument first, measure after
- ticket history is not preserved (system without audit log) — fix the tooling first
- engagement is explicitly T&M open-scope — drift is the business model, metrics don't apply

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ticket-system API access with history endpoints | JSON over HTTPS | Jira / Linear / ADO admin |
| baseline mapping: each ticket linked to baseline requirement id | CSV / DB view | BA team |
| Change Request status definition in the ticket system | config snapshot | PM |
| parking-lot dataset | CSV / API | scope-creep-parking-lot-protocol |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[requirements-traceability-full-lifecycle]] | Provides the requirement → ticket mapping these metrics aggregate over. |
| [[scope-creep-parking-lot-protocol]] | Parking-lot age feeds metric #5. |
| [[scope-change-vs-scope-creep-detection]] | Classifier verdicts feed metric #1 (CR-volume). |
| [[risk-threshold-policy]] | Red triggers route through the policy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: five-metric coverage, baseline-relative thresholds, daily refresh, trigger actions, owner | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for dashboard + trigger-log + metric-definitions; valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: vanity metrics, threshold staleness, dashboard-alone, single-metric noise, compute lag, trigger fatigue | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree on engagement length + baseline + history availability | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `nightly_metric_compute` | n/a | Deterministic batch — no LLM call. |
| `daily_dashboard_summary` | sonnet | Translate metrics into PM-readable language. |
| `red_trigger_action_draft` | sonnet | Draft the escalation message per the risk policy. |
| `weekly_trend_commentary` | opus | Cross-metric trend analysis with framing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scope-drift-dashboard.md` | Daily dashboard layout with 5 metric blocks + trigger log table. |
| `templates/metric-definitions.md` | Precise formulas, inputs, thresholds, exceptions per metric. |
| `templates/trigger-log.schema.json` | JSON Schema for the trigger event log. |
| `templates/_smoke-test.md` | Minimum viable filled-in dashboard. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-scope-drift-early-warning-metrics.py` | Validates dashboard artefact against the JSON Schema in 02-output-contract.xml. | After dashboard refresh; pre-commit on the dashboard repo. |

## Related

- [[requirements-traceability-full-lifecycle]]
- [[scope-creep-parking-lot-protocol]]
- [[scope-change-vs-scope-creep-detection]]
- [[risk-threshold-policy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
