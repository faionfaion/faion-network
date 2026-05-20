---
slug: viral-metrics
tier: pro
group: marketing
domain: growth-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The viral coefficient K = i * c, where i is average invites sent per user and c is the conversion rate of those invites.
content_id: "58c9e3b42face8fd"
tags: [viral, k-factor, referrals, growth, sharing]
---
# Viral Metrics and K-factor

## Summary

**One-sentence:** The viral coefficient K = i * c, where i is average invites sent per user and c is the conversion rate of those invites.

**One-paragraph:** The viral coefficient K = i * c, where i is average invites sent per user and c is the conversion rate of those invites. K greater than 1 produces exponential growth; K = 0.5-1.0 amplifies other channels. Measure i, c, and viral cycle time weekly; optimize both independently.

## Applies If (ALL must hold)

- Designing or auditing a referral/sharing mechanism for an existing product.
- Building a weekly viral dashboard to track i, c, and K by loop type and channel.
- Projecting growth to determine whether viral alone can hit a user target within N cycles.
- Identifying which factor (i or c) has the most improvement headroom.

## Skip If (ANY kills it)

- Pre-retention: if D30 retention is below 20%, increasing K just cycles more users through a leaky bucket.
- B2B enterprise with 6-month sales cycles — K compounds too slowly to matter for pipeline.
- When invite event tracking is not yet in place — computing K from incomplete data is misleading.
- Regulated products where incentivized referrals trigger disclosure requirements.

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
