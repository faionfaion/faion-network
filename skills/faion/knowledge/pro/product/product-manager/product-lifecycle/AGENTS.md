---
slug: product-lifecycle
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A four-stage framework (Introduction → Growth → Maturity → Decline) for diagnosing which lifecycle stage a product is in and applying the matching investment strategy.
content_id: "98dbff05c4bede18"
tags: [product-lifecycle, portfolio-management, stage-strategy, investment-allocation]
---
# Product Lifecycle Management

## Summary

**One-sentence:** A four-stage framework (Introduction → Growth → Maturity → Decline) for diagnosing which lifecycle stage a product is in and applying the matching investment strategy.

**One-paragraph:** A four-stage framework (Introduction → Growth → Maturity → Decline) for diagnosing which lifecycle stage a product is in and applying the matching investment strategy. Each stage has distinct focus areas, key metrics, and transition triggers. The process runs in four steps: assess stage from metrics, validate with multi-quarter trends, apply stage-appropriate strategy, and plan the next-stage transition.

## Applies If (ALL must hold)

- Quarterly portfolio review — decide investment level for each shipped product and stop applying growth budget to maturity or decline assets.
- A product hits a metrics inflection (growth slows from 30% to 8%, churn jumps) — need a structured stage reassessment, not a gut call.
- Pre-roadmap step: tag every product with its stage before sequencing the year.
- End-of-life decision: product declining for 3+ quarters, need a sunset plan with migration timeline.
- Investor or board update: defending why a Maturity product gets retention budget instead of new features.
- Stage transition checkpoint: Introduction product hits PMF and must shift from "learn fast" to "scale" tooling.

## Skip If (ANY kills it)

- Pre-PMF startup with one product still hunting for fit — there is no lifecycle yet, only a discovery loop.
- Sub-feature decisions inside one product (which feature to build next) — RICE / MoSCoW are sharper at that grain.
- Pure B2B services / agency revenue with no productized asset — lifecycle math is undefined.
- Internal tools / platforms with no external customers — they have a usefulness curve, not a revenue curve.
- Crisis weeks (P0 outage, security incident) — survival first, restore lifecycle planning after.

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

- parent skill: `pro/product/product-manager/`
