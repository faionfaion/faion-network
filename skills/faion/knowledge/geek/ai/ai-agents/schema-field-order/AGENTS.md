---
slug: schema-field-order
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: In a structured-output schema (JSON schema, Pydantic model, tool input schema, response_format), place dependent fields AFTER their dependencies.
content_id: "89674b71f298e496"
tags: [schema, field-order, structured-output, autoregressive, chain-of-thought]
---
# Schema Field Order — Autoregressive Steering

## Summary

**One-sentence:** In a structured-output schema (JSON schema, Pydantic model, tool input schema, response_format), place dependent fields AFTER their dependencies.

**One-paragraph:** In a structured-output schema (JSON schema, Pydantic model, tool input schema, response_format), place dependent fields AFTER their dependencies. The model generates left-to-right and each field can attend only to fields that came before it. If field B is conceptually derived from field A, A must appear earlier in the schema than B. This is free chain-of-thought: every "thought" field placed before the "answer" field acts as scratchpad, and every "input echo" field placed before "output" acts as a re-grounding step.

## Applies If (ALL must hold)

- Whenever your schema has fields where one depends on another (almost always).
- When you want a "reasoning before answer" effect without using extended-thinking APIs.
- When you want a "title from content" pattern — content first, title last.
- When you need re-grounding on long inputs — put a field that restates the question before the answer.

## Skip If (ANY kills it)

- Schemas with no semantic dependency (pure parallel extraction of independent facts) — order does not matter.
- When your runtime parses fields in arbitrary order (rare; almost all do declaration-order generation).

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

- parent skill: `geek/ai/ai-agents/`
