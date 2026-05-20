---
slug: ops-customer-success-metrics
tier: pro
group: marketing
domain: gtm-strategist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Effective CS operations require a health score system that combines usage frequency, feature adoption, support sentiment, engagement level, and payment status.
content_id: "138d07c54acadea8"
tags: [customer-success, metrics, health-score, retention, nrr]
---
# Customer Success Metrics and Health Scoring

## Summary

**One-sentence:** Effective CS operations require a health score system that combines usage frequency, feature adoption, support sentiment, engagement level, and payment status.

**One-paragraph:** Effective CS operations require a health score system that combines usage frequency, feature adoption, support sentiment, engagement level, and payment status. Monitor health distribution across account cohorts, track cohort retention curves, measure NPS/CSAT survey responses, and set up leading indicator alerts for usage drops and support escalations. Track expansion revenue from CS-driven upsells and Net Revenue Retention.

## Applies If (ALL must hold)

- SaaS / subscription products with more than 10 paying customers and monthly billing cycles.
- Establishing a CS function or migrating from reactive support to proactive retention.
- Diagnosing why retention dropped without understanding which accounts are at risk.
- Measuring CS team impact: expansion revenue, accounts saved from churn, NRR improvement.
- Building a customer health dashboard as the single source of truth for CS priorities.

## Skip If (ANY kills it)

- Single-purchase products with no recurring revenue — metrics apply to contracts/support satisfaction instead.
- Fewer than 10 paying customers — cohort curves are statistically unreliable; use qualitative feedback instead.
- Fully self-serve products with no human interaction — usage metrics alone suffice; add NPS only if you have onboarding touch points.
- Pre-PMF products where most customers churn regardless of effort — measure product-market fit first, then add CS.

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

- parent skill: `pro/marketing/gtm-strategist/`
