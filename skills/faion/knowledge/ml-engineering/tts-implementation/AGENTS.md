# Text-to-Speech Implementation

## Summary

**One-sentence:** Wraps single-call TTS into a production service: cache eviction, LongTextTTS chunking, async PCM streaming, ElevenLabs voice cloning behind a consent gate.

**One-paragraph:** TTSService centralises multi-provider TTS (OpenAI, ElevenLabs, Google Cloud) behind a unified synthesize() entry point with sha256-keyed cache including provider in the key, eviction by age + total size, transparent LongTextTTS chunking for payloads &gt; 4000 chars, async generator streaming for sub-second first-byte delivery, and consent-validated ElevenLabs clone_voice. Replaces direct provider calls from `tts-basics` once a pipeline produces long-form, multi-tenant, or streamed audio. Output is the standard contract from `tts-basics` plus a `chunks` array for assembled long-form audio.

**Ефективно для:** інженера AI-конвеєра, що збирає подкасти / епізоди / WebSocket-стрім — закриває петлю між draft-TTS і прод-нагрузкою з обмеженням бюджету та консент-аудитом.

## Applies If (ALL must hold)

- Payload is long-form (article, podcast episode, book chapter) exceeding the 4000-char single-call cap.
- Pipeline runs multiple synthesize calls per minute and needs sha256 cache + eviction.
- Real-time streaming TTS (WebSocket, pyaudio speaker) is required, not just file delivery.
- Voice cloning via ElevenLabs is on the roadmap and a consent-record store exists.
- The agent operates in an async context (FastAPI, LiveKit, Daily) or controls a multi-worker pool.

## Skip If (ANY kills it)

- Single one-off audio generation — use `tts-basics` directly; TTSService setup adds overhead.
- Voice cloning without a stored consent record naming the speaker — ElevenLabs ToS blocker, hard stop.
- Sub-200ms first-byte latency in telephony — even streaming PCM cannot reach below ~50ms.
- Languages not covered by OpenAI TTS (≤16 supported) — use Google Cloud or Azure TTS directly.
- No async runtime available — TTSService streaming requires asyncio; the sync path still works but loses the latency benefit.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Long-form text | UTF-8 string (≥4000 chars allowed) | upstream LLM / CMS |
| TTSConfig | dataclass: provider, voice, model, cache_dir, max_age_days, max_size_mb | pipeline config loader |
| Provider credentials | env: `OPENAI_API_KEY`, `ELEVEN_API_KEY`, `GOOGLE_APPLICATION_CREDENTIALS` | secrets manager |
| Consent record (clone path only) | JSON: `{speaker_id, signed_at, scope, sample_paths[]}` | consent store / ledger |
| pydub + ffmpeg installed | apt / brew | host setup |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/multimodal-ai/tts-basics` | core preprocess, voice-map, single-call cache key — TTSService builds on these. |
| `geek/ai/multimodal-ai/voice-implementation` | downstream consumer when TTSService output feeds a duplex voice agent. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: provider in cache key, eviction by age+size, tempfile.mkdtemp for chunks, semantic split, async stream, clone consent | ~1000 |
| `content/02-output-contract.xml` | essential | TTSService.synthesize() schema + chunks[] for assembled long-form + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: predictable /tmp paths, regex split on code blocks, sync stream_to_file in async, missing duration check, clone without consent | ~900 |
| `content/04-procedure.xml` | deep | 8-step procedure: probe cache → check length → chunk on semantic boundaries → parallel synth → assemble → measure → log → evict | ~900 |
| `content/05-examples.xml` | medium | Worked podcast-episode synthesis: 18000-char article → 5 chunks → assembled mp3 | ~600 |
| `content/06-decision-tree.xml` | essential | Routing: short vs long, cache hit vs miss, stream vs file, clone vs library voice | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `chunk-long-text` | sonnet | Semantic boundary detection: paragraphs, headings, sentence groups. |
| `assemble-chunks` | haiku | pydub concat with silence padding; mechanical. |
| `select-provider` | sonnet | Decision-tree walk: language, voice clone, cost cap, SSML. |
| `validate-consent` | sonnet | Compare consent scope to requested clone use; gate the call. |
| `synthesize-chunk` | haiku | Single API call per chunk; mechanical. |
| `evict-cache` | haiku | LRU + size + age scan; mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tts_service.py` | TTSService + TTSConfig + cache eviction by age + total size. |
| `templates/long_text_tts.py` | LongTextTTS with semantic split + tempfile.mkdtemp() for concurrent agent safety. |
| `templates/stream_tts.py` | stream_tts() async generator + WebSocket forwarder pattern. |
| `templates/elevenlabs_tts.py` | elevenlabs_tts() + clone_voice() gated on consent record. |
| `templates/prompt-tts-prod.txt` | Agent task prompt for production TTS with cache semantics. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tts-implementation.py` | Validate TTSService output JSON (long-form with chunks[]) against 02-output-contract. | Post-synthesize, before downstream consumes. |

## Related

- [[tts-basics]] — single-call layer this service builds on.
- [[voice-implementation]] — duplex voice agent that consumes TTSService streaming output.
- [[multimodal-ai/voice-basics]] — turn-based STT→LLM→TTS pipeline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks: payload length (short → tts-basics; long → chunk path), cache state (hit → return cached chunks; miss → synth), delivery mode (file → save to cache_dir; stream → async generator), voice mode (library → standard call; clone → consent gate then ElevenLabs). Use it at the synthesize() entry point of TTSService before any provider call.
