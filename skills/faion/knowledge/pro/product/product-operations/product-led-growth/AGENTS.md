---
slug: product-led-growth
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: PLG uses the product itself as the primary acquisition, activation, and expansion engine: self-serve onboarding, a clearly defined "aha moment" under 5 minutes, usage-gated upgrade triggers, and PQL scoring that hands off to sales-assist at the right moment.
content_id: "26749fdc15d89d48"
tags: [plg, growth, activation, freemium, saas]
---
# Product-Led Growth (PLG)

## Summary

**One-sentence:** PLG uses the product itself as the primary acquisition, activation, and expansion engine: self-serve onboarding, a clearly defined "aha moment" under 5 minutes, usage-gated upgrade triggers, and PQL scoring that hands off to sales-assist at the right moment.

**One-paragraph:** PLG uses the product itself as the primary acquisition, activation, and expansion engine: self-serve onboarding, a clearly defined "aha moment" under 5 minutes, usage-gated upgrade triggers, and PQL scoring that hands off to sales-assist at the right moment. The agent workflow instruments the funnel, generates activation hypotheses, ships the smallest in-product change behind a feature flag, and gates experimentation behind SRM check and pre-registered MDE.

## Applies If (ALL must hold)

- SaaS / dev tools / API products where users can self-onboard without sales (Linear, Vercel, PostHog pattern).
- ACV under ~$25k where sales-led economics break down; freemium → paid conversion is the growth lever.
- Product produces measurable in-app events (signup, activation step, feature use) that can drive PQL scoring.
- Bottom-up motion targeting individual contributors who later expand to teams (Slack, Notion, Figma pattern).
- Existing product with traffic but flat activation — room for funnel instrumentation and onboarding redesign.

## Skip If (ANY kills it)

- Highly regulated, procurement-heavy enterprise sales (defense, banking core) — buyer is not the user.
- Products requiring data integration, on-prem deploy, or contracts before any value can be shown.
- ACV above ~$100k where one closed deal pays for many SDRs; sales-led ROI dominates.
- Pre-PMF: PLG amplifies a working loop; on a broken product it industrialises churn.
- Network products without single-player value — optimising activation has no payoff if the user lands alone.

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

- parent skill: `pro/product/product-operations/`
