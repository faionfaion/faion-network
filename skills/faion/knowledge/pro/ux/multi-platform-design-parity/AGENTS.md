---
slug: multi-platform-design-parity
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Web, mobile-web, native iOS/Android, desktop, TV, wearable — token mapping, gesture vs pointer, density tiers across platforms unified.
content_id: "e9c8c5790b9a4f5e"
tags: [multi-platform-design-parity, ux, pro]
---

# Multi-Platform Design Parity

## Summary

**One-sentence:** Web, mobile-web, native iOS/Android, desktop, TV, wearable — token mapping, gesture vs pointer, density tiers across platforms unified.

**One-paragraph:** faion has mobile-ux + VUI + spatial as silos; no methodology that unifies cross-platform parity. Output: token map + interaction-model matrix + density tier rules.

## Applies If (ALL must hold)

- product targets ≥2 platforms (e.g., web + mobile)
- design system exists OR being established
- user expectation of feature parity across platforms

## Skip If (ANY kills it)

- single-platform product
- platforms with deliberately different value props (e.g., 'mobile is just login')
- team has dedicated per-platform design leads with established protocols

## Prerequisites

- design tokens for the primary platform
- list of target platforms + tiers (production vs companion)
- user research on cross-platform usage patterns

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ux/ux-ui-designer` | parent skill — provides operating context for this methodology |
| `pro/ux/ux-ui-designer` | peer methodology — produces inputs or consumes outputs |
| `pro/product/design-ops-foundations` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/ux/ux-ui-designer/`
- peer methodology: `pro/ux/ux-ui-designer`
- peer methodology: `pro/product/design-ops-foundations`
- peer methodology: `solo/ux/ui-designer`
- external: https://m3.material.io/foundations/adaptive-design; https://developer.apple.com/design/human-interface-guidelines/
