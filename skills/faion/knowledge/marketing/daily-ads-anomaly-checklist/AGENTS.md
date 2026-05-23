# Daily Ads Anomaly Checklist

## Summary

**One-sentence:** 15-minute daily paid-ads triage — 6 anomaly checks (spend spike, CPA spike, frequency, CTR, conversion drop, account-health) with thresholds + escalation gates.

**One-paragraph:** ppc-manager has plenty of setup content but no daily 15-minute triage routine; this is where money is actively lost. The checklist defines six anomaly checks with explicit thresholds, an escalation gate per check, and an output artefact (a daily run log) that downstream owners can review without re-running the queries. Core rules: every check has a numeric threshold; every triggered anomaly produces a named owner action; pauses are reversible by default (≤24h) unless cost continues climbing; the log carries account-id + time-window + threshold values so the same anomaly cannot be silently re-classified next day.

**Ефективно для:**

- Solo / small-team paid ads — 1 person 15 хвилин на день.
- Multi-account agency — repeatable triage across 10+ ad accounts.
- After-hours / weekend cover — junior owner runs the checklist + escalates.
- Post-launch monitoring перших 14 днів кампанії.

## Applies If (ALL must hold)

- ≥1 active paid-ads channel with daily spend ≥ $50.
- Owner has API or dashboard access to spend + CPA + frequency + CTR per ad set.
- Pause/budget-change permissions are scoped to the owner.
- A daily 15-minute slot is dedicated (or scheduled cron).

## Skip If (ANY kills it)

- Weekly review cadence is sufficient (low-spend account, no time-sensitive offer).
- No write access to pause / shift budget — the checklist becomes a powerless audit log.
- Brand-awareness campaign without direct-response metrics — different signal set.
- Account is in initial-learning phase (<7 days) where noise dominates signal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Spend + CPA + CTR per ad set (yesterday vs 7-day avg) | dashboard / API | ad platform |
| Frequency + creative fatigue indicator | dashboard | ad platform |
| Conversion tracking validation status | health check | analytics infra |
| Pause / budget-change permissions | account role | ad platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cross-channel-cpa-rollup]] | Weekly rollup defines baseline CPA the checklist compares against. |
| [[paid-ads-creative-library]] | Creative fatigue context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: numeric-threshold-per-check, named-owner-action, reversible-pause-default, log-with-context, escalation-gate-on-repeat | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for one daily-run log + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-check procedure with thresholds + actions | 700 |
| `content/06-decision-tree.xml` | essential | Tree: anomaly signal → action (pause / reduce / escalate / no-op) | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pull-yesterday-metrics` | haiku | Mechanical API call. |
| `apply-thresholds` | haiku | Numeric comparison. |
| `decide-action` | sonnet | Bounded judgment on pause/reduce/escalate. |
| `write-log-entry` | haiku | Template fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/daily-run-log.json` | JSON example matching the output contract. |
| `templates/checklist.md` | Human-friendly 6-check Markdown to print or pin. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-daily-ads-anomaly-checklist.py` | Validate the daily-run log JSON against the schema | Daily after run; pre-publish. |

## Related

- [[cross-channel-cpa-rollup]]
- [[paid-ads-creative-library]]
- [[deliverability-incident-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps the observed anomaly (which threshold tripped) to the action (pause vs reduce vs escalate vs no-op) and pins the rule from `01-core-rules.xml`. Use it during the daily run — bypassing the tree leads to over-pausing or missed anomalies.
