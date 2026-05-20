---
slug: ads-retargeting
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Full-funnel retargeting strategy: segment past visitors by intent (all visitors → blog readers → product viewers → pricing viewers → cart abandoners), tailor ad messaging to each segment's stage, apply frequency caps to prevent fatigue, and always exclude recent converters from acquisition campaigns.
content_id: "e4e64d144e990c36"
tags: [retargeting, remarketing, funnel, audiences, conversion-optimization]
---
# Retargeting

## Summary

**One-sentence:** Full-funnel retargeting strategy: segment past visitors by intent (all visitors → blog readers → product viewers → pricing viewers → cart abandoners), tailor ad messaging to each segment's stage, apply frequency caps to prevent fatigue, and always exclude recent converters from acquisition campaigns.

**One-paragraph:** Full-funnel retargeting strategy: segment past visitors by intent (all visitors → blog readers → product viewers → pricing viewers → cart abandoners), tailor ad messaging to each segment's stage, apply frequency caps to prevent fatigue, and always exclude recent converters from acquisition campaigns. Retargeting should be 20-30% of total ad spend and delivers 40-70% lower CPA versus cold prospecting.

## Applies If (ALL must hold)

- Any campaign where a pixel is installed and website audience segments are large enough (1,000+).
- After launching prospecting campaigns to recover non-converters.
- Building sequential ad sequences (reminder → benefits → social proof → urgency).
- Upselling or cross-selling to past purchasers.

## Skip If (ANY kills it)

- Before the pixel is installed and events are verified — audiences won't populate.
- Audience size under 1,000 — Meta/Google will throttle delivery; build up traffic first.
- When ad fatigue is already high (frequency >5 and CTR declining) — pause and refresh creative.
- For purely brand-awareness campaigns with no conversion goal — retargeting requires a defined conversion event.

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
