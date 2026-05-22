---
slug: speech-to-text-basics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Transcribing audio to text using OpenAI Whisper API, local Whisper, or faster-whisper (CTranslate2).
content_id: "e30865cc132b4b6f"
tags: [speech-to-text, transcription, whisper, audio, multilingual]
---
# Speech-to-Text Basics

## Summary

**One-sentence:** Transcribing audio to text using OpenAI Whisper API, local Whisper, or faster-whisper (CTranslate2).

**One-paragraph:** Transcribing audio to text using OpenAI Whisper API, local Whisper, or faster-whisper (CTranslate2). Covers API parameters for timestamps and translation, local model selection by hardware, and the 25MB file-size limit that forces pre-splitting.

## Applies If (ALL must hold)

- Transcribing recorded audio: interviews, meetings, podcasts, call recordings
- Building voice input pipelines where microphone audio is the primary channel
- Generating searchable transcripts with timestamps for media libraries
- Multilingual transcription or audio-to-English translation
- Pre-processing audio before LLM analysis (summarize, extract, classify)

## Skip If (ANY kills it)

- Real-time streaming requirements below 300ms — use Deepgram or AssemblyAI WebSocket streaming instead
- Audio files exceeding 25MB per file — must split first with pydub
- Extremely noisy audio (SNR below 5dB) — accuracy degrades to unusable
- High-volume production (>10k hours/month) — local faster-whisper on GPU is significantly cheaper

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
