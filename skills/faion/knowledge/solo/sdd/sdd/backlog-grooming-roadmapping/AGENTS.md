---
slug: backlog-grooming-roadmapping
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Backlog grooming is the weekly practice of scoring, reordering, and refining items in `.
content_id: "ed721940dbfde52b"
tags: [backlog, grooming, roadmap, prioritization, rice, moscow]
---
# Backlog Grooming and Roadmapping

## Summary

**One-sentence:** Backlog grooming is the weekly practice of scoring, reordering, and refining items in `.

**One-paragraph:** Backlog grooming is the weekly practice of scoring, reordering, and refining items in `.aidocs/backlog/` using RICE or MoSCoW frameworks. Roadmapping translates the groomed backlog into a Now/Next/Later horizon document. Agent-generated RICE scores are always marked `[estimate]` — they are hypotheses, not data. Never more than 3 items as P0. Use Now/Next/Later over date-based roadmaps to avoid false precision.

## Applies If (ALL must hold)

- Weekly or monthly: agent-assisted grooming session to score and reorder `.aidocs/backlog/`.
- When the backlog exceeds 20 items without re-prioritization in 2+ weeks.
- Starting a new quarter: generate or update roadmap.md from current backlog state.
- When performing MVP scoping: run MoSCoW analysis against a candidate feature set.

## Skip If (ANY kills it)

- As a replacement for human strategic decisions — P0 prioritization requires business context the agent lacks.
- During active feature execution — grooming is planning work; mixing them degrades both.
- When roadmap.md does not yet exist — create it with human-defined horizons first.
- For items requiring stakeholder input the agent cannot simulate (pricing, partnerships).

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

- parent skill: `solo/sdd/sdd/`
