---
slug: ai-persona-building
tier: geek
group: ux
domain: user-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Lightweight single-pass persona generation: a Sonnet subagent receives a structured description of a user type with known data points and a JTBD statement, and produces a persona card.
content_id: "2550b232685227d3"
tags: [persona-building, ux-research, ai-agents, lightweight-process]
---
# AI Persona Building (Lightweight)

## Summary

**One-sentence:** Lightweight single-pass persona generation: a Sonnet subagent receives a structured description of a user type with known data points and a JTBD statement, and produces a persona card.

**One-paragraph:** Lightweight single-pass persona generation: a Sonnet subagent receives a structured description of a user type with known data points and a JTBD statement, and produces a persona card. A Haiku subagent formats the card into the team's documentation template. No clustering step — suitable for early exploration or updating a single field, not for full segmentation.

## Applies If (ALL must hold)

- Lightweight persona creation needed quickly without a dedicated researcher
- Prototyping phase where placeholder personas unblock design decisions
- Updating a single persona field across an existing library
- Generating documentation from an already-agreed behavioral cluster description
- Supplementing thin data with AI-expanded hypotheses for rapid validation planning

## Skip If (ANY kills it)

- No real user data exists and the team plans to treat AI output as ground truth
- Regulated domains (healthcare, finance) where persona inaccuracy causes downstream harm
- Personas will drive hiring, pricing, or go-to-market budget without human review
- Full clustering from multi-source data is needed — use ai-assisted-persona-building instead

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

- parent skill: `geek/ux/user-researcher/`
