---
slug: structured-output-patterns
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production patterns for reliable LLM structured extraction: Pydantic schema design, retry with error-message injection, streaming JSON handling, and the StructuredOutputService abstraction.
content_id: "7c298344b8da7683"
tags: [structured-output, pydantic, json, validation, agent-pipeline]
---
# Structured Output Patterns

## Summary

**One-sentence:** Production patterns for reliable LLM structured extraction: Pydantic schema design, retry with error-message injection, streaming JSON handling, and the StructuredOutputService abstraction.

**One-paragraph:** Production patterns for reliable LLM structured extraction: Pydantic schema design, retry with error-message injection, streaming JSON handling, and the StructuredOutputService abstraction. Core rule: keep schemas flat (1–2 nesting levels) — models handle flat schemas with near-zero errors; deeply nested schemas (5+ levels) cause frequent parse failures even in structured output mode.

## Applies If (ALL must hold)

- Agent pipelines passing data between steps — structured output prevents parse errors at handoff points
- Extracting information from unstructured text (emails, docs, PDFs) for downstream processing
- Multi-agent coordination where subagent outputs must conform to a contract
- Any agent output feeding into a database, API, or service expecting typed data
- Replacing regex-based parsing with LLM extraction for complex, variable-format inputs

## Skip If (ANY kills it)

- Free-form conversational responses — forcing JSON on chat output degrades quality
- Schema changes frequently — Pydantic + re-generation overhead is unnecessary if shape unknown at design time
- Simple string outputs (yes/no, short answers) — structured output adds token overhead for no gain
- OpenAI Structured Outputs beta unavailable for your model tier — fall back to JSON mode with manual validation

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

- parent skill: `geek/ai/llm-integration/`
