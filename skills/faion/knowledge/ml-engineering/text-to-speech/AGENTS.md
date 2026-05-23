# Text-to-Speech

## Summary

**One-sentence:** Ship TTS by picking provider (latency / voice quality / cost), caching audio by text-hash, gating voice cloning behind explicit consent, and wiring a fallback for outage resilience.

**One-paragraph:** TTS provider choice spans 5× cost and 10× latency: OpenAI tts-1 ($15/M chars, ≈800ms first byte), ElevenLabs Turbo v2 ($0.18/1k chars, ≈400ms with streaming), Google Cloud (Chirp 3, $16/M, ≈600ms), Azure ($16/M, neural voices), Deepgram Aura ($0.135/1k, ≈200ms), local Coqui XTTS (free, GPU-bound). Cache audio output by text-hash because identical strings recur 40-70% in real traffic. Voice cloning requires consent record per voice. Streaming TTS to the user reduces perceived latency by ≈70%. Output: a `tts-config.yaml` declaring provider + voice + cache + fallback + consent.

**Ефективно для:**

- Voice agents та IVR — latency ≤500ms критичний; Deepgram Aura або ElevenLabs Turbo дають real-time.
- Audiobook / podcast generation — quality &gt; latency; ElevenLabs multilingual або Google Chirp 3 з 25+ голосами.
- Notifications / accessibility — кешуй; одна й та сама фраза перевикористовується 100×.
- Brand voice — voice cloning з консент-логом + ElevenLabs Voice Lab.

## Applies If (ALL must hold)

- Need to convert text → spoken audio in product flow
- Latency budget defined per use case (real-time vs batch)
- Voice quality requirements articulated (neural vs basic)

## Skip If (ANY kills it)

- Use case is dual-purpose (display text + read aloud); start with display text and add TTS later
- All target languages out of provider support
- Voice cloning required but no consent process exists — legal / ethics block

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `use-case-constraints.yaml` | YAML | latency, voice quality, cost cap |
| `voice-catalog.yaml` | YAML | provider voice IDs + language coverage |
| `consent-record.yaml` | YAML | per-voice consent metadata (cloning use) |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `speech-to-text` | Sibling in voice-agent stack |
| `cost-optimization` | Provider rate comparison |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: latency-bucket pick, voice consent, cache-by-hash, streaming for real-time, mandatory fallback | 1100 |
| `content/02-output-contract.xml` | essential | tts-config.yaml schema | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: no cache, cloning without consent, real-time on tts-1, hard-coded provider, missing language fallback | 900 |
| `content/04-procedure.xml` | essential | 5 steps: scope → bench → pick → cache+fallback → ship | 700 |
| `content/05-examples.xml` | essential | Worked example: voice agent with ElevenLabs Turbo + OpenAI fallback + Redis cache | 500 |
| `content/06-decision-tree.xml` | essential | Routes by latency + voice quality + cloning need | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `voice_quality_blind_test` | n/a (human) | Subjective |
| `provider_compare_drafting` | sonnet | Trade-offs |
| `tts_config_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/tts-cached.py` | TTS call with text-hash cache layer |
| `templates/chunk-text.py` | Long-text → sentence chunks for streamed TTS |
| `templates/tts-config.schema.yaml` | Schema for tts-config |
| `templates/_smoke-test.yaml` | Minimum-viable tts-config |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-text-to-speech.py` | Lint tts-config | Pre-commit |

## Related

- [[speech-to-text]] — paired in voice agents
- external: [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech) · [ElevenLabs](https://elevenlabs.io/) · [Deepgram Aura](https://deepgram.com/product/voice-ai)

## Decision tree

See `content/06-decision-tree.xml`. Routes by (a) latency budget, (b) voice-cloning need, (c) on-prem requirement → {Aura, ElevenLabs Turbo, OpenAI tts-1, Google Chirp, Coqui local}.
