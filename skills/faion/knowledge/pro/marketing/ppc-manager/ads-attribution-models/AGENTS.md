---
slug: ads-attribution-models
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Attribution models define how conversion credit is distributed across ad touchpoints in a customer journey.
content_id: "5e1f9408732a6e96"
tags: [attribution, analytics, conversion, multi-touch, ga4]
---
# Ads Attribution Models

## Summary

**One-sentence:** Attribution models define how conversion credit is distributed across ad touchpoints in a customer journey.

**One-paragraph:** Attribution models define how conversion credit is distributed across ad touchpoints in a customer journey. Each platform (Meta, Google, LinkedIn) claims its own conversions using different windows and logic, causing totals to exceed actual sales. Use GA4 as a unified source of truth and compare platform-reported, GA4-modeled, and warehouse-deduped numbers per channel. Flag variances above 15% before making budget decisions.

## Applies If (ALL must hold)

- Multi-channel paid programs (2+ platforms) where platform totals do not match the warehouse
- Setting up GA4 or BigQuery export pipelines that produce reconciled CPA and ROAS per channel
- Designing and scheduling quarterly geo-holdout (incrementality) tests
- Auto-generating weekly variance reports (platform vs. GA4 vs. warehouse) for human review
- Budget reallocation reviews requiring a defensible model

## Skip If (ANY kills it)

- Single-channel programs — use the platform default model; cross-channel attribution adds no signal
- Pre-revenue or fewer than 50 conversions/month — data is too sparse for any model to be reliable
- Optimizing inside a single platform (bids, ad copy) — use native attribution; switching models mid-flight confuses the bidding algorithm
- Tactical creative decisions — attribution informs strategy and budget, not which thumbnail to ship

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

- parent skill: `pro/marketing/ppc-manager/`
