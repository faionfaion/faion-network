---
slug: xp-extreme-programming
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: An agile methodology built on 12 engineering practices taken to their logical extreme: TDD (test everything), continuous integration (integrate many times daily), pair programming (review all code), simple design (fewest elements that pass), and collective ownership (anyone changes anything).
content_id: "09561b55db549aca"
tags: [xp, tdd, agile, continuous-integration, quality]
---
# Extreme Programming (XP)

## Summary

**One-sentence:** An agile methodology built on 12 engineering practices taken to their logical extreme: TDD (test everything), continuous integration (integrate many times daily), pair programming (review all code), simple design (fewest elements that pass), and collective ownership (anyone changes anything).

**One-paragraph:** An agile methodology built on 12 engineering practices taken to their logical extreme: TDD (test everything), continuous integration (integrate many times daily), pair programming (review all code), simple design (fewest elements that pass), and collective ownership (anyone changes anything). For solo + AI dev, Claude acts as the pair partner and TDD is non-negotiable.

## Applies If (ALL must hold)

- Small teams (2-12) with rapidly changing requirements and direct customer access.
- Greenfield projects where TDD, CI, and pair programming can be established from day one.
- Recovering a brownfield codebase where quality has rotted — XP's practices are a culture reset.
- Solo + AI dev: most XP practices map cleanly onto a human-in-loop with Claude as the pair.
- Teams adopting agile but failing on engineering excellence (Scrum-without-XP).

## Skip If (ANY kills it)

- Compliance-heavy / regulated work where every change needs upfront sign-off — "embrace change" clashes.
- Distributed teams with poor async culture and no shared timezone — pair programming falls apart.
- Outsourced arrangements where the customer is unreachable.
- Hardware / firmware where test-refactor cycle is dominated by hardware-in-loop.
- Research / exploratory ML where most code is thrown away — TDD overhead exceeds value.

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

- parent skill: `solo/dev/software-developer/`
