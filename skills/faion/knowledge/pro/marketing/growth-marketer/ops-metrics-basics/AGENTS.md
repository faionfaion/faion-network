---
slug: ops-metrics-basics
tier: pro
group: marketing
domain: growth-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A practical metrics management system for solopreneurs and small teams: choose 5-10 actionable metrics, implement collection from existing data sources, set targets and alerts, and establish a review cadence (daily pulse, weekly review, monthly deep-dive).
content_id: "366339592d76f091"
tags: [metrics, operations, saas, analytics, reporting]
---
# Ops Metrics Basics

## Summary

**One-sentence:** A practical metrics management system for solopreneurs and small teams: choose 5-10 actionable metrics, implement collection from existing data sources, set targets and alerts, and establish a review cadence (daily pulse, weekly review, monthly deep-dive).

**One-paragraph:** A practical metrics management system for solopreneurs and small teams: choose 5-10 actionable metrics, implement collection from existing data sources, set targets and alerts, and establish a review cadence (daily pulse, weekly review, monthly deep-dive). Includes all core SaaS metric formulas (MRR, ARR, churn, LTV, CAC, ARPU, net retention).

## Applies If (ALL must hold)

- Early-stage product that has some paying users but no formal metrics system.
- Solo operator who needs to answer "how is business?" with real numbers on demand.
- Team misaligned on what constitutes good/bad performance for the current phase.
- Setting up Stripe → Sheets → Looker Studio pipeline for the first time.

## Skip If (ANY kills it)

- Pre-revenue product — no payment data means the core metrics are undefined.
- Enterprises with dedicated BI teams — this pattern targets lean operations, not warehouse-scale analytics.
- When you want deep behavioral analytics — use product analytics tools (Mixpanel, Amplitude) instead of this ops-level framework.

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
