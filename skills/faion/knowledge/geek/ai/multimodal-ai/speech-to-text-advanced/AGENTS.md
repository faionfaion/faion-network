---
slug: speech-to-text-advanced
tier: geek
group: ai
domain: multimodal-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Long audio processing (>25MB), speaker diarization, and production TranscriptionService with provider routing (OpenAI, faster-whisper, local Whisper).
content_id: "930bd90c90cbb6fd"
tags: [speech-to-text, transcription, diarization, long-audio, whisper, pyannote]
---
# Speech-to-Text Advanced

## Summary

**One-sentence:** Long audio processing (>25MB), speaker diarization, and production TranscriptionService with provider routing (OpenAI, faster-whisper, local Whisper).

**One-paragraph:** Long audio processing (>25MB), speaker diarization, and production TranscriptionService with provider routing (OpenAI, faster-whisper, local Whisper). Covers chunked transcription via LongAudioTranscriber, speaker labeling via SpeakerDiarizer (pyannote 3.1), and known bugs that must be patched before production use.

## Applies If (ALL must hold)

- Audio files larger than 25MB need transcription (Whisper API hard limit)
- Multi-speaker recordings (meetings, podcasts, interviews) need speaker attribution
- Long-form transcription (1+ hour files) requiring timestamps and segment structure
- Building a production STT service with provider fallback (cloud vs. local GPU)

## Skip If (ANY kills it)

- Audio under 25MB and single speaker — use speech-to-text-basics direct API call; LongAudioTranscriber adds unnecessary overhead
- Real-time (live) transcription — Whisper is batch-only; use Deepgram or AssemblyAI streaming
- GPU unavailable and diarization needed — pyannote on CPU is ~10x real-time; impractical
- Language is non-standard or heavily accented without prior quality validation

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
