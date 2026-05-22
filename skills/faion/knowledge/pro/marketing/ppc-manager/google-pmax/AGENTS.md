---
slug: google-pmax
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Performance Max uses Google AI to automatically optimize across all Google inventory (Search, Display, YouTube, Gmail, Discover, Maps).
content_id: "b63f32c1a2baa030"
tags: [google-ads, pmax, ai-optimization, asset-groups, performance-max]
---
# Google Performance Max (PMax)

## Summary

**One-sentence:** Performance Max uses Google AI to automatically optimize across all Google inventory (Search, Display, YouTube, Gmail, Discover, Maps).

**One-paragraph:** Performance Max uses Google AI to automatically optimize across all Google inventory (Search, Display, YouTube, Gmail, Discover, Maps). Requires conversion tracking, diverse asset groups, and optional audience signals. The AI learns from conversion data and automatically allocates spend to best-performing placements.

## Applies If (ALL must hold)

- Advertising across Google's full network (Search, Display, YouTube, Discover) with one unified budget and objective.
- Campaigns with sufficient conversion volume (30+ monthly conversions recommended for learning) to let the algorithm optimize.
- Brands or products with high-quality creative assets (images, videos) to provide asset diversity for testing.
- Goals centered on conversions or conversion value rather than impressions or clicks.
- Teams lacking time for granular keyword and placement management who benefit from automation.

## Skip If (ANY kills it)

- Campaigns with low conversion volume (under 10/month)—the algorithm needs data to learn; manual optimization is more effective.
- Search-only campaigns—Search campaigns with keywords and match types offer more control and often better ROI.
- Brand protection critical—PMax may show ads on placements or audiences you'd normally exclude; conversion data is the only feedback mechanism.
- Limited creative assets—the algorithm needs diverse images, videos, and copy variations to test; single static ad performs poorly.
- New accounts under 30 days history—algorithmic variance dominates treatment effect; wait for conversion history first.

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
