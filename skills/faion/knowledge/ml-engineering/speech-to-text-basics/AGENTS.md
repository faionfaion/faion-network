# Speech-to-Text Basics

## Summary

**One-sentence:** Produces a Whisper transcription integration — OpenAI API or local faster-whisper, language pin, verbose_json timestamps, 25MB pre-split, format guard.

**One-paragraph:** Whisper is the de-facto standard for multilingual transcription. The API is batch-only (no streaming) and has a 25 MB file-size cap, requiring upstream split via pydub for longer audio. Production wires: pin `language=` explicitly (saves ~200ms, prevents UK/RU or SR/HR misclassification), use `response_format="verbose_json"` + `timestamp_granularities=["segment"]` for downstream alignment, accept only the supported formats (MP3/MP4/MPEG/MPGA/M4A/WAV/WEBM — NOT FLAC/OGG), and route to local faster-whisper on GPU for high-volume (>10k hr/month) to break the API cost curve.

**Ефективно для:** інженера, що транскрибує podcasts / meetings / interviews і потребує детермінованої pipeline з timestamps + multilingual + cost-aware local fallback.

## Applies If (ALL must hold)

- Transcribing recorded audio (no streaming requirement).
- Source files in Whisper-supported formats (or convertible upstream).
- Latency tolerance ≥1s per call.
- Audio SNR sufficient (≥5 dB).

## Skip If (ANY kills it)

- Real-time streaming <300ms — use Deepgram / AssemblyAI WebSocket.
- Files >25 MB without upstream split — fix the split first.
- Extremely noisy audio (SNR <5 dB).
- High-volume (>10k hr/month) on the API — local faster-whisper is cheaper.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| OpenAI API key (or local faster-whisper install) | secret | secrets manager |
| Source audio in supported codec | MP3/M4A/WAV | content pipeline |
| Language code (BCP-47 or 2-letter) | string | content metadata |
| pydub for split | package | pyproject |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/multimodal-ai/speech-to-text-advanced` | Sibling: production patterns including speaker diarisation. |
| `geek/ai/llm-integration/openai-api-integration` | Baseline SDK setup. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: language pin, verbose_json + timestamps, format guard, 25MB split, local for high volume, no streaming. | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for stt-config: provider, language, format, timestamps. | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: no language, unsupported format, no split, streaming expectation, API for >10k hr. | ~700 |
| `content/04-procedure.xml` | medium | Steps: pick provider → check format → split if >25MB → transcribe with pinned lang → return verbose_json. | ~700 |
| `content/06-decision-tree.xml` | essential | Routes by volume + latency + privacy to API vs local faster-whisper. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `wire-api-call` | sonnet | Mechanical SDK call with params. |
| `pick-provider` | opus | Cost/latency/privacy reasoning. |
| `format-guard` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/whisper-api.py` | OpenAI Whisper API with verbose_json + language pin. |
| `templates/faster-whisper.py` | Local faster-whisper (CTranslate2) for cost-sensitive high-volume. |
| `templates/split-audio.py` | pydub-based split helper for >25MB inputs. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-speech-to-text-basics.py` | Validate stt-config: provider, language, format, timestamps enabled. | Pre-commit + CI. |

## Related

- [[speech-to-text-advanced]]
- [[openai-api-integration]]

## Decision tree

The tree at `content/06-decision-tree.xml` routes: privacy / volume / latency drive API vs local. Walk it before wiring the SDK so the cost-curve break (>10k hr/month) doesn't catch you off-guard.
