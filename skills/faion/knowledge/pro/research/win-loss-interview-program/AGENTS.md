---
slug: win-loss-interview-program
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Sample frame, deal-stage selection, script bias, sales handoff — the specific structure of win/loss interviews user-interviews and problem-validation don't cover.
content_id: "048cd72a34428ec1"
tags: [win-loss-interview-program, research, pro]
---

# Win-Loss Interview Program

## Summary

**One-sentence:** Sample frame, deal-stage selection, script bias, sales handoff — the specific structure of win/loss interviews user-interviews and problem-validation don't cover.

**One-paragraph:** Researcher skill covers user-interviews + problem-validation but not the specific structure of win/loss interviews. P6 PMs lose deals to invisible reasons without this. Output: program design + script + sample frame + insight pipeline.

## Applies If (ALL must hold)

- sales-led B2B with ≥10 deals/quarter
- named PM/researcher with authority to interview
- sales team can hand off won/lost contacts

## Skip If (ANY kills it)

- PLG self-serve (use churn-cohort-analysis)
- <5 deals/quarter — sample too small
- sales team unwilling to hand off (organizational gap)

## Prerequisites

- list of last 90 days won + lost deals
- interview scheduling + recording infrastructure
- synthesis cadence + consumer (roadmap, marketing, sales)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/researcher` | parent skill — provides operating context for this methodology |
| `pro/research/researcher` | peer methodology — produces inputs or consumes outputs |
| `pro/research/user-interviews` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/research/researcher/`
- peer methodology: `pro/research/researcher`
- peer methodology: `pro/research/user-interviews`
- peer methodology: `pro/product/win-loss-quarterly-pm-template`
- external: https://www.lennyrachitsky.com/p/win-loss-analysis; https://primaryintelligence.com/research/why-win-loss-analysis
