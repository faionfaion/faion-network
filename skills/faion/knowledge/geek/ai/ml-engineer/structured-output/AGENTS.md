---
slug: structured-output
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured output ensures LLMs return data in consistent, parseable formats (JSON matching a schema).
content_id: "1237cf075a04f940"
tags: [structured-output, json-schema, pydantic, validation, type-safety]
---
# Structured Output for LLMs

## Summary

**One-sentence:** Structured output ensures LLMs return data in consistent, parseable formats (JSON matching a schema).

**One-paragraph:** Structured output ensures LLMs return data in consistent, parseable formats (JSON matching a schema). Define output schemas as Pydantic models. For OpenAI: use `client.beta.chat.completions.parse()` (native structured output). For Claude: use tool-calling via `instructor` library. For local models: use `outlines` for token-level grammar constraints. Never use raw JSON mode — it guarantees valid JSON syntax but NOT schema compliance.

## Applies If (ALL must hold)

- Agent tool calls return typed data consumed by downstream code
- Extracting structured records from unstructured documents (invoices, forms, emails)
- Building pipelines where each stage's input is the previous stage's validated output
- Any place where a parsing failure would silently corrupt downstream state
- Multi-model workflows where one model's output feeds into another model's prompt

## Skip If (ANY kills it)

- Free-form creative generation where schema over-constrains the response
- Exploratory research where the output structure is unknown in advance
- Very long outputs (>2K tokens) with complex nested schemas — reliability degrades
- Streaming responses where structured output cannot be validated until complete

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

- parent skill: `geek/ai/ml-engineer/`
