---
slug: business-model-research
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Systematic analysis of how a business will create, deliver, and capture value, structured as a Business Model Canvas (9 blocks) plus P10/P50/P90 unit economics (CAC, LTV, LTV:CAC, payback period) and 5 stress tests.
content_id: "243577a9242ec7d2"
tags: [business-model, unit-economics, ltv, cac, pricing]
---
# Business Model Research

## Summary

**One-sentence:** Systematic analysis of how a business will create, deliver, and capture value, structured as a Business Model Canvas (9 blocks) plus P10/P50/P90 unit economics (CAC, LTV, LTV:CAC, payback period) and 5 stress tests.

**One-paragraph:** Systematic analysis of how a business will create, deliver, and capture value, structured as a Business Model Canvas (9 blocks) plus P10/P50/P90 unit economics (CAC, LTV, LTV:CAC, payback period) and 5 stress tests. Every assumption is tagged Hard (sourced) or Soft (founder estimate); LTV must never use a lifetime of more than 60 months.

## Applies If (ALL must hold)

- Pre-spec phase: founder has a product idea but no defended monetization story.
- Pricing decision under uncertainty: ARPU/margin/churn assumptions must be modeled before a price page ships.
- Pivot review: existing product is missing LTV:CAC >= 3:1 and the model itself may be broken.
- Investor memo/seed deck requiring "How we make money" section with stress tests.
- Multi-revenue-stream design: subscription + usage + marketplace fee blends.

## Skip If (ANY kills it)

- Internal tools, OSS side-projects, hobby apps with no intent to monetize.
- Already-shipping products with 12+ months of real ARR data — use aarrr-pirate-metrics instead.
- Pure infrastructure libraries where revenue is a downstream consequence.
- Government/grant-funded work where the "customer" is a budget line.
- Two-sided marketplace pre-launch with zero supply — do network-effects first.
- Hardware/regulated products where margin is dictated by BOM + compliance, not chosen.

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

- parent skill: `pro/research/researcher/`
