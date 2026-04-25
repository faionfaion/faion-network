# Agent Integration — Text-to-Speech Implementation

## When to use
- Production TTS service with caching, retry, and multi-provider support
- Long-form content (articles, podcast episodes) that exceeds 4096-char API limits
- Real-time streaming TTS to a speaker or WebSocket client
- Voice cloning from audio samples (ElevenLabs)
- Multilingual TTS where Google Neural2 voices outperform OpenAI on specific languages

## When NOT to use
- Simple one-off audio generation — use `tts-basics` direct API call; `TTSService` adds unnecessary setup overhead
- Voice cloning of persons without explicit consent — ElevenLabs ToS requires consent documentation
- Sub-200ms first-audio-byte latency — streaming helps but not enough for truly real-time telephony (<50ms)
- Languages not covered by OpenAI TTS (limited to ~50 languages) — use Google or Azure for broader coverage

## Where it fails / limitations
- `LongTextTTS._split_text` splits on sentence boundaries — fails for text with no sentence-ending punctuation (code blocks, lists); produces one giant chunk that may exceed API limit
- `stream_tts` uses `async with ... with_streaming_response.create()` — sync wrapper `stream_to_speaker` must be awaited; calling it from sync context requires `asyncio.run()`
- `TTSService._synthesize_long` stubs only OpenAI provider; ElevenLabs and Google long-text paths are not implemented
- ElevenLabs `clone_voice` takes file paths not file handles — paths must be absolute and files must be .mp3/.wav ≥30s each (3 samples recommended)
- `TTSService._get_duration` silently returns 0.0 on any pydub exception — invalid audio files appear to have 0-second duration rather than raising
- Google TTS `voice_name` format is locale-specific (`en-US-Neural2-D`) — picking wrong locale for a given language code silently generates wrong accent
- Cached audio files are never evicted — disk fills up over time in long-running production services

## Agentic workflow
An agent receives text, voice parameters, and an output path. It calls `TTSService.synthesize()` which handles caching, length validation, and chunking transparently. For streaming use cases, an agent calls `stream_tts()` as an async generator and forwards bytes to a WebSocket or audio output stream. For voice cloning pipelines, a prep agent validates and uploads sample audio, calls `clone_voice`, stores the returned `voice_id`, then uses it in subsequent `elevenlabs_tts` calls.

### Recommended subagents
- `haiku` — Execute `TTSService.synthesize()`: receive text + params, return `{success, path, duration, cached}`
- `haiku` — Streaming audio delivery: call `stream_tts()`, chunk bytes to WebSocket or pyaudio stream
- `sonnet` — Long text preprocessing: split into chapters/sections, generate per-section audio, assemble with chapter markers
- `sonnet` — Voice clone setup: validate sample files (duration, format, quality), call `clone_voice`, register voice_id in config

### Prompt pattern
```xml
<task>
Synthesize speech for production use.
Text length: {{CHAR_COUNT}} chars
Provider: {{PROVIDER}}  (openai|elevenlabs|google)
Voice: {{VOICE_ID_OR_NAME}}
Speed: {{SPEED}}
Output: {{OUTPUT_PATH}}
Cache: enabled

Use TTSService. If text > 4000 chars, chunking is automatic.
Return: {"success": true, "path": "...", "duration": N, "cached": false}
</task>
```

