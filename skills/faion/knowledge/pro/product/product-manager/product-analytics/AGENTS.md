---
slug: product-analytics
tier: pro
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Product analytics is measuring and analyzing user behavior to make better product decisions.
content_id: "9f27252d25e50bd4"
tags: [product-analytics, tracking-plan, metrics, funnels, cohorts, aarrr, agent-integration]
---
# Product Analytics

## Summary

**One-sentence:** Product analytics is measuring and analyzing user behavior to make better product decisions.

**One-paragraph:** Product analytics is measuring and analyzing user behavior to make better product decisions. The key discipline: define which decisions each event will inform before implementing tracking. Freeze the event taxonomy in git (tracking-plan.md as source of truth); runtime catalogs drift toward it via PR, never the other way. Structure analytics as a four-stage agent pipeline: plan → implement → monitor → analyze.

## Applies If (ALL must hold)

- Pre-launch: agent drafts the tracking plan from a feature spec, so day-1 events ship with the code (not tacked on three sprints later).
- Activation diagnosis: drop in funnel data + cohort table, ask the agent to pinpoint the highest-leakage step and propose two experiments.
- Weekly product-health digest: scheduled agent reads BI source (BigQuery / Snowflake / Postgres replica), writes a markdown summary with anomalies highlighted.
- Post-experiment readout: agent merges A/B exposure logs with metric tables, writes the analysis report, flags Simpson's-paradox segments.
- Tracking-plan audit before a vendor migration (e.g., GA4 → PostHog) — agent diffs the live event catalog against the documented plan.
- Inbound product question from a stakeholder ("did churn move after price change?") — agent runs a parameterized SQL or Mixpanel JQL and returns chart + caveats.

## Skip If (ANY kills it)

- Pre-PMF (less than 100 weekly active users) — sample sizes are too small for funnel/cohort math; talk to users instead, no analytics framework will save you.
- Causal claims with only observational data — agent will happily call a correlation a cause; if you need causality, gate behind a proper experiment design or quasi-experimental method (DiD, synthetic control), not a dashboard.
- Exec one-pagers where the audience needs judgment, not numbers — let the agent prep the data, but a human writes the recommendation.
- High-cardinality PII queries — agents pulling raw user-level data without aggregation/scrubbing is a privacy incident waiting to happen.
- Replacing a tracking plan review with a one-shot LLM call — naming, taxonomy, and ownership decisions outlive any single feature; commit them via PR, not chat.

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

- parent skill: `pro/product/product-manager/`
