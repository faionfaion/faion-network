---
slug: churn-cohort-analysis
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Cohort isolation by activation status, leading-indicator detection, save-flow design — the dedicated playbook product-analytics generalities don't provide.
content_id: "af76e1d50ab55723"
tags: [churn-cohort-analysis, product, pro]
---

# Churn Cohort Analysis

## Summary

**One-sentence:** Cohort isolation by activation status, leading-indicator detection, save-flow design — the dedicated playbook product-analytics generalities don't provide.

**One-paragraph:** Product-analytics covers cohorts generically; no dedicated playbook for churn cohort isolation by activation, leading indicators, save-flow. Output: churn cohort table + leading-indicator alerts + save-flow design with ≥1 control group.

## Applies If (ALL must hold)

- SaaS or subscription product with ≥6 months of paid data
- ≥100 paying customers OR ≥10 paying enterprise accounts
- PM/data has access to activation event tracking (not just MRR)

## Skip If (ANY kills it)

- annual contracts only — different churn cadence; use ARR-renewal patterns
- freemium with no paid layer — there is no churn, only inactivity
- <6 months of data — too noisy for cohort analysis

## Prerequisites

- subscription state table (signup, activate, paid, churn dates)
- activation event definition (concrete behavioral milestone)
- ability to A/B test save-flows or hold out a control

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent skill — provides operating context for this methodology |
| `pro/product/product-analytics` | peer methodology — produces inputs or consumes outputs |
| `pro/product/customer-success-basics` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/product/product-manager/`
- peer methodology: `pro/product/product-analytics`
- peer methodology: `pro/product/customer-success-basics`
- external: https://www.lennyrachitsky.com/p/churn-benchmarks (Lenny benchmarks); https://www.profitwell.com/recur/all/churn
