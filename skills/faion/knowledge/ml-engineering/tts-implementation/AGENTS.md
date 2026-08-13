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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tts_service.py`

```python
"""Production TTSService with SHA-256 caching, provider routing, eviction."""
from __future__ import annotations

import hashlib
import logging
import shutil
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from openai import OpenAI


class TTSProvider(Enum):
    OPENAI = "openai"
    ELEVENLABS = "elevenlabs"
    GOOGLE = "google"


@dataclass
class TTSConfig:
    provider: TTSProvider = TTSProvider.OPENAI
    default_voice: str = "alloy"
    default_speed: float = 1.0
    output_format: str = "mp3"
    cache_enabled: bool = True
    cache_dir: str = "./tts_cache"
    max_text_length: int = 4000  # 4000 not 4096 — avoid off-by-one truncation


class TTSService:
    """Production text-to-speech service with caching and long-text handling."""

    def __init__(self, config: TTSConfig | None = None):
        self.config = config or TTSConfig()
        self.logger = logging.getLogger(__name__)
        if self.config.cache_enabled:
            Path(self.config.cache_dir).mkdir(parents=True, exist_ok=True)
        if self.config.provider == TTSProvider.OPENAI:
            self.client = OpenAI()

    def synthesize(
        self,
        text: str,
        output_path: str | None = None,
        voice: str | None = None,
        speed: float | None = None,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        """Synthesize speech. Returns {"success", "path", "duration", "cached"}."""
        voice = voice or self.config.default_voice
        speed = speed or self.config.default_speed
        if use_cache and self.config.cache_enabled:
            cached = self._get_cached(text, voice, speed)
            if cached:
                return {"success": True, "path": cached, "cached": True, "duration": self._get_duration(cached)}
        if len(text) > self.config.max_text_length:
            return self._synthesize_long(text, output_path, voice, speed)
        try:
            path = self._synthesize_openai(text, output_path, voice, speed)
            if self.config.cache_enabled:
                self._cache_audio(text, voice, speed, path)
            return {"success": True, "path": path, "cached": False, "duration": self._get_duration(path)}
        except Exception as e:
            return {"success": False, "error": str(e), "path": None}

    def _synthesize_openai(self, text: str, output_path: str | None, voice: str, speed: float) -> str:
        response = self.client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text,
            speed=speed,
            response_format=self.config.output_format,
        )
        output_path = output_path or f"/tmp/tts_{hashlib.md5(text.encode()).hexdigest()}.{self.config.output_format}"
        response.stream_to_file(output_path)
        return output_path

    def _synthesize_long(self, text: str, output_path: str | None, voice: str, speed: float) -> dict:
        from tts_implementation.templates.long_text_tts import LongTextTTS
        processor = LongTextTTS(max_chars=self.config.max_text_length)
        output_path = output_path or f"/tmp/tts_long_{hashlib.md5(text.encode()).hexdigest()}.mp3"
        result_path = processor.synthesize(text, output_path, voice)
        return {"success": True, "path": result_path, "cached": False, "duration": self._get_duration(result_path)}

    def _get_cache_key(self, text: str, voice: str, speed: float) -> str:
        content = f"{text}|{voice}|{speed}|{self.config.provider.value}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _get_cached(self, text: str, voice: str, speed: float) -> str | None:
        path = Path(self.config.cache_dir) / f"{self._get_cache_key(text, voice, speed)}.{self.config.output_format}"
        return str(path) if path.exists() else None

    def _cache_audio(self, text: str, voice: str, speed: float, audio_path: str) -> None:
        key = self._get_cache_key(text, voice, speed)
        shutil.copy(audio_path, Path(self.config.cache_dir) / f"{key}.{self.config.output_format}")

    def _get_duration(self, audio_path: str) -> float:
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0
        except Exception:
            return 0.0  # callers must treat 0.0 as an error indicator


def evict_tts_cache(cache_dir: str, max_age_days: int = 30, max_size_mb: int = 500) -> int:
    """Evict old cache entries by age or total size limit. Returns number of files deleted."""
    cache = Path(cache_dir)
    entries = sorted(cache.glob("*.mp3"), key=lambda p: p.stat().st_mtime)
    total_mb = sum(p.stat().st_size for p in entries) / (1024 * 1024)
    now, deleted = time.time(), 0
    for entry in entries:
        if (now - entry.stat().st_mtime) / 86400 > max_age_days or total_mb > max_size_mb:
            total_mb -= entry.stat().st_size / (1024 * 1024)
            entry.unlink()
            deleted += 1
    return deleted
```

### `templates/long_text_tts.py`

```python
"""LongTextTTS: chunk long text at sentence boundaries with mkdtemp isolation."""
from __future__ import annotations

import re
import shutil
import tempfile
from pathlib import Path

from openai import OpenAI
from pydub import AudioSegment


