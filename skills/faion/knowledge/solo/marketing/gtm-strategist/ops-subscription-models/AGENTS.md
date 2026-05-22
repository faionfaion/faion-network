---
slug: ops-subscription-models
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A framework for designing and operating subscription businesses: choose model type (SaaS, membership, replenishment, curation), structure tiers with strategic feature allocation, instrument MRR/churn/LTV metrics, automate billing recovery (dunning), and manage the full customer lifecycle from trial through win-back.
content_id: "e53d828d4b044352"
tags: [subscription, billing, mrr, churn, ltv]
---
# Subscription Models

## Summary

**One-sentence:** A framework for designing and operating subscription businesses: choose model type (SaaS, membership, replenishment, curation), structure tiers with strategic feature allocation, instrument MRR/churn/LTV metrics, automate billing recovery (dunning), and manage the full customer lifecycle from trial through win-back.

**One-paragraph:** A framework for designing and operating subscription businesses: choose model type (SaaS, membership, replenishment, curation), structure tiers with strategic feature allocation, instrument MRR/churn/LTV metrics, automate billing recovery (dunning), and manage the full customer lifecycle from trial through win-back. Net Revenue Retention above 100% is the goal — meaning expansion revenue offsets churn.

## Applies If (ALL must hold)

- Launching a SaaS, digital membership, or content platform.
- Converting an existing one-time-purchase product to recurring revenue.
- Churn rate is above 5%/month and root cause is unclear.
- Expansion revenue (upgrades) is zero — missing upsell/tier paths.
- Setting up billing infrastructure for the first time (Stripe, Paddle).

## Skip If (ANY kills it)

- One-time high-value services (consulting, agency work) where recurring isn't the model.
- Products with naturally episodic demand (event software, seasonal tools).
- When product has not yet demonstrated retention past 90 days — subscription without retention is an expensive churn machine.
- Physical product subscriptions without reliable supply chain — replenishment model requires fulfillment reliability.

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

- parent skill: `solo/marketing/gtm-strategist/`
