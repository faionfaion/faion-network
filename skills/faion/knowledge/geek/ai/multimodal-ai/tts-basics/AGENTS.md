---
slug: tts-basics
tier: geek
group: ai
domain: multimodal-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Convert text to natural speech using OpenAI TTS, ElevenLabs, or Google Cloud TTS.
content_id: "c8689c6211136998"
tags: [tts, audio-generation, voice-synthesis, openai-tts, caching]
---
# Text-to-Speech Basics

## Summary

**One-sentence:** Convert text to natural speech using OpenAI TTS, ElevenLabs, or Google Cloud TTS.

**One-paragraph:** Convert text to natural speech using OpenAI TTS, ElevenLabs, or Google Cloud TTS. Covers voice selection, SSML control for Google/Azure, caching by content hash, and the provider differences every agent must know before routing a TTS call.

## Applies If (ALL must hold)

- Converting article, news, or notification text to audio in an agent pipeline.
- Generating narration tracks for video content automation.
- Adding voice output to a chatbot or assistant interface.
- Creating audio previews of generated text for human review.
- Any single-pass synthesis where text fits under 4000 characters.

## Skip If (ANY kills it)

- Text exceeds 4000 characters — use tts-implementation which provides LongTextTTS chunking.
- Sub-200ms latency required — OpenAI TTS adds 300-800ms minimum; cache known phrases instead.
- A specific person's voice is required — use ElevenLabs voice cloning (tts-implementation).
- SSML markup (pauses, prosody, say-as) is needed with OpenAI TTS — OpenAI does not support SSML; route SSML to Google Cloud or Azure only.
- Text contains heavy domain abbreviations (API, ETA, DB) without preprocessing — they are read literally and sound odd to listeners.

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
