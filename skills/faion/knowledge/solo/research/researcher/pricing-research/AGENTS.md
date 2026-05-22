---
slug: pricing-research
tier: solo
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for determining optimal pricing by combining value-capture math, competitor analysis, Van Westendorp willingness-to-pay research, and tier design.
content_id: "f2319f9798e9e54e"
tags: [pricing, pricing-strategy, value-based-pricing, market-research, customer-research]
---
# Pricing Research

## Summary

**One-sentence:** A methodology for determining optimal pricing by combining value-capture math, competitor analysis, Van Westendorp willingness-to-pay research, and tier design.

**One-paragraph:** A methodology for determining optimal pricing by combining value-capture math, competitor analysis, Van Westendorp willingness-to-pay research, and tier design. The rule: anchor on value delivered first (target 10-20% capture rate), map the competitive field, validate with customer research (N≥30 for statistical significance), then design 2-3 tiers with a clear anchor, main revenue tier, and entry option.

## Applies If (ALL must hold)

- Pre-launch: setting initial price for a SaaS, course, template pack, or service.
- Re-pricing: revenue-per-customer is below 10% of value delivered.
- Designing a new tier (Pro / Enterprise) on top of an existing plan.
- Choosing between subscription, usage-based, one-time, or hybrid models.

## Skip If (ANY kills it)

- Fewer than 10 paying customers — insufficient signal; use competitor anchor + intuition and iterate.
- Highly bespoke enterprise sales where price is negotiated per deal.
- Marketplace or two-sided platforms where take-rate dynamics dominate.
- Regulated pricing (healthcare, energy, telecom) where compliance frameworks apply instead.

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

- parent skill: `solo/research/researcher/`
