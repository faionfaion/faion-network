# Text-to-Speech Implementation

## Summary

Production TTS service with multi-provider support (OpenAI, ElevenLabs, Google Cloud), content-hash
caching, long-text chunking via `LongTextTTS`, real-time streaming via async PCM, and voice cloning
via ElevenLabs. Use when `tts-basics` patterns are insufficient — this layer adds `TTSService`,
cache eviction, and streaming delivery.

## Why

Single-call TTS fails for pipeline audio generation: no caching means repeated phrases re-bill on
every pipeline run, no chunking means articles and episodes error out at 4096 chars, no streaming
means high-latency first-audio delivery. `TTSService` centralizes these concerns with SHA-256 content
hashing, transparent chunking, and async generator streaming.

## When To Use

- Long-form content (articles, podcast episodes) exceeding 4096-char API limits.
- Production TTS service needing content-hash caching, retry, and multi-provider support.
- Real-time streaming TTS to a speaker or WebSocket client.
- Voice cloning from audio samples via ElevenLabs.
- Multilingual synthesis where Google Neural2 outperforms OpenAI on specific languages.

## When NOT To Use

- Simple one-off audio generation — use `tts-basics` direct API call; `TTSService` setup adds overhead.
- Voice cloning of persons without explicit consent — ElevenLabs ToS requires consent documentation.
- Sub-200ms first-audio-byte latency in telephony — streaming helps but cannot reach <50ms.
- Languages not covered by OpenAI TTS — use Google Cloud or Azure TTS directly.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tts-service.xml` | `TTSService` architecture, caching design, provider init, known return-shape inconsistency. |
| `content/02-long-text.xml` | `LongTextTTS` chunking logic, sentence-boundary splitting limitation, temp-file collision fix. |
| `content/03-streaming.xml` | `stream_tts` async generator, `stream_to_speaker` pyaudio pattern, WebSocket delivery. |
| `content/04-elevenlabs.xml` | `elevenlabs_tts`, `clone_voice`, voice settings, sample requirements, gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tts_service.py` | `TTSService`, `TTSConfig`, `TTSProvider` with cache eviction included. |
| `templates/long_text_tts.py` | `LongTextTTS` with `tempfile.mkdtemp()` fix for concurrent agent safety. |
| `templates/stream_tts.py` | `stream_tts` async generator + WebSocket handler pattern. |
| `templates/elevenlabs_tts.py` | `elevenlabs_tts` + `clone_voice` with sample validation. |
| `templates/prompt-tts-prod.txt` | Agent task prompt for production TTS synthesis with cache semantics. |
