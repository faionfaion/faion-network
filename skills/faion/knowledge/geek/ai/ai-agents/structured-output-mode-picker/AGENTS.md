---
slug: structured-output-mode-picker
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Four constrained-decoding modes ship in 2026 SDKs and they are NOT interchangeable.
content_id: "35c1c0ce3b817744"
tags: [structured-outputs, json-schema, tool-calling, constrained-decoding, llm-api]
---
# Structured Output Mode — JSON-Mode vs SO vs Tool-Call vs Grammar

## Summary

**One-sentence:** Four constrained-decoding modes ship in 2026 SDKs and they are NOT interchangeable.

**One-paragraph:** Four constrained-decoding modes ship in 2026 SDKs and they are NOT interchangeable. JSON mode guarantees only valid JSON; Structured Outputs (response_format: json_schema, strict: true) guarantees full schema compliance; tool calls guarantee schema-compliant arguments and dispatch to a function; grammar-mode (XGrammar / Outlines / GBNF) constrains generation to any context-free grammar including non-JSON DSLs. Picking by use case — extraction → SO, action → tool call, custom DSL/SQL → grammar, legacy fallback → json mode — saves tokens and prevents silent constraint violations.

## Applies If (ALL must hold)

- Choosing constrained decoding for a new agent or pipeline stage
- Migrating a legacy response_format={"type": "json_object"} codebase
- Adding a constrained-output step on a local open-source model (vLLM/Ollama)
- Designing an agent that mixes data extraction and action dispatch in one loop

## Skip If (ANY kills it)

- Free-form chat where structure is undesirable — keep plain text
- One-off scripts where downstream parsing tolerates failure — json_object is acceptable
- Pure transformation tasks fully solved by regex / deterministic code — skip the LLM
- When the chosen provider does not support the mode you picked — fall back to closest peer

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
