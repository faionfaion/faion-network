---
slug: usability-testing
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Observe real users completing tasks with a product to discover what works, what confuses, and where users struggle.
content_id: "a6fd93373f75147c"
tags: [usability, user-research, testing, ux-validation, qualitative]
---
# Usability Testing

## Summary

**One-sentence:** Observe real users completing tasks with a product to discover what works, what confuses, and where users struggle.

**One-paragraph:** Observe real users completing tasks with a product to discover what works, what confuses, and where users struggle. Generates test plans, session scripts, and structured findings reports with severity ratings. Use when you need evidence-based validation of design decisions before or after launch.

## Applies If (ALL must hold)

- A feature or flow has never been tested with real users
- Conversion or task-completion metrics show unexplained drops
- A redesign is complete and ready for pre-launch validation
- Synthesizing recordings or transcripts into structured findings for stakeholders
- Generating test plans from a feature spec or acceptance criteria set

## Skip If (ANY kills it)

- Nothing testable yet (no wireframe or prototype) — nothing to observe
- Fewer than 3 participants available — no pattern detection is meaningful at that scale
- Large-N quantitative benchmarking (SUS scoring, statistical significance) — use survey instruments instead
- As a substitute for live facilitation — agents cannot observe non-verbal cues or probe nuance

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

- parent skill: `solo/ux/ux-ui-designer/`
