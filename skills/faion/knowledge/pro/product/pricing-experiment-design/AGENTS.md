---
slug: pricing-experiment-design
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Live pricing experiments (van Westendorp on production traffic, grandfathering policy, cohort-segmented A/B legality, price-sensitivity flags).
content_id: "cca765b9150568f0"
tags: [pricing-experiment-design, product, pro]
---

# Pricing Experiment Design

## Summary

**One-sentence:** Live pricing experiments (van Westendorp on production traffic, grandfathering policy, cohort-segmented A/B legality, price-sensitivity flags).

**One-paragraph:** Pricing-research exists at market-researcher level but nothing covers LIVE pricing experiments on production traffic. PMs at P6 with pricing power need this. Output: experiment design + grandfathering + legal-and-ethical guardrails.

## Applies If (ALL must hold)

- SaaS / subscription product with pricing-power
- ≥1k active customers OR ≥10k monthly visitors
- PM has authority to run pricing tests

## Skip If (ANY kills it)

- B2B sales-led where pricing is per-deal — not A/B-able
- regulated pricing (utilities, healthcare) — defer to compliance
- team has no analytics infrastructure (prerequisite)

## Prerequisites

- current pricing tiers + conversion baseline
- experimentation infrastructure
- legal review of A/B price discrimination in target jurisdictions

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent skill — provides operating context for this methodology |
| `pro/product/product-manager` | peer methodology — produces inputs or consumes outputs |
| `pro/research/pricing-research` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `pro/product/product-manager`
- peer methodology: `pro/research/pricing-research`
- peer methodology: `pro/marketing/conversion-optimizer`
- external: https://www.priceintelligently.com/blog/saas-pricing-experiments; https://www.lennyrachitsky.com/p/pricing-experiments
