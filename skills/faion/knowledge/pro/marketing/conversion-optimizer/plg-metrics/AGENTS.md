---
slug: plg-metrics
tier: pro
group: marketing
domain: conversion-optimizer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A metrics methodology for Product-Led Growth: the full funnel from acquisition through expansion, including activation rate, time-to-value (TTV), free-to-paid conversion, Product-Qualified Lead (PQL) scoring, net revenue retention (NRR), and cohort analysis.
content_id: "f641c8b6fd29e42b"
tags: [plg, metrics, activation, conversion, analytics]
---
# PLG Metrics and Tracking

## Summary

**One-sentence:** A metrics methodology for Product-Led Growth: the full funnel from acquisition through expansion, including activation rate, time-to-value (TTV), free-to-paid conversion, Product-Qualified Lead (PQL) scoring, net revenue retention (NRR), and cohort analysis.

**One-paragraph:** A metrics methodology for Product-Led Growth: the full funnel from acquisition through expansion, including activation rate, time-to-value (TTV), free-to-paid conversion, Product-Qualified Lead (PQL) scoring, net revenue retention (NRR), and cohort analysis. Every metric must have a single owner, a machine-verifiable definition tied to a single event in a single table, and a "who acts and how" runbook line attached to each dashboard tile.

## Applies If (ALL must hold)

- Standing up a PLG dashboard with activation, conversion, expansion, and retention metrics in one place
- Defining or refining the activation event ("aha moment") and time-to-value for a SaaS product
- Designing a PQL scoring model from product behavior signals
- Running cohort analysis for retention and free-to-paid conversion
- Quarterly PLG strategy review where freemium vs. trial model and gating thresholds are on the table

## Skip If (ANY kills it)

- Sales-led motions where the buyer never logs in before purchase — PLG metrics produce noise
- Pre-product-market-fit startups: vanity metrics dominate, PQL scoring overfits to a tiny sample
- Self-hosted or single-tenant deployments where event telemetry is not centralized
- Hardware or one-time-purchase products without recurring usage signals
- Regulated industries where logging granular user behavior requires consent gates that break funnel completeness

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
