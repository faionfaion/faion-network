---
slug: continuous-discovery
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Teresa Torres' framework for embedding product discovery into the weekly delivery rhythm: daily signal collection (analytics, tickets), weekly customer interviews (2-3), weekly competitor monitoring, weekly assumption testing, bi-weekly OST synthesis, monthly research review.
content_id: "09d2bd7b60d51b4e"
tags: [continuous-discovery, product-discovery, teresa-torres, opportunity-solution-tree, agents]
---
# Continuous Discovery (Teresa Torres)

## Summary

**One-sentence:** Teresa Torres' framework for embedding product discovery into the weekly delivery rhythm: daily signal collection (analytics, tickets), weekly customer interviews (2-3), weekly competitor monitoring, weekly assumption testing, bi-weekly OST synthesis, monthly research review.

**One-paragraph:** Teresa Torres' framework for embedding product discovery into the weekly delivery rhythm: daily signal collection (analytics, tickets), weekly customer interviews (2-3), weekly competitor monitoring, weekly assumption testing, bi-weekly OST synthesis, monthly research review. Implemented as a cron-driven multi-agent pipeline that writes to .aidocs/product_docs/discovery/.

## Applies If (ALL must hold)

- Live products with active users where signal volume exceeds what a human PM can review unaided.
- Product Trio (PM + designer + engineer) workflows needing a weekly cadence of customer touchpoints.
- Markets with 6-month half-life on user-need validity.
- Solopreneur stacks where one operator must simulate trio coverage via subagents.
- After a launch when growth slows and the "solution that worked 6 months ago no longer works" pattern must be detected.

## Skip If (ANY kills it)

- Pre-PMF zero-to-one with no users yet—start with customer-development or jobs-to-be-done.
- Compliance-bound enterprise sales where contract cycles are 6-18 months.
- Hardware/regulated medical where each iteration ships in months.
- Crisis mode (active outage, churn cliff)—switch to root-cause work first.
- When stakeholders demand "validated" answers from a single interview—Torres explicitly rejects validation theater.

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
