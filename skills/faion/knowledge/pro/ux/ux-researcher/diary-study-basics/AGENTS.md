---
slug: diary-study-basics
tier: pro
group: ux
domain: ux-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A longitudinal research method where participants self-record behaviors, thoughts, and contexts in the moment or shortly after, over days or weeks.
content_id: "d9b0492cfdc20403"
tags: [diary, study, longitudinal, self-report, experience]
---
# Diary Study Basics

## Summary

**One-sentence:** A longitudinal research method where participants self-record behaviors, thoughts, and contexts in the moment or shortly after, over days or weeks.

**One-paragraph:** A longitudinal research method where participants self-record behaviors, thoughts, and contexts in the moment or shortly after, over days or weeks. Three variants: interval-contingent (fixed schedule), event-contingent (triggered by occurrence), and signal-contingent (random prompts). Each entry captures when, where, what happened, how the participant felt, and their interpretation.

## Applies If (ALL must hold)

- Studying behavior that unfolds over days or weeks (onboarding journeys, habit formation, multi-device patterns).
- Capturing real-world context (location, mood, environment) that lab conditions eliminate.
- Tracking how user understanding evolves from novice to proficient.
- Pre-purchase or high-consideration journeys where each touchpoint matters.
- Validating retention drop-off hypotheses by following individual usage trajectories.

## Skip If (ANY kills it)

- Need findings in under two weeks — minimum useful diary period is 7-14 days.
- Single isolated event with no context dependency — a post-event interview is faster and cheaper.
- Sensitive personal contexts (mental health, finances) without ethics review — continuous self-documentation feels surveillance-like.
- Behaviors already covered by product analytics — diary adds self-report noise without incremental signal.
- Rare events (less than once per week) — participants miss too many triggers to form useful patterns.

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

- parent skill: `pro/ux/ux-researcher/`
