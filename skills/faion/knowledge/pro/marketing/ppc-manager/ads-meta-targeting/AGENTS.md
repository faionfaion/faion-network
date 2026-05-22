---
slug: ads-meta-targeting
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Three-tier audience strategy for Meta Ads: Core (interest/demographic/behavior) for cold traffic, Custom (pixel + email + engagement) for warm traffic, and Lookalike (1%, 2-3%, 5-10% of a quality source) for scaling.
content_id: "2c3a5dda065951f9"
tags: [meta-ads, targeting, audiences, lookalike, custom-audiences]
---
# Meta Targeting & Audiences

## Summary

**One-sentence:** Three-tier audience strategy for Meta Ads: Core (interest/demographic/behavior) for cold traffic, Custom (pixel + email + engagement) for warm traffic, and Lookalike (1%, 2-3%, 5-10% of a quality source) for scaling.

**One-paragraph:** Three-tier audience strategy for Meta Ads: Core (interest/demographic/behavior) for cold traffic, Custom (pixel + email + engagement) for warm traffic, and Lookalike (1%, 2-3%, 5-10% of a quality source) for scaling. Build exclusion audiences (purchasers, subscribers) before launching any campaign. Use Advantage+ only for large budgets with broad-appeal products; manual targeting for niche or small budgets.

## Applies If (ALL must hold)

- Setting up audiences before launching any Meta campaign.
- Scaling a campaign by expanding from Core/Interest to Lookalike.
- Building retargeting audiences by pixel behavior (pricing page, cart, checkout).
- Testing which audience type produces the lowest CPA (Core vs LAL vs retarget).

## Skip If (ANY kills it)

- Audience size below 500K for Core/Interest — ad delivery is constrained and CPM spikes.
- Lookalike with a source smaller than 1,000 people — match quality is poor; build up the source first.
- Advantage+ when the product is niche or the budget is small — Meta's AI needs scale to work.
- When pixel is not installed and verified — Custom and Lookalike audiences won't populate correctly.

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
