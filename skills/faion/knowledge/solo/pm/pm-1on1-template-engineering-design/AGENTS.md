---
slug: pm-1on1-template-engineering-design
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Opinionated agenda template for weekly PM ↔ EM, design lead, support lead 1:1s — tuned for product-org reality.
content_id: "98a14d47b21c71c2"
tags: [pm-1on1-template-engineering-design, pm, solo]
---

# PM 1:1 Template for Engineering and Design

## Summary

**One-sentence:** Opinionated agenda template for weekly PM ↔ EM, design lead, support lead 1:1s — tuned for product-org reality.

**One-paragraph:** PMs run weekly 1:1s with EM, design lead, support lead. No opinionated agenda template tuned for product-org reality. Output: 1:1 agenda template per partner + action-item flow.

## Applies If (ALL must hold)

- PM in product org with ≥1 EM partner + ≥1 design partner
- weekly 1:1 cadence
- PM has authority to set agenda

## Skip If (ANY kills it)

- solo PM (no partners to 1:1 with)
- partner relationship in conflict — needs mediation, not template
- company already has standardized 1:1 template

## Prerequisites

- list of standing partners (EM, design lead, support lead, data, marketing)
- shared docs space for 1:1 notes
- action-item tracker (project tool)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent skill — provides operating context for this methodology |
| `pro/pm/pm-agile` | peer methodology — produces inputs or consumes outputs |
| `pro/product/product-manager` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/pm/project-manager/`
- peer methodology: `pro/pm/pm-agile`
- peer methodology: `pro/product/product-manager`
- peer methodology: `pro/product/discovery-cadence-design`
- external: https://www.lennyrachitsky.com/p/the-art-of-the-1-on-1; https://www.svpg.com/articles/silicon-valley-product-group-articles/
