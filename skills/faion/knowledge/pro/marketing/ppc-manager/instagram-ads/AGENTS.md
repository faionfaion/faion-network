---
slug: instagram-ads
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Instagram ads via Meta API: Feed, Stories, Reels, Explore placements with per-placement creative specs, ad set targeting, shopping creatives, and placement breakdowns for budget allocation.
content_id: "f3af05f507db6a0e"
tags: [instagram-ads, meta-marketing-api, placement-specs, creative-optimization, reels-ads]
---
# Instagram Ads: Placement Specs, API Configuration, and Performance Reporting

## Summary

**One-sentence:** Instagram ads via Meta API: Feed, Stories, Reels, Explore placements with per-placement creative specs, ad set targeting, shopping creatives, and placement breakdowns for budget allocation.

**One-paragraph:** Instagram ads via Meta API: Feed, Stories, Reels, Explore placements with per-placement creative specs, ad set targeting, shopping creatives, and placement breakdowns for budget allocation.

## Applies If (ALL must hold)

- Creating or auditing Instagram ad sets via the Meta Marketing API
- Uploading creative assets and need spec validation before submission
- Running Instagram-only vs. cross-platform (Facebook + Instagram) campaigns
- Setting up Instagram Shopping or Collection ads with product catalogs
- Reporting on placement-level performance with `publisher_platform` + `platform_position` breakdown

## Skip If (ANY kills it)

- Facebook-only campaigns — use `ads-meta-campaign-setup` for full campaign structure
- Audience construction — use `meta-audience-targeting` for custom/lookalike audience setup
- Cross-platform budget allocation decisions — use `ads-budget-optimization`
- Creative strategy ideation (not API configuration) — this covers specs and API calls, not copywriting

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
