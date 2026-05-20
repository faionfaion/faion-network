---
slug: voice-basics
tier: geek
group: ai
domain: multimodal-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Building conversational voice agents that chain STT (Whisper) to LLM (GPT-4o) to TTS into a turn-based loop.
content_id: "65615e7740d6887a"
tags: [voice, speech-to-text, text-to-speech, agents, realtime]
---
# Voice Agents - Basics

## Summary

**One-sentence:** Building conversational voice agents that chain STT (Whisper) to LLM (GPT-4o) to TTS into a turn-based loop.

**One-paragraph:** Building conversational voice agents that chain STT (Whisper) to LLM (GPT-4o) to TTS into a turn-based loop. Covers the basic architecture, latency budget per component, tool-calling integration, and the core pitfalls of fixed-duration recording and unbounded conversation history.

## Applies If (ALL must hold)

- Customer service automation requiring natural voice interaction
- Accessibility tools where text input is not viable
- Voice-controlled CLI wrappers for internal tools
- Real-time voice assistants embedded in hardware
- Adding speech I/O to an existing text agent

## Skip If (ANY kills it)

- Latency requirements below 800ms end-to-end - use OpenAI Realtime API (WebSocket) instead
- High-security contexts where audio recording raises GDPR/compliance concerns
- Noisy environments without pre-processing (SNR below 10dB) - Whisper accuracy degrades significantly
- Tasks where text output is superior (structured data, code, tables) - voice cannot render formatting

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
