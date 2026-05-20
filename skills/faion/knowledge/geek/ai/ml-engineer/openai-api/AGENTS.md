---
slug: openai-api
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: OpenAI Platform provides Chat Completions, the Responses API (2025+, stateful), Structured Outputs, Batch API (50% discount), embeddings, Whisper, TTS, DALL-E, and fine-tuning.
content_id: "cc027a7b2fe0a111"
tags: [openai, llm-api, structured-output, function-calling, batch-processing]
---
# OpenAI API Integration

## Summary

**One-sentence:** OpenAI Platform provides Chat Completions, the Responses API (2025+, stateful), Structured Outputs, Batch API (50% discount), embeddings, Whisper, TTS, DALL-E, and fine-tuning.

**One-paragraph:** OpenAI Platform provides Chat Completions, the Responses API (2025+, stateful), Structured Outputs, Batch API (50% discount), embeddings, Whisper, TTS, DALL-E, and fine-tuning. Pin exact model versions (gpt-4o-2024-08-06). Use Structured Outputs (beta.chat.completions.parse) not JSON mode. Set max_tokens on every call. For new projects, prefer the Responses API over Chat Completions — it manages conversation state server-side.

## Applies If (ALL must hold)

- Production app requiring best-in-class structured output with native schema enforcement
- Vision tasks requiring GPT-4o's image understanding
- Batch processing of non-time-sensitive data (50% cost discount via Batch API)
- Function calling / tool use as the primary agentic mechanism
- Audio transcription (Whisper) or TTS in agent pipelines
- Responses API's built-in conversation state management is needed

## Skip If (ANY kills it)

- Privacy-sensitive data that must not leave your infrastructure (use local Ollama instead)
- Very long context (>128K tokens) — use Claude (200K) or Gemini (2M)
- When Anthropic Claude's instruction-following is more reliable for your specific task
- Tight budget with high-volume simple tasks — Gemini Flash ($0.10/M) is cheaper than gpt-4o-mini ($0.15/M)
- When you need >128K context for a single call (use gpt-4.1 with 1M context or alternatives)

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
