---
slug: openai-chat-completions
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Complete guide to the OpenAI Chat Completions endpoint (`/v1/chat/completions`): request structure, model selection, parameters (temperature, max_tokens, response_format), streaming, vision (URL and base64), error handling with exponential backoff, rate limit headers, and cost tracking via tiktoken.
content_id: "d6a311d947a72fda"
tags: [openai, chat-completions, api, streaming, vision]
---
# OpenAI Chat Completions

## Summary

**One-sentence:** Complete guide to the OpenAI Chat Completions endpoint (`/v1/chat/completions`): request structure, model selection, parameters (temperature, max_tokens, response_format), streaming, vision (URL and base64), error handling with exponential backoff, rate limit headers, and cost tracking via tiktoken.

**One-paragraph:** Complete guide to the OpenAI Chat Completions endpoint (`/v1/chat/completions`): request structure, model selection, parameters (temperature, max_tokens, response_format), streaming, vision (URL and base64), error handling with exponential backoff, rate limit headers, and cost tracking via tiktoken. The core rule: always read `stop_reason` — `"max_tokens"` means silent truncation; never parse JSON from a truncated response.

## Applies If (ALL must hold)

- Building agent pipelines calling OpenAI models (gpt-4o, gpt-4o-mini, o1, o3-mini)
- Streaming partial outputs to users or downstream pipeline steps in real time
- Generating structured JSON via `response_format={"type": "json_object"}`
- Multi-image or screenshot analysis inside an automated workflow
- Cost-sensitive pipelines where gpt-4o-mini quality is acceptable

## Skip If (ANY kills it)

- When persistent conversation state is needed across sessions — use Assistants API
- When guaranteed schema compliance is required — use Structured Outputs (`beta.parse`) not JSON Mode
- Tasks requiring more than 128K context — use Claude 200K or Gemini 2M
- When Anthropic Claude is available and task quality matters more than vendor diversity

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
