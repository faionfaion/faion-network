---
slug: ai-assisted-persona-building
tier: geek
group: ux
domain: user-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Synthesize data-backed user personas from multi-source inputs (analytics CSVs, interview transcripts, survey exports) using a two-pass agent pipeline: a Sonnet subagent clusters behavioral patterns and produces draft persona JSON, then a validation agent checks each persona for JTBD consistency and flags fabricated fields.
content_id: "73260ac58e8f8236"
tags: [personas, ux-research, jtbd, data-driven, clustering]
---
# AI-Assisted Persona Building

## Summary

**One-sentence:** Synthesize data-backed user personas from multi-source inputs (analytics CSVs, interview transcripts, survey exports) using a two-pass agent pipeline: a Sonnet subagent clusters behavioral patterns and produces draft persona JSON, then a validation agent checks each persona for JTBD consistency and flags fabricated fields.

**One-paragraph:** Synthesize data-backed user personas from multi-source inputs (analytics CSVs, interview transcripts, survey exports) using a two-pass agent pipeline: a Sonnet subagent clusters behavioral patterns and produces draft persona JSON, then a validation agent checks each persona for JTBD consistency and flags fabricated fields. Human researchers approve before personas enter any design system.

## Applies If (ALL must hold)

- You have real user data (analytics events, interview transcripts, survey CSVs) to cluster
- You need to synthesize personas from multi-source data faster than manual affinity mapping
- A product team wants data-backed personas replacing assumption archetypes
- Updating stale personas after a major product pivot or new market entry
- Running a JTBD framing exercise alongside persona creation

## Skip If (ANY kills it)

- Zero real user data exists — AI will hallucinate plausible-sounding but false personas
- Product is in pre-discovery with no interviews or analytics yet
- Regulatory context prohibits feeding user data to third-party LLMs (HIPAA, GDPR special categories)
- Only 1–2 archetypes needed from a single homogeneous segment — manual synthesis is faster

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
