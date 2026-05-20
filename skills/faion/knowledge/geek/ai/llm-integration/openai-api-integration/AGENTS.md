---
slug: openai-api-integration
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: OpenAI API provides access to GPT-4, GPT-4 Turbo, GPT-4o, and other models for text generation, embeddings, image generation, and more.
content_id: "b56e9abdbb892e7e"
tags: [openai, gpt-4, api-integration, llm, async]
---
# OpenAI API Integration

## Summary

**One-sentence:** OpenAI API provides access to GPT-4, GPT-4 Turbo, GPT-4o, and other models for text generation, embeddings, image generation, and more.

**One-paragraph:** OpenAI API provides access to GPT-4, GPT-4 Turbo, GPT-4o, and other models for text generation, embeddings, image generation, and more. This methodology covers authentication, model selection, request handling, and production-ready integration patterns.

## Applies If (ALL must hold)

- Building conversational AI applications
- Text generation, summarization, translation
- Code generation and analysis
- Content moderation and classification
- When you need state-of-the-art language capabilities
- Production applications requiring high reliability

## Skip If (ANY kills it)

- The task fits a smaller model (Claude Haiku, GPT-4o-mini) — always start with the cheapest model that meets quality bar
- You need 1M+ context — Gemini 1.5 Pro is the right tool; OpenAI's max is 128K
- The project policy requires on-premise or self-hosted inference — use Ollama or a local model
- The response format is unknown/flexible — structured output requires knowing the schema up front

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
