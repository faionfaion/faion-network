---
slug: schema-version-pinning
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every Pydantic model used as an SO `text_format` or tool `input_schema` carries a `schema_version: Literal["vN"] = "vN"` discriminator field, and each pipeline event/log persists it.
content_id: "6fa16b1e8a28d935"
tags: [pydantic, structured-output, schema, versioning, multi-stage]
---
# Versioned SO Contracts — schema_version Pin in Every Payload

## Summary

**One-sentence:** Every Pydantic model used as an SO `text_format` or tool `input_schema` carries a `schema_version: Literal["vN"] = "vN"` discriminator field, and each pipeline event/log persists it.

**One-paragraph:** Every Pydantic model used as an SO `text_format` or tool `input_schema` carries a `schema_version: Literal["vN"] = "vN"` discriminator field, and each pipeline event/log persists it. When a schema changes you bump the version and keep the previous parser registered for at least one rollback window. Strict mode forces the model to emit the declared literal, so events are guaranteed-tagged at the source. Silent schema drift — the dominant failure mode in multi-stage agent pipelines — becomes a typed branch dispatcher: "v3" events route to the v3 parser, "v4" to v4, unknown versions raise loudly instead of corrupting downstream state.

## Applies If (ALL must hold)

- Multi-stage pipelines where output of stage N is input to stage N+1
- Event-sourced agent systems with replay or backfill
- Cross-team contracts where producer and consumer ship independently
- Long-running batch jobs that span schema-change releases
- Stored conversation logs you plan to re-process months later

## Skip If (ANY kills it)

- One-shot scripts and exploratory notebooks — overhead not justified
- Single-process pipelines where producer and consumer always deploy together
- Schemas with no breaking changes expected ever (rare; usually wrong)

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
