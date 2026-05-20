---
slug: facebook-ads
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Meta Marketing API v20+ campaign hierarchy: objectives, CBO, bid strategies, creative upload flow, status lifecycle, and budget in cents not dollars.
content_id: "89ab54159e7a72c3"
tags: [facebook-ads, meta-ads, api-integration, campaign-management, creative-upload]
---
# Facebook Ads API

## Summary

**One-sentence:** Meta Marketing API v20+ campaign hierarchy: objectives, CBO, bid strategies, creative upload flow, status lifecycle, and budget in cents not dollars.

**One-paragraph:** Meta Marketing API v20+ campaign hierarchy: objectives, CBO, bid strategies, creative upload flow, status lifecycle, and budget in cents not dollars.

## Applies If (ALL must hold)

- Creating or managing Facebook/Instagram ad campaigns via the Meta Marketing API
- Implementing CBO (Campaign Budget Optimization) or ad set-level budgets
- Building image, video, or dynamic creative programmatically
- Setting up retargeting funnels with audience-based targeting

## Skip If (ANY kills it)

- Instagram-specific placement optimization — refer to instagram-ads methodology
- Audience research and lookalike creation — use meta-audience-targeting methodology
- Attribution modeling — use ads-attribution-models methodology
- Active learning phase (first 50 conversions per ad set) — automated bid/budget tweaks reset learning and burn money
- Tiny budgets under $30/day per ad set — Meta has minimum-spend signal floors and API adds operational risk
- Special Ad Categories (housing, employment, credit, social issues) without explicit category flag
- One-off creative judgement calls (which hero image wins) — humans still beat agents on visual taste

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