class LongTextTTS:
    """Handle text exceeding the 4000-char OpenAI TTS limit."""

    def __init__(self, max_chars: int = 4000):
        self.max_chars = max_chars
        self.client = OpenAI()

    def synthesize(self, text: str, output_path: str, voice: str = "alloy") -> str:
        """Synthesize long text with automatic sentence-boundary chunking."""
        chunks = self._split_text(text)
        if not chunks:
            raise ValueError("Text produced no chunks after splitting")
        tmpdir = tempfile.mkdtemp()  # unique per call — safe for concurrent agents
        try:
            segments = []
            for i, chunk in enumerate(chunks):
                chunk_path = str(Path(tmpdir) / f"chunk_{i}.mp3")
                response = self.client.audio.speech.create(
                    model="tts-1",
                    voice=voice,
                    input=chunk,
                )
                response.stream_to_file(chunk_path)
                segments.append(AudioSegment.from_mp3(chunk_path))
            combined = segments[0]
            for seg in segments[1:]:
                combined += seg
            combined.export(output_path, format="mp3")
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
        return output_path

    def _split_text(self, text: str) -> list[str]:
        """
        Split text at sentence boundaries.
        WARNING: text with no sentence-ending punctuation (code, lists, data)
        produces a single chunk that may exceed max_chars. Pre-process such text.
        """
        chunks: list[str] = []
        current = ""
        for sentence in re.split(r'(?<=[.!?])\s+', text):
            if len(current) + len(sentence) <= self.max_chars:
                current += sentence + " "
            else:
                if current:
                    chunks.append(current.strip())
                current = sentence + " "
        if current:
            chunks.append(current.strip())
        return chunks
```

### `templates/stream_tts.py`

```python
"""Async TTS streaming: stream_tts generator + pyaudio + WebSocket forwarders."""
from __future__ import annotations

from typing import AsyncGenerator

from openai import AsyncOpenAI


async def stream_tts(text: str, voice: str = "alloy") -> AsyncGenerator[bytes, None]:
    """
    Stream TTS audio as PCM bytes.
    Must be called from async context. In sync context:
        audio = asyncio.run(collect_stream(text))
    """
    client = AsyncOpenAI()
    async with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="pcm",
    ) as response:
        async for chunk in response.iter_bytes():
            yield chunk


async def collect_stream(text: str, voice: str = "alloy") -> bytes:
    """Collect all stream chunks into a single bytes object (sync-friendly wrapper)."""
    return b"".join([chunk async for chunk in stream_tts(text, voice=voice)])


async def stream_to_speaker(text: str, voice: str = "alloy") -> None:
    """
    Stream TTS directly to speakers via pyaudio.
    Requires: pip install pyaudio && apt install portaudio19-dev
    PCM format: paInt16, 1 channel, 24000 Hz (matches OpenAI PCM output).
    """
    try:
        import pyaudio
    except ImportError as e:
        raise ImportError("pyaudio not installed. Run: pip install pyaudio (requires portaudio)") from e

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=24_000, output=True)
    try:
        async for chunk in stream_tts(text, voice=voice):
            stream.write(chunk)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


async def ws_tts_handler(websocket: object, text: str, voice: str = "alloy") -> None:
    """Forward TTS stream to a WebSocket client."""
    async for chunk in stream_tts(text, voice=voice):
        await websocket.send_bytes(chunk)  # type: ignore[attr-defined]
```

### `templates/elevenlabs_tts.py`

```python
"""ElevenLabs TTS + voice cloning. Cloning requires consent record (rule r6)."""
from __future__ import annotations

import os

from elevenlabs import ElevenLabs, Voice, VoiceSettings


def elevenlabs_tts(
    text: str,
    output_path: str,
    voice_id: str,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    model: str = "eleven_multilingual_v2",
) -> str:
    """
    Generate speech using ElevenLabs.
    voice_id: use a built-in voice ID or one returned by clone_voice().
    stability: 0.0-1.0 (lower = more variable/expressive)
    similarity_boost: 0.0-1.0 (higher = closer to original voice)
    """
    client = ElevenLabs()
    audio = client.generate(
        text=text,
        voice=Voice(
            voice_id=voice_id,
            settings=VoiceSettings(
                stability=stability,
                similarity_boost=similarity_boost,
                style=0.5,
                use_speaker_boost=True,
            ),
        ),
        model=model,
    )
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    return output_path


def clone_voice(audio_sample_paths: list[str], name: str, description: str = "") -> str:
    """
    Clone a voice from audio samples. Returns voice_id for use in elevenlabs_tts().
    audio_sample_paths: list of ABSOLUTE paths to .mp3 or .wav files, each >= 30 seconds.
    Recommended: 3 samples of 30-60s each, minimal background noise, normalized levels.
    SLOW: 10-30 seconds per call. Call once and cache the returned voice_id.
    """
    for path in audio_sample_paths:
        if not os.path.isabs(path):
            raise ValueError(f"clone_voice requires absolute paths, got: {path}")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Sample file not found: {path}")
    client = ElevenLabs()
    voice = client.clone(name=name, description=description, files=audio_sample_paths)
    return voice.voice_id
```

### `templates/prompt-tts-prod.txt`

```text
<task>
Synthesize speech for production use.

Text length: {{CHAR_COUNT}} chars
Provider: {{PROVIDER}}  (openai|elevenlabs|google)
Voice: {{VOICE_ID_OR_TYPE}}  (provider voice ID or semantic type: news|assistant|narrator|neutral)
Speed: {{SPEED}}  (0.25-4.0, default 1.0)
Output path: {{OUTPUT_PATH}}
Cache: enabled

Use TTSService. If text > 4000 chars, chunking is automatic.
If provider is elevenlabs with a cloned voice, ensure voice_id is pre-registered (do NOT call clone_voice here).

Return JSON:
{
  "success": true,
  "path": "...",
  "duration": N,
  "cached": false
}

On error:
{
  "success": false,
  "error": "...",
  "path": null
}

Notes:
- duration = 0.0 means generation may have failed — treat as error
- "path" key is always "path", never "audio_path"
</task>
```
