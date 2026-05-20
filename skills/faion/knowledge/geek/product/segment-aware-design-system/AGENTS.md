---
slug: segment-aware-design-system
tier: geek
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Tier-aware experiences: same design system expressing different states (locked, preview, full) across free/paid or B2C/B2B segments.
content_id: "3a3fd3d5f01e9af5"
tags: [segment-aware-design-system, product, geek]
---

# Segment-Aware Design System

## Summary

**One-sentence:** Tier-aware experiences: same design system expressing different states (locked, preview, full) across free/paid or B2C/B2B segments.

**One-paragraph:** When a product has free/paid tiers or B2C/B2B segments, the same design system must express different states (locked, preview, full). No corpus methodology covers designing for tier-aware experiences. Output: state taxonomy + token extensions + upgrade-path UX.

## Applies If (ALL must hold)

- product has ≥2 user segments (free/paid, B2C/B2B, basic/pro)
- design system in place with token foundation
- PM + designer want consistent expression across segments

## Skip If (ANY kills it)

- single-segment product
- team has no design-system foundation (build first)
- segments are sufficiently different to warrant separate apps

## Prerequisites

- segment definitions + traffic distribution
- current design system tokens + component library
- product-tier capability matrix

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent skill — provides operating context for this methodology |
| `pro/product/design-ops-foundations` | peer methodology — produces inputs or consumes outputs |
| `pro/product/segment-aware-design-system` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/product/product-manager/`
- peer methodology: `pro/product/design-ops-foundations`
- peer methodology: `pro/product/segment-aware-design-system`
- peer methodology: `geek/ai/ai-product-marketing-patterns`
- external: https://www.smashingmagazine.com/2021/09/empty-states-design/; https://baymard.com/learn/empty-state-design
