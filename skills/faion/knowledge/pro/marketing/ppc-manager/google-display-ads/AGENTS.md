---
slug: google-display-ads
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Python patterns for creating DISPLAY_NETWORK campaigns, adding contextual (keyword/placement) and audience targeting to ad groups, building responsive display ads with required asset sets (1-5 headlines, long headline, 1-5 descriptions, 1-15 images), and querying placement-level performance reports.
content_id: "9d55132b6d2430ab"
tags: [google-ads, display, campaigns, responsive-ads, api]
---
# Google Display Ads — Campaign Setup, Targeting, Responsive Ads

## Summary

**One-sentence:** Python patterns for creating DISPLAY_NETWORK campaigns, adding contextual (keyword/placement) and audience targeting to ad groups, building responsive display ads with required asset sets (1-5 headlines, long headline, 1-5 descriptions, 1-15 images), and querying placement-level performance reports.

**One-paragraph:** Python patterns for creating DISPLAY_NETWORK campaigns, adding contextual (keyword/placement) and audience targeting to ad groups, building responsive display ads with required asset sets (1-5 headlines, long headline, 1-5 descriptions, 1-15 images), and querying placement-level performance reports.

## Applies If (ALL must hold)

- Creating banner ad campaigns across Google Display Network (GDN)
- Adding remarketing audiences or contextual keyword targeting to display ad groups
- Uploading image assets and assembling responsive display ads (RDA)
- Reporting on which placements are driving impressions and conversions
- Migrating legacy image ads to RDAs (Google sunsets uploaded display ads in favour of RDA)

## Skip If (ANY kills it)

- Search text ads — use google-search-ads methodology instead
- Performance Max campaigns — use google-pmax methodology instead
- Shopping product listing ads — use google-shopping-ads methodology instead
- YouTube-only video campaigns — use google-video-ads methodology instead

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
