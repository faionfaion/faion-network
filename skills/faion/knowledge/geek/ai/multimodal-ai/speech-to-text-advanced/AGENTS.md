---
slug: speech-to-text-advanced
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces an advanced transcription service — speaker diarisation, word-timestamp alignment, vocabulary biasing, streaming via Deepgram/AssemblyAI, post-processing.
content_id: "930bd90c90cbb6fd"
complexity: medium
produces: code
est_tokens: 3200
tags: [speech-to-text, diarisation, streaming, deepgram, assemblyai, vocabulary-bias]
---
# Speech-to-Text Advanced

## Summary

**One-sentence:** Produces an advanced transcription service — speaker diarisation, word-timestamp alignment, vocabulary biasing, streaming via Deepgram/AssemblyAI, post-processing.

**One-paragraph:** Above Whisper basics, production transcription often needs: speaker diarisation (who said what), word-level timestamps (caption alignment, search), vocabulary biasing (boost domain terms / brand names), real-time streaming (sub-300ms), and post-processing (punctuation, filler removal, abbreviation expansion). This methodology produces a TranscriptionService class that routes between providers based on requirements: Whisper batch for non-streaming, Deepgram or AssemblyAI for streaming + diarisation, faster-whisper local for privacy. Output: diarised transcript with per-word timestamps + speaker labels + audit trail.

**Ефективно для:** інженера, що транскрибує meetings / interviews з кількома спікерами + потребує real-time captioning або vocabulary boost для domain-specific terms.

## Applies If (ALL must hold)

- Need speaker diarisation OR word timestamps OR vocabulary biasing OR sub-300ms streaming.
- Latency / accuracy bar above what Whisper basics can deliver.
- Budget allows third-party API (Deepgram / AssemblyAI) if privacy permits.
- Post-processing pipeline (punctuation / filler-removal) is available or builds into the service.

## Skip If (ANY kills it)

- Simple single-speaker transcription — `[[speech-to-text-basics]]` is sufficient.
- No budget for third-party API and no GPU for local advanced models.
- Stream not needed and content fits 25 MB — use basics.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Provider API keys (Deepgram / AssemblyAI / OpenAI) | secret | secrets manager |
| Vocabulary boost list (brand names, jargon) | YAML | content repo |
| Speaker hint count (per-meeting) | int | calendar / metadata |
| Post-processing pipeline (punctuation + filler removal) | python | service repo |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/multimodal-ai/speech-to-text-basics` | Single-provider Whisper baseline. |
| `geek/ai/llm-integration/openai-api-integration` | Baseline SDK setup. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: diarisation provider routing, word timestamps for captions, vocab biasing, streaming via Deepgram/AssemblyAI, sentence-level post-process, audit. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for advanced-stt-config + diarised transcript shape. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: diarisation via heuristic, vocab in prompt instead of param, no speaker hint, missing speaker labels, no post-process. | ~800 |
| `content/04-procedure.xml` | medium | Steps: requirements gather → pick provider → wire diarisation + word ts + vocab → post-process → audit. | ~800 |
| `content/06-decision-tree.xml` | essential | Routes diarisation/stream/vocab needs to Whisper / Deepgram / AssemblyAI / faster-whisper. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `pick-provider` | opus | Multi-axis (cost / quality / streaming) reasoning. |
| `wire-diarisation` | sonnet | Mechanical SDK. |
| `tune-vocab` | sonnet | Term-by-term tuning. |
| `audit-speaker-labels` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/transcription_service.py` | TranscriptionService class with multi-provider router + diarisation + post-process. |
| `templates/prompt-transcribe.txt` | Prompt-template for downstream LLM analysis of the diarised transcript. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-speech-to-text-advanced.py` | Validate advanced-stt-config: provider supports requested capabilities, speaker_hint set if diarisation needed, vocab passed as param not in prompt. | Pre-commit + CI. |

## Related

- [[speech-to-text-basics]]
- [[openai-api-integration]]

## Decision tree

The tree at `content/06-decision-tree.xml` routes diarisation / streaming / vocabulary biasing needs to the provider that natively supports them. Walk it before wiring; using the wrong provider for diarisation means stitching speaker labels with heuristics that fail.
