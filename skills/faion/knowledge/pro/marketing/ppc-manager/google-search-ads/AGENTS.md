---
slug: google-search-ads
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Master Google Search campaign setup via API: network targeting, ad group creation, keyword match types, Quality Score optimization, and Search Terms Report analysis.
content_id: "b146b0f875d03354"
tags: [google-ads, search-campaigns, keywords, quality-score, bidding]
---
# Google Search Ads Campaign Management

## Summary

**One-sentence:** Master Google Search campaign setup via API: network targeting, ad group creation, keyword match types, Quality Score optimization, and Search Terms Report analysis.

**One-paragraph:** Master Google Search campaign setup via API: network targeting, ad group creation, keyword match types, Quality Score optimization, and Search Terms Report analysis.

## Applies If (ALL must hold)

- Setting up or modifying Google Search campaigns programmatically.
- Building agents that manage keyword bids, match types, or negative keyword lists.
- Automating Quality Score diagnosis and ad copy optimization.
- Integrating Search campaign data into multi-channel campaign management tools.

## Skip If (ANY kills it)

- Display Network or YouTube campaigns — different ad types and network settings apply.
- Shopping campaigns — use google-shopping-ads instead.
- Manual, one-off bid adjustments where API overhead exceeds value.

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
