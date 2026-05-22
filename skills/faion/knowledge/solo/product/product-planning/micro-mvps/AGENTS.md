---
slug: micro-mvps
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Micro-MVPs are extremely small, high-signal experiments designed to validate one key assumption in hours to days rather than weeks.
content_id: "fafd75a87ee3804d"
tags: [mvp, validation, experiments, lean, rapid-testing]
---
# Micro-MVPs

## Summary

**One-sentence:** Micro-MVPs are extremely small, high-signal experiments designed to validate one key assumption in hours to days rather than weeks.

**One-paragraph:** Micro-MVPs are extremely small, high-signal experiments designed to validate one key assumption in hours to days rather than weeks. Six experiment types (landing page, concierge, Wizard of Oz, video demo, fake door, smoke test) map to specific assumption categories. The pattern forces assumption identification, success-metric definition, and a pivot/persevere decision before starting, not after.

## Applies If (ALL must hold)

- New product idea where demand, willingness-to-pay, or workflow fit is unvalidated.
- Feature hypothesis that can be faked before building (Wizard of Oz, fake door).
- Budget or time is too constrained for a full MVP build.
- Iterating rapidly post-MVP to validate the next bet without a full sprint.

## Skip If (ANY kills it)

- Assumption already validated by strong existing evidence — skip to build.
- Regulated domains where a "fake" product violates compliance (fintech, medical).
- Infrastructure/platform work with no user-facing surface to fake.
- When the experiment would damage brand trust with early adopters.

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

- parent skill: `solo/product/product-planning/`