```python
# Streaming TTS to WebSocket (agent pattern)
async def ws_tts_handler(websocket, text: str, voice: str = "alloy"):
    async for chunk in stream_tts(text, voice=voice):
        await websocket.send_bytes(chunk)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| openai (Python SDK) | OpenAI TTS, streaming | `pip install openai` |
| elevenlabs | ElevenLabs TTS + voice cloning | `pip install elevenlabs` |
| google-cloud-texttospeech | Google Neural2 voices | `pip install google-cloud-texttospeech` |
| pydub | Long audio assembly, duration check | `pip install pydub` |
| pyaudio | Direct speaker output | `pip install pyaudio` (requires portaudio) |
| fastapi + websockets | WebSocket TTS server | `pip install fastapi websockets uvicorn` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI TTS | SaaS | Yes — Python SDK | tts-1/tts-1-hd; streaming PCM; no SSML; best for English |
| ElevenLabs | SaaS | Yes — Python SDK | Voice cloning; multilingual; `eleven_multilingual_v2`; best quality overall |
| Google Cloud TTS | SaaS | Yes — Python SDK | SSML; Neural2 + Studio; 400+ voices; best multilingual breadth |
| Azure Cognitive Services TTS | SaaS | Yes — REST SDK | SSML; neural voices; good latency in EU regions |
| AWS Polly | SaaS | Yes — boto3 | Neural voices; SSML; async synthesis for long text via S3 |
| Coqui TTS | OSS | Yes — Python | Self-hosted; supports XTTS for cloning; GPU recommended |
| Kokoro | OSS | Yes — local | 80MB model; CPU-viable; MIT license; English-focused |

## Templates & scripts
See `templates.md` for `TTSService`, `LongTextTTS`, `stream_tts`, `elevenlabs_tts`, `google_tts`.

Inline: cache eviction (15 lines — production necessity):
```python
import os, time
from pathlib import Path

def evict_tts_cache(cache_dir: str, max_age_days: int = 30, max_size_mb: int = 500):
    """Evict old cache entries by age or total size limit."""
    cache = Path(cache_dir)
    entries = sorted(cache.glob("*.mp3"), key=lambda p: p.stat().st_mtime)
    total_mb = sum(p.stat().st_size for p in entries) / (1024 * 1024)
    now = time.time()
    for entry in entries:
        age_days = (now - entry.stat().st_mtime) / 86400
        if age_days > max_age_days or total_mb > max_size_mb:
            total_mb -= entry.stat().st_size / (1024 * 1024)
            entry.unlink()
```

## Best practices
- Use content-hash caching at the service level — identical text+voice+speed combos are common in pipelines; caching cuts costs significantly
- For long content: split on semantic boundaries (paragraphs, headings), not arbitrary character counts; chapter-level splits produce more natural prosody than mid-sentence splits
- Use `response_format="pcm"` for streaming to reduce decode overhead in the playback chain
- Implement cache eviction by age and total size — production services accumulate gigabytes of cached audio over time
- For ElevenLabs voice cloning: collect 3+ audio samples of 30–60s each in the target voice; minimize background noise; normalize audio levels before uploading
- Test streaming latency by measuring time-to-first-byte; OpenAI streaming typically delivers first chunk in 200–400ms
- Log provider, voice, character count, and cached status for every synthesis call to track costs and debug quality issues

## AI-agent gotchas
- `stream_tts` is an async generator — agents calling it in a sync context must use `asyncio.run(collect_stream(text))` wrapper; direct iteration in sync code raises TypeError
- `pyaudio` requires `portaudio` system library — install fails silently in some container images; check at import, not at runtime
- ElevenLabs `clone_voice` call is slow (10–30s for upload + processing) — agents must not treat it as a fast operation; run once and cache the `voice_id`
- `LongTextTTS` temp files use predictable paths (`/tmp/chunk_0.mp3`, etc.) — concurrent agent instances will overwrite each other's chunks; use `tempfile.mkdtemp()` instead
- Google TTS `speaking_rate` range is 0.25–4.0 but quality degrades noticeably above 1.5 — agents should cap at 1.3 for production
- `TTSService._synthesize_long` returns a dict but the path key is `"path"` not `"audio_path"` — callers must handle both return shapes from `synthesize()`
- Cache key includes provider value via `self.config.provider.value` — switching providers invalidates the entire cache even for identical text+voice combos; document this behavior

## References
- https://platform.openai.com/docs/guides/text-to-speech
- https://platform.openai.com/docs/api-reference/audio/createSpeech
- https://elevenlabs.io/docs/api-reference/text-to-speech
- https://elevenlabs.io/docs/voices/voice-lab/instant-voice-cloning
- https://cloud.google.com/text-to-speech/docs
- https://github.com/coqui-ai/TTS
- https://github.com/hexgrad/kokoro
