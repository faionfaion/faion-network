---
slug: tts-implementation
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production TTS service with multi-provider support (OpenAI, ElevenLabs, Google Cloud), content-hash caching, long-text chunking via LongTextTTS, real-time streaming via async PCM, and voice cloning via ElevenLabs.
content_id: "e877b30726476edc"
tags: [tts, audio-production, streaming, voice-cloning, multi-provider]
---
# Text-to-Speech Implementation

## Summary

**One-sentence:** Production TTS service with multi-provider support (OpenAI, ElevenLabs, Google Cloud), content-hash caching, long-text chunking via LongTextTTS, real-time streaming via async PCM, and voice cloning via ElevenLabs.

**One-paragraph:** Production TTS service with multi-provider support (OpenAI, ElevenLabs, Google Cloud), content-hash caching, long-text chunking via LongTextTTS, real-time streaming via async PCM, and voice cloning via ElevenLabs. Use when tts-basics patterns are insufficient — this layer adds TTSService, cache eviction, and streaming delivery.

## Applies If (ALL must hold)

- Long-form content (articles, podcast episodes) exceeding 4096-char API limits.
- Production TTS service needing content-hash caching, retry, and multi-provider support.
- Real-time streaming TTS to a speaker or WebSocket client.
- Voice cloning from audio samples via ElevenLabs.
- Multilingual synthesis where Google Neural2 outperforms OpenAI on specific languages.

## Skip If (ANY kills it)

- Simple one-off audio generation — use tts-basics direct API call; TTSService setup adds overhead.
- Voice cloning of persons without explicit consent — ElevenLabs ToS requires consent documentation.
- Sub-200ms first-audio-byte latency in telephony — streaming helps but cannot reach <50ms.
- Languages not covered by OpenAI TTS — use Google Cloud or Azure TTS directly.

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

- parent skill: `geek/ai/multimodal-ai/`
