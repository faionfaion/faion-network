---
slug: gemini-multimodal
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Gemini is the only frontier model with native video understanding (no frame extraction), native audio processing (no separate Whisper call), and a 2M-token context window.
content_id: "84e848cad8338495"
tags: [gemini, multimodal, video, audio, context-caching]
---
# Gemini Multimodal Integration

## Summary

**One-sentence:** Gemini is the only frontier model with native video understanding (no frame extraction), native audio processing (no separate Whisper call), and a 2M-token context window.

**One-paragraph:** Gemini is the only frontier model with native video understanding (no frame extraction), native audio processing (no separate Whisper call), and a 2M-token context window. For multi-document pipelines, context caching cuts costs 75% vs. full-price per call. Without the polling guard and file-expiry handler, agents loop indefinitely or silently re-upload duplicate files.

## Applies If (ALL must hold)

- Processing video natively — no frame extraction or separate transcription pipeline needed
- Audio transcription and analysis without a separate Whisper call
- Long document pipelines — 2M token context handles books, large codebases, multi-document sets
- Combined modality tasks: video + PDF slides, image + audio explanation, multiple images compared
- Code execution tasks where the model must compute and return results
- Enterprise Google Cloud deployments requiring CMEK, VPC Service Controls, IAM (Vertex AI)

## Skip If (ANY kills it)

- Simple text-only tasks — adds SDK complexity if already on OpenAI/Anthropic
- When maximum reasoning depth matters — Claude Opus and o1 outperform Gemini on complex multi-step reasoning
- Privacy-sensitive content that cannot leave on-premises — Gemini requires upload to Google servers
- Low-latency real-time voice — Gemini Live API is more complex than OpenAI Realtime API
- Teams with deep OpenAI or Anthropic expertise — switching SDK adds friction for marginal gains on text tasks

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
