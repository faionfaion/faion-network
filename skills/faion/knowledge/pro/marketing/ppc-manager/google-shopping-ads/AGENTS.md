---
slug: google-shopping-ads
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Master Google Shopping campaigns via API: feed setup, Merchant Center integration, product partition strategies, campaign structure, bidding progression, and authentication across two APIs.
content_id: "9fc35e74f9da8827"
tags: [google-ads, shopping-campaigns, product-feed, merchant-center, ecommerce]
---
# Google Shopping Ads Campaign Management

## Summary

**One-sentence:** Master Google Shopping campaigns via API: feed setup, Merchant Center integration, product partition strategies, campaign structure, bidding progression, and authentication across two APIs.

**One-paragraph:** Master Google Shopping campaigns via API: feed setup, Merchant Center integration, product partition strategies, campaign structure, bidding progression, and authentication across two APIs.

## Applies If (ALL must hold)

- Setting up or scaling Google Shopping campaigns for ecommerce catalogs.
- Building agents that manage product feeds, partition trees, or bid adjustments.
- Automating feed quality audits, disapproval diagnosis, or feed upload workflows.
- Integrating Shopping performance data into multi-channel campaign dashboards.

## Skip If (ANY kills it)

- Small catalogs (under 50 SKUs) where manual Google Merchant Center management is simpler.
- Non-ecommerce businesses or services without a product feed.
- Performance Max campaigns — use google-pmax instead.

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
