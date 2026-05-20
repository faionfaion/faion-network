---
slug: claude-messages-api
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The Claude Messages API is the single completion endpoint for all Claude calls.
content_id: "66c2b069488be49c"
tags: [claude, messages-api, streaming, vision, multi-turn]
---
# Claude Messages API

## Summary

**One-sentence:** The Claude Messages API is the single completion endpoint for all Claude calls.

**One-paragraph:** The Claude Messages API is the single completion endpoint for all Claude calls. Covers basic request structure, parameters, response object, multi-turn history management, vision (base64 and URL, images and PDFs), streaming (text_stream and event-based), and SSE event format. The core rule: append the full `resp.content` list (not just text) as the assistant turn in multi-turn history — tool_use blocks must be preserved or the next turn gets a 400 error.

## Applies If (ALL must hold)

- All direct Claude API calls — Messages is the only completion endpoint.
- Streaming responses to a user interface or pipeline sink consuming partial text.
- Multi-turn agent conversations with explicit message history management.
- Vision tasks: screenshot analysis, document OCR, UI inspection, PDF summarization.
- When the agent needs to detect `stop_reason` to branch logic.

## Skip If (ANY kills it)

- When persistent thread storage is needed across sessions — build your own; Anthropic has no Threads equivalent.
- When guaranteed schema compliance without retry loops is required — use OpenAI `beta.parse` or `instructor`.
- High-volume batch jobs — prefer the Batch API (50% cost reduction).
- Computer Use or Extended Thinking inside a stateless lambda — those require multi-turn conversation state.

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
