---
slug: discovery-cadence-design
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Designs the interview slot, OST refresh cycle, and assumption-test pipeline for a specific team — the act continuous-discovery-habits assumes already happened.
content_id: "80bfd94991972e95"
tags: [discovery-cadence-design, product, pro]
---

# Discovery Cadence Design

## Summary

**One-sentence:** Designs the interview slot, OST refresh cycle, and assumption-test pipeline for a specific team — the act continuous-discovery-habits assumes already happened.

**One-paragraph:** Continuous-discovery-habits assumes the cadence exists. Nothing covers the act of designing the cadence for a specific team (interview slots, OST refresh cycle, assumption-test pipeline). PMs joining new teams hit this immediately. Output: cadence plan + interview slot policy + OST cycle + assumption-test queue.

## Applies If (ALL must hold)

- PM joining new team OR existing team without discovery cadence
- team has ≥1 PM with discovery authority
- ≥1 active product surface with paying users

## Skip If (ANY kills it)

- team already has stable Teresa-Torres-style cadence (interview/week + OST) — augment, don't re-design
- team in shutdown phase — discovery not the priority
- purely B2C consumer impulse product — qualitative discovery has limited fit

## Prerequisites

- current team size + roles
- current customer-research capacity
- current OST or assumption inventory (or willingness to start one)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent skill — provides operating context for this methodology |
| `pro/product/continuous-discovery-habits` | peer methodology — produces inputs or consumes outputs |
| `solo/research/user-interviews` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `pro/product/continuous-discovery-habits`
- peer methodology: `solo/research/user-interviews`
- external: https://www.producttalk.org/ (Teresa Torres); https://www.producttalk.org/2021/08/continuous-discovery-habits/
