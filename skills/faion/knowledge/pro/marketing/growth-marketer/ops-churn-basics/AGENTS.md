---
slug: ops-churn-basics
tier: pro
group: marketing
domain: growth-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Churn measurement is the prerequisite for retention intervention.
content_id: "3a420558d0a72c4b"
tags: [churn, retention, saas-metrics, measurement, health-score]
---
# Churn Basics

## Summary

**One-sentence:** Churn measurement is the prerequisite for retention intervention.

**One-paragraph:** Churn measurement is the prerequisite for retention intervention. Three metrics reported together: customer churn rate, MRR churn rate, Net Revenue Retention (NRR). Voluntary and involuntary churn tracked separately. Health score provides leading indicators before cancel.

## Applies If (ALL must hold)

- Subscription/usage-based business needing a baseline churn rate before prevention work.
- Quarterly review or board prep requiring customer churn, MRR churn, NRR, and segment breakdowns.
- Diagnosing whether retention pain is acquisition-mix, new-cohort onboarding, or aging-cohort decay.
- Precursor to ops-churn-prevention and cohort-basics.

## Skip If (ANY kills it)

- One-off transactional businesses without subscriptions — measure repeat-purchase rate instead.
- Free B2C with no revenue — focus on retention curves directly.
- Pre-revenue products — churn is meaningless until cohort sizes stabilize.
- Annual-only contracts with fewer than 2 renewal cycles — sample too small for a stable rate.

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
