---
slug: ads-meta-campaign-setup
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: End-to-end checklist for launching a Facebook/Instagram campaign via Meta Ads Manager: install and verify the Meta Pixel, choose the correct campaign objective, configure the three-tier structure (Campaign → Ad Set → Ad), set targeting and placements, upload at least 3 creative variations per ad set, and avoid editing during the learning phase.
content_id: "75f6fe27fa9f4a71"
tags: [meta, facebook, instagram, campaign-setup, pixel]
---
# Meta Campaign Setup

## Summary

**One-sentence:** End-to-end checklist for launching a Facebook/Instagram campaign via Meta Ads Manager: install and verify the Meta Pixel, choose the correct campaign objective, configure the three-tier structure (Campaign → Ad Set → Ad), set targeting and placements, upload at least 3 creative variations per ad set, and avoid editing during the learning phase.

**One-paragraph:** End-to-end checklist for launching a Facebook/Instagram campaign via Meta Ads Manager: install and verify the Meta Pixel, choose the correct campaign objective, configure the three-tier structure (Campaign → Ad Set → Ad), set targeting and placements, upload at least 3 creative variations per ad set, and avoid editing during the learning phase. The core rule is: select the objective that matches the actual business action — choosing Traffic when the goal is leads optimizes for clicks, not conversions, and wastes budget.

## Applies If (ALL must hold)

- Launching a new Meta campaign from scratch
- Auditing an existing campaign's structure for mis-aligned objectives or missing Pixel setup
- Setting up the naming conventions and UTM parameters for a new product line
- Configuring CBO vs. ad-set budget for a new test
- Onboarding a new account that has never run Meta ads

## Skip If (ANY kills it)

- Audience construction (custom, lookalike, interest targeting) — use meta-audience-targeting
- Creative copy and image/video spec decisions for Instagram placements — use instagram-ads
- Budget reallocation across live campaigns — use ads-budget-optimization
- Reporting and analysis of a running campaign — use the Meta reporting methodology

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
