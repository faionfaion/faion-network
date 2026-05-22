---
slug: gemini-basics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Core concepts, setup, text generation, streaming, and chat conversations.
content_id: "f105a21b257899a4"
tags: [gemini, llm-api, text-generation, chat, streaming]
---
# Gemini API Basics

## Summary

**One-sentence:** Core concepts, setup, text generation, streaming, and chat conversations.

**One-paragraph:** Core concepts, setup, text generation, streaming, and chat conversations. This methodology covers model selection (2.0 Flash vs. 1.5 Pro vs. Thinking), initialization, basic text generation with configuration, streaming responses, multi-turn chat, safety settings, and error handling with retry logic.

## Applies If (ALL must hold)

- Starting a new project that will use Gemini and needs auth, model selection, and generation config established.
- Exploring Gemini model capabilities (Flash vs. Pro vs. Thinking) before committing to an architecture.
- Building a simple text generation or chat pipeline that does not yet need multimodal or function calling.
- The team needs a working reference implementation of streaming, async, and JSON output modes.

## Skip If (ANY kills it)

- The task requires function calling or tool use — see gemini-api-integration for that pattern.
- You need file uploads (audio/video/large docs) — use the Files API from gemini-api-integration.
- The context window needed exceeds what Flash supports and you have not benchmarked Pro vs. Flash trade-offs yet.
- You are integrating with Google Cloud enterprise infra — start with Vertex AI patterns, not AI Studio keys.

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
