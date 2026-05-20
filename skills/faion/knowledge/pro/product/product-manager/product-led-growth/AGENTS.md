---
slug: product-led-growth
tier: pro
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: PLG is a metric-driven loop, not a feature shipping cadence.
content_id: "26749fdc15d89d48"
tags: [product-led-growth, plg, activation, retention, pql, self-serve]
---
# Product-Led Growth (PM Angle)

## Summary

**One-sentence:** PLG is a metric-driven loop, not a feature shipping cadence.

**One-paragraph:** PLG is a metric-driven loop, not a feature shipping cadence. The PM owns the activation metric definition, the PQL-to-sales hand-off contract, and the weekly metric-review loop with growth. Drive it with three subagent passes per week: analytics pass (activation/retention/expansion cohorts), discovery pass (activation drop-off synthesis), and SDD planning pass (friction → task).

## Applies If (ALL must hold)

- New SaaS / API / dev-tool product where the buyer is also the user (founder, dev, designer, marketer).
- Existing sales-led product losing on CAC payback (greater than 18 months) — convert top-of-funnel to self-serve while keeping enterprise sales-assist.
- Bottom-up wedge into an enterprise account: individual signs up free, expansion to team/org is the business model.
- Product has a measurable "aha moment" reachable in less than 10 minutes (signup → first value-creating action).
- API / developer product where the integration itself is the activation event (first successful call).
- Pricing-page experimentation: PM owns activation funnel and runs PQL → SQL conversion tests with sales.

## Skip If (ANY kills it)

- True top-down enterprise sales (procurement, RFPs, security review take 6+ months) — PLG instrumentation is fine, but PLG-as-strategy will starve.
- Highly regulated B2B (healthcare, banking) where self-serve onboarding is legally blocked.
- One-time-purchase / transactional products (no retention curve to optimize).
- Marketplaces with cold-start liquidity problems — fix supply/demand before PLG funnels.
- Products that genuinely need a human implementation (data migration, custom modeling) — fake-PLG forces ops to do invisible setup.

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
