---
slug: openai-function-calling
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: OpenAI-specific patterns for function calling (tool use), Pydantic-validated structured extraction via `client.
content_id: "5a36a22471356ca3"
tags: [function-calling, openai, structured-output, tool-use, pydantic]
---
# OpenAI Function Calling and Structured Outputs

## Summary

**One-sentence:** OpenAI-specific patterns for function calling (tool use), Pydantic-validated structured extraction via `client.

**One-paragraph:** OpenAI-specific patterns for function calling (tool use), Pydantic-validated structured extraction via `client.beta.chat.completions.parse`, parallel tool calls, and multimodal extensions (DALL-E 3, Whisper, TTS). The primary distinction from generic tool use: structured outputs enforce schema compliance at the API level, not just via prompt instruction.

## Applies If (ALL must hold)

- Reliable, schema-validated JSON extraction from unstructured text
- Pipeline driving external actions (API calls, DB writes) triggered by model decisions
- Multiple tools needed in a single model response (parallel tool calls) to reduce round-trips
- Image generation (DALL-E 3), speech-to-text (Whisper), or TTS alongside text LLM calls
- Strict output format enforcement where `json_object` mode alone is insufficient

## Skip If (ANY kills it)

- Only need a JSON blob without schema strictness — `response_format={"type": "json_object"}` is simpler
- Simple prompting + regex post-processing is sufficient
- Schema is deeply nested (>10 params) causing frequent misselection — simplify the schema first
- Real-time audio generation at sub-200ms latency — TTS streaming is not suitable

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
