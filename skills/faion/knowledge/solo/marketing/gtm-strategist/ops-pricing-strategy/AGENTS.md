---
slug: ops-pricing-strategy
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A value-based framework for setting prices: calculate cost floor, estimate customer value ceiling, research willingness to pay, choose a pricing model, and test.
content_id: "44adcaea3dfce921"
tags: [pricing, pricing-strategy, value-based-pricing, monetization, saas]
---
# Pricing Strategy

## Summary

**One-sentence:** A value-based framework for setting prices: calculate cost floor, estimate customer value ceiling, research willingness to pay, choose a pricing model, and test.

**One-paragraph:** A value-based framework for setting prices: calculate cost floor, estimate customer value ceiling, research willingness to pay, choose a pricing model, and test. Price should be 10–20% of the measurable value delivered — not cost-plus or competitor-copy. Pricing determines business model, customer expectations, and growth trajectory. Cost-plus pricing systematically underprices; competitor-copying ignores value differentiation. Value-based pricing with Van Westendorp research finds the acceptable range empirically, then psychological anchoring maximizes revenue within it.

## Applies If (ALL must hold)

- New product needs initial pricing before launch; no data exists yet
- Existing pricing is below market and owner suspects leaving revenue on the table
- Adding a new tier (freemium, enterprise) and need to define feature gating
- Conversion rate is less than 1% and pricing objections are common — need diagnostic
- Quarterly pricing review cycle; need to compare conversion and churn data against benchmarks

## Skip If (ANY kills it)

- Pricing change affects existing paying customers — requires careful communication strategy beyond agent output; risk of churn spike
- Enterprise pricing involving custom contracts and negotiation — agents can set anchor points but cannot negotiate
- Regulated industries (healthcare, finance, gov) where pricing is constrained by compliance rules
- The product has less than 10 paying customers; there is not enough data for quantitative analysis — do customer interviews first
- Pre-product-market-fit stage — pricing experiments are meaningless without retention signal

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
