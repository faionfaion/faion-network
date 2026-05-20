---
slug: plg-optimization-tactics
tier: pro
group: marketing
domain: conversion-optimizer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A tactics catalog for improving activation, free-tier-to-paid, and expansion conversion in an existing PLG product.
content_id: "a46cc6a8f8fda365"
tags: [plg, activation, conversion, upgrade-prompts, ice-scoring]
---
# PLG Optimization Tactics

## Summary

**One-sentence:** A tactics catalog for improving activation, free-tier-to-paid, and expansion conversion in an existing PLG product.

**One-paragraph:** A tactics catalog for improving activation, free-tier-to-paid, and expansion conversion in an existing PLG product. Core rules: pair every tactic with the metric it moves and a current baseline; show upgrade prompts at 80% of limit (not 100%); cap prompts to one per session and zero during the first session; name a comparable customer and quantify value in all upgrade copy; reject "Upgrade Now" and "Premium Plan" as CTA text.

## Applies If (ALL must hold)

- Running an existing PLG product where activation, free-tier-to-paid, or expansion conversion has plateaued and you need a backlog of tested tactics rather than a strategy rewrite.
- Designing a free tier or self-serve checkout from scratch and want a pre-curated list of friction points to instrument before launch.
- Generating in-product upgrade copy, feature-gate messaging, and pricing-page variants that follow the methodology good vs bad patterns.
- Producing a quarterly A/B test backlog scored against the included onboarding/upgrade/pricing test idea bank.

## Skip If (ANY kills it)

- Pre-PMF teams without measurable activation data — generic tactics distract from PMF discovery.
- Pure sales-led ACVs above ~$50K where self-serve patterns do not survive procurement; route to sales-led playbooks instead.
- Single-event transactions (one-shot ecommerce, ticketing) where there is no expansion or seat-growth surface to optimize.
- Hard-regulated products (healthcare, banking) where "instant access, no approval" recommendations conflict with compliance.

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

- parent skill: `pro/marketing/conversion-optimizer/`
