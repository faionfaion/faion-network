---
slug: engineering-ladder-and-growth-plan
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ladder definitions (L1-L5 with example artifacts), growth-plan template, promo packet template — without it juniors leave.
content_id: "222719ae393984d0"
tags: [engineering-ladder-and-growth-plan, pm, geek]
---

# Engineering Ladder and Growth Plan

## Summary

**One-sentence:** Ladder definitions (L1-L5 with example artifacts), growth-plan template, promo packet template — without it juniors leave.

**One-paragraph:** How does a Junior become a Senior at THIS company? Every successful product team has a ladder; faion has zero coverage. Output: ladder document + growth-plan template + promo-packet template.

## Applies If (ALL must hold)

- engineering team size ≥5
- team has ≥1 junior or mid-level engineer with growth ambition
- manager/CTO has authority to define levels + run promotions

## Skip If (ANY kills it)

- team <5 — ladder over-engineers a small team; use 1:1 growth docs instead
- agency / contract team — ladder less applicable
- team unable to commit to evaluation cadence

## Prerequisites

- team org chart with current titles
- list of recent hires + recent departures with reasons
- manager bandwidth for quarterly growth conversations

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm-agile` | parent skill — provides operating context for this methodology |
| `geek/sdlc-ai/methodology-contribution-flow` | peer methodology — produces inputs or consumes outputs |
| `pro/pm/team-management` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/pm/pm-agile/`
- peer methodology: `geek/sdlc-ai/methodology-contribution-flow`
- peer methodology: `pro/pm/team-management`
- external: https://www.engineeringladders.com/; https://progression.fyi/; https://medium.com/@kentbeck_7670/software-design-x-rays-and-progression-frameworks
