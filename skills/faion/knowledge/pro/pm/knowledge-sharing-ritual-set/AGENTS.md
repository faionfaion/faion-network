---
slug: knowledge-sharing-ritual-set
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Weekly tech-talk, biweekly demo, monthly architecture review, quarterly skip-level — the rituals that convert tribal knowledge to documented.
content_id: "05365493f772b568"
tags: [knowledge-sharing-ritual-set, pm, pro]
---

# Knowledge Sharing Ritual Set

## Summary

**One-sentence:** Weekly tech-talk, biweekly demo, monthly architecture review, quarterly skip-level — the rituals that convert tribal knowledge to documented.

**One-paragraph:** Tribal knowledge is the stated pain. faion has no methodology on the rituals that convert tribal → documented. Output: ritual calendar + format templates + decay metric.

## Applies If (ALL must hold)

- team ≥6 with shared codebase or product
- evidence of tribal knowledge (newcomers asking same questions repeatedly)
- manager authority to set rituals

## Skip If (ANY kills it)

- team ≤3 — over-engineered
- team is all senior with shared tenure ≥3 years — different knowledge profile
- knowledge is in regulated context requiring formal docs only

## Prerequisites

- calendar with shared time slots
- documentation home (Notion, Outline, Confluence)
- manager bandwidth for facilitation

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm-agile` | parent skill — provides operating context for this methodology |
| `geek/sdlc-ai/team-async-rituals` | peer methodology — produces inputs or consumes outputs |
| `geek/pm/engineering-ladder-and-growth-plan` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `geek/sdlc-ai/team-async-rituals`
- peer methodology: `geek/pm/engineering-ladder-and-growth-plan`
- external: https://medium.com/spotify-engineering/spotify-engineering-culture-part-1-2f2a3c10c2fc (Spotify guilds); https://shopify.engineering/learning-and-development
