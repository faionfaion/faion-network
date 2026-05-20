---
slug: embedded-scratchpad-field
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Before any non-trivial answer field, embed a scratchpad, plan_steps, or reasoning field IN the schema.
content_id: "44d179def52bb9fd"
tags: [structured-output, chain-of-thought, schema-design, reasoning, tab-cot]
---
# Embedded Scratchpad Field

## Summary

**One-sentence:** Before any non-trivial answer field, embed a scratchpad, plan_steps, or reasoning field IN the schema.

**One-paragraph:** Before any non-trivial answer field, embed a scratchpad, plan_steps, or reasoning field IN the schema. The model writes its working notes there before generating the answer. This is structured-output's equivalent of thinking tags but works even in strict JSON mode where free-form preambles aren't allowed.

## Applies If (ALL must hold)

- Strict JSON mode (no free-form preamble allowed)
- Decisions that benefit from CoT but where you also need structured output
- Tasks with greater than 1 reasoning step
- Anywhere "the model commits before thinking" is a known failure mode

## Skip If (ANY kills it)

- Pure transformation tasks where reasoning adds latency without accuracy
- When the upstream model is already a reasoning model (o-series, Opus thinking) — paying twice
- For trivial fields where the schema is already forcing the model through an enum

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
