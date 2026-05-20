---
slug: sunset-failed-product-playbook
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Refund policy, customer migration, domain reuse, asset salvage, public retro — how to shut down a failing product gracefully.
content_id: "4f405bf79398cc7b"
tags: [sunset-failed-product-playbook, product, solo]
---

# Sunset Failed Product Playbook

## Summary

**One-sentence:** Refund policy, customer migration, domain reuse, asset salvage, public retro — how to shut down a failing product gracefully.

**One-paragraph:** faion has launch methodologies but zero coverage of how to shut down a failing product gracefully. Indie hackers fail 4 out of 5 products; this is core lifecycle. Output: shutdown plan + refund + migration + retro.

## Applies If (ALL must hold)

- product with ≥1 paying customer being shut down
- founder accepts decision (not impulsive)
- 30-60 day shutdown window feasible

## Skip If (ANY kills it)

- free-only product (no refund obligation)
- regulated product with mandatory continuity (regulators run shutdown)
- acquisition / acqui-hire — different exit path

## Prerequisites

- list of paying customers with subscription state
- data export capability OR migration partner
- refund processor (Stripe etc.)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning` | parent skill — provides operating context for this methodology |
| `solo/product/audience-driven-pivot-decision` | peer methodology — produces inputs or consumes outputs |
| `solo/marketing/content-marketer` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `solo/product/product-planning/`
- peer methodology: `solo/product/audience-driven-pivot-decision`
- peer methodology: `solo/marketing/content-marketer`
- peer methodology: `solo/product/product-launch`
- external: https://www.indiehackers.com/post/how-i-killed-my-product-gracefully; https://blog.gitlab.com/2020/09/22/lessons-from-shutting-down-a-product/
