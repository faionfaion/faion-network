---
slug: ollama-tool-calling
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Ollama supports OpenAI-compatible tool/function calling and JSON schema structured outputs.
content_id: "c56516d6395257f7"
tags: [ollama, tool-calling, structured-output, function-calling]
---
# Ollama Tool Calling and Structured Outputs

## Summary

**One-sentence:** Ollama supports OpenAI-compatible tool/function calling and JSON schema structured outputs.

**One-paragraph:** Ollama supports OpenAI-compatible tool/function calling and JSON schema structured outputs. Tool calling requires Llama 3.1 8B or higher with num_ctx set to at least 32768. Structured output uses the format parameter with a Pydantic-derived JSON schema.

## Applies If (ALL must hold)

- Building a local agent that needs to call external tools or APIs without cloud API costs.
- Extracting structured data (entities, classifications, analysis) from text with schema validation.
- Replacing cloud LLM tool-calling in CI pipelines or privacy-sensitive workflows.
- Testing agent tool-calling logic locally before deploying against cloud models.

## Skip If (ANY kills it)

- Models smaller than 13B — tool calling reliability degrades significantly; Llama 3.1 8B is the practical minimum.
- Context window below 32k — the model returns text instead of JSON tool calls silently.
- Complex multi-tool chains where frontier cloud models (GPT-4o, Claude) produce significantly more reliable results.
- Structured output schemas with deeply nested objects — compliance varies by model; test thoroughly before production.

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
