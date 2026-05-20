---
slug: mob-programming
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A team practice where all members work together on one task at one machine: a rotating Driver types only what the Navigator(s) dictate, and ideas must pass through someone else's hands before reaching the keyboard.
content_id: "aaaac3d98c397e53"
tags: [mob-programming, pair-programming, teamwork, knowledge-transfer, collaboration]
---
# Mob Programming

## Summary

**One-sentence:** A team practice where all members work together on one task at one machine: a rotating Driver types only what the Navigator(s) dictate, and ideas must pass through someone else's hands before reaching the keyboard.

**One-paragraph:** A team practice where all members work together on one task at one machine: a rotating Driver types only what the Navigator(s) dictate, and ideas must pass through someone else's hands before reaching the keyboard. Strong-style navigation, strict 5-10 minute rotation, and a written session goal are the three load-bearing constraints.

## Applies If (ALL must hold)

- High-stakes changes requiring multiple specialists simultaneously (payment flow, schema migration, security refactor).
- Onboarding: new engineer navigates while the team drives — knowledge transfers in hours.
- "Impossible" production bugs requiring frontend + backend + ops context simultaneously.
- Killing a knowledge silo when the only expert is leaving.
- Cross-team API contract design where decisions must stick.
- Spreading a new technique (TDD, hexagonal arch) across the team via kata.

## Skip If (ANY kills it)

- Routine CRUD, typo fixes, dependency bumps — overhead exceeds benefit.
- Async teams with more than three time zones — coordination cost exceeds knowledge gain.
- Solo founder or two-person team — that is pairing, not mobbing.
- When more than 50 percent of time is spent waiting on builds or external APIs.
- Teams that have never paired — start with pairing for 2-4 weeks first.
- Tasks the team genuinely needs to parallelize to hit a deadline.

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

- parent skill: `free/dev/software-developer/`
