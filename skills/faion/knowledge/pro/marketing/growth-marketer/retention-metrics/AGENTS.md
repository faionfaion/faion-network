---
slug: retention-metrics
tier: pro
group: marketing
domain: growth-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Retention metrics quantify how many users return over time.
content_id: "aa6164f6dc00f2fd"
tags: [retention, metrics, cohort, churn, engagement]
---
# Retention Metrics

## Summary

**One-sentence:** Retention metrics quantify how many users return over time.

**One-paragraph:** Retention metrics quantify how many users return over time. Core set: D1/D7/D30 cohort retention rates, DAU/MAU engagement ratio, monthly churn rate, and a churn-risk score per user. Every metric requires a locked SQL definition — "DAU" computed differently across reports produces uncomparable numbers.

## Applies If (ALL must hold)

- Standing up retention reporting for the first time — generate D1/D7/D30 cohort tables.
- Weekly digest automation: WoW deltas, at-risk cohort flags, DAU/MAU trend.
- Benchmarking against industry norms (B2B SaaS, social, mobile, ecom) to set realistic targets.
- Building a churn-risk model: feature engineering per user from event data.
- Pre-A/B-test power planning — knowing baseline cohort variance is required to size experiments.

## Skip If (ANY kills it)

- One-off transactional products (single-purchase utility, gift) — retention is the wrong primitive; use LTV + repeat-purchase.
- Pre-PMF: cohorts smaller than 100 users produce noise, not signal.
- B2B products with monthly or quarterly usage — D1/D7 retention misleads; use feature-event retention or contract-tied metrics.
- Heavily seasonal products where cohort comparison across periods is invalid without de-seasonalizing.

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

- parent skill: `pro/marketing/growth-marketer/`
