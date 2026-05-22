---
slug: speech-to-text
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Speech-to-text (STT) methodology covering provider selection (OpenAI Whisper/GPT-4o, AssemblyAI, Deepgram, ElevenLabs Scribe), local model deployment (faster-whisper, whisper.
content_id: "cb76315447243ae2"
tags: [speech-to-text, stt, transcription, audio, provider-selection]
---
# Speech-to-Text Integration

## Summary

**One-sentence:** Speech-to-text (STT) methodology covering provider selection (OpenAI Whisper/GPT-4o, AssemblyAI, Deepgram, ElevenLabs Scribe), local model deployment (faster-whisper, whisper.

**One-paragraph:** Speech-to-text (STT) methodology covering provider selection (OpenAI Whisper/GPT-4o, AssemblyAI, Deepgram, ElevenLabs Scribe), local model deployment (faster-whisper, whisper.cpp), integration patterns, and cost optimization. Decision axis: real-time vs batch, accuracy vs cost, cloud vs self-hosted.

## Applies If (ALL must hold)

- Meeting transcription, voice notes, podcast/video indexing (batch).
- Real-time captioning, voice commands, live call analysis (streaming).
- Any feature where users speak instead of type.
- Audio content pipelines requiring transcript search or summarization.

## Skip If (ANY kills it)

- Audio is synthetic TTS output — transcribe the source text instead.
- Audio quality is below 8kHz mono — accuracy will be poor across all providers; fix the recording.
- Language is not in the provider's supported list — verify before building.

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
