---
slug: ads-budget-optimization
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Allocate budgets using efficiency ratios and the 70-20-10 rule.
content_id: "b3da78d84b112130"
tags: [budget, optimization, allocation, efficiency, ppc]
---
# Budget Optimization

## Summary

**One-sentence:** Allocate budgets using efficiency ratios and the 70-20-10 rule.

**One-paragraph:** Allocate budgets using efficiency ratios and the 70-20-10 rule. Scale campaigns beating target, optimize underperformers, and maintain test reserves. Avoid premature cuts and single-step budget doubling.

## Applies If (ALL must hold)

- Multi-campaign or multi-channel programs needing a reallocation framework
- Setting up automated budget rules in platform interfaces or custom dashboards
- Weekly or monthly budget review meetings requiring a decision matrix
- Scaling campaigns from test phase to production with controlled increments
- Running quarterly variance and incrementality analyses across channels

## Skip If (ANY kills it)

- Single-campaign programs — reallocate within the campaign via bid adjustments, not budget cuts
- Pre-learning-phase campaigns with fewer than 50 conversions — data is too sparse to make decisions
- Tactical daily bid optimization — budget allocation is a weekly/monthly cadence, not a hourly signal
- Exploring new channels for the first time — test with fixed budgets, not proportional allocation

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

- parent skill: `pro/marketing/ppc-manager/`
