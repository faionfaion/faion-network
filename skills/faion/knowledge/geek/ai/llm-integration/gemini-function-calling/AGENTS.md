---
slug: gemini-function-calling
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Gemini function calling lets Python functions serve as LLM tools by using their docstrings and type hints as the tool schema.
content_id: "02ab428132bc6fef"
tags: [gemini, function-calling, tool-use, grounding, embeddings]
---
# Gemini Function Calling, Grounding, and Embeddings

## Summary

**One-sentence:** Gemini function calling lets Python functions serve as LLM tools by using their docstrings and type hints as the tool schema.

**One-paragraph:** Gemini function calling lets Python functions serve as LLM tools by using their docstrings and type hints as the tool schema. The SDK supports automatic mode (model executes tools in-process) and manual mode (caller controls execution). Beyond tools, Gemini offers Google Search grounding for live web data and text-embedding-004 (768-dim) for RAG pipelines, plus native JSON schema-constrained output via response_mime_type.

## Applies If (ALL must hold)

- Pipelines running on Google Cloud / Vertex AI infrastructure.
- Tasks requiring Google Search grounding for live web data.
- RAG pipelines using text-embedding-004 (768-dim, multilingual).
- Structured extraction with JSON schema (simpler than tool-forcing).
- Agent loops where manual function calling allows logging, validation, and controlled execution.

## Skip If (ANY kills it)

- OpenAI or Claude is already in the pipeline — adding Gemini increases vendor surface area without clear benefit unless Search grounding is needed.
- Production pipelines requiring deterministic, auditable tool execution — automatic function calling is opaque and non-deterministic.
- Tasks requiring Anthropic Extended Thinking-level transparent reasoning.
- Complex nested function signatures — Gemini parses docstrings as schema; complex types degrade accuracy.

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
