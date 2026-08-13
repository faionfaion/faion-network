# Speech-to-Text Integration

## Summary

**One-sentence:** Picks an STT provider (OpenAI Whisper, GPT-4o Transcribe, AssemblyAI, Deepgram, ElevenLabs Scribe, faster-whisper local) by use case (batch vs streaming) and ships a typed transcription service with timestamps + diarization + custom vocab.

**One-paragraph:** Modern STT APIs differ 10-20× on latency (150 ms vs 5 s), accuracy (WER), language support (30-125 languages), and cost ($0.002-$0.04/min). Choosing wrong burns budget or misses accuracy. Real-time captioning needs ≤300ms latency (ElevenLabs Scribe, Deepgram); batch transcription tolerates seconds (Whisper); self-hosted faster-whisper breaks even at ≈500 hours/month. The pattern: declare use-case constraints → pick provider → wire typed `Transcript {text, segments[], speakers[]?, confidence}` → add custom-vocabulary boost where domain words matter → stream OR batch by SLO.

**Ефективно для:**

- Meeting / podcast / video indexing — batch Whisper або GPT-4o Transcribe з timestamps вистачає; цінник $0.003-0.006/min.
- Real-time captioning та voice commands — ElevenLabs Scribe (150ms) або Deepgram Nova (200ms).
- Industry-specific vocabulary (medical, legal, finance) — custom-vocab boost у Deepgram або AssemblyAI знижує WER 20-40%.
- High-volume (≥500h/month) — self-host faster-whisper економить 60-80% проти cloud.

## Applies If (ALL must hold)

- Feature requires turning audio into text (commands, captions, transcripts)
- Audio quality ≥ 8 kHz mono (lower → fix recording first, no provider fixes garbage in)
- Language is in the chosen provider's supported list

## Skip If (ANY kills it)

- Audio is synthetic TTS output — transcribe the source text instead
- Language not in any provider's list — bail, no point picking
- Cost prohibitive AND no GPU available for local — re-scope feature

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `use-case-constraints.yaml` | YAML | product/PM (real-time vs batch, max latency, WER target) |
| `audio-samples-eval/` | folder of WAV / MP3 | 30-min representative clip per language |
| `monthly-volume-hours.json` | JSON | finance / analytics estimate |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `text-to-speech` | Often paired in voice-agent stack |
| `cost-optimization` | Provider pricing comparison |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: latency-bucket provider pick, custom-vocab discipline, WER eval gate, self-host break-even, output schema | 1100 |
| `content/02-output-contract.xml` | essential | `stt-config.yaml` schema + `Transcript` JSON shape | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: real-time on Whisper, no custom vocab, no WER eval, hard-coded provider, missing diarization fallback | 900 |
| `content/04-procedure.xml` | essential | 5 steps: scope use case → bench providers → pick → wire fallback → ship + monitor | 700 |
| `content/05-examples.xml` | essential | Worked example: support-call transcription with Deepgram + custom medical vocab | 500 |
| `content/06-decision-tree.xml` | essential | Routes by latency + privacy + volume to provider | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audio_sample_bench` | n/a (deterministic) | WER computation |
| `provider_compare_drafting` | sonnet | Trade-off analysis |
| `stt_config_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/transcription-api.py` | OpenAI Whisper batch call with timestamps |
| `templates/transcription-service.py` | FastAPI service wrapping AssemblyAI streaming |
| `templates/stt-config.schema.yaml` | Schema for stt-config.yaml |
| `templates/_smoke-test.yaml` | Minimum-viable stt-config |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-speech-to-text.py` | Lint stt-config.yaml | Pre-commit |

## Related

- [[text-to-speech]] — paired in voice agents
- [[tool-use-function-calling]] — STT often feeds tool-calling LLM
- external: [OpenAI Whisper](https://platform.openai.com/docs/guides/speech-to-text) · [Deepgram Nova-2](https://deepgram.com/) · [AssemblyAI](https://www.assemblyai.com/) · [faster-whisper](https://github.com/SYSTRAN/faster-whisper)

## Decision tree

See `content/06-decision-tree.xml`. Branches by latency requirement, privacy, monthly volume → {Whisper batch, GPT-4o Transcribe, Deepgram, AssemblyAI, ElevenLabs Scribe, faster-whisper local}.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/transcription-api.py`

```python
"""
FastAPI transcription endpoint with sync and async (webhook) modes.
Requires: pip install fastapi python-multipart httpx

Run: uvicorn transcription_api:app --reload
"""

from __future__ import annotations

import os
import tempfile
import uuid
from pathlib import Path
from typing import Optional

import httpx
from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from transcription_service import TranscriptionConfig, TranscriptionProvider, TranscriptionService

app = FastAPI(title="Transcription API", version="1.0.0")

# Singleton service — primary: GPT-4o Mini, fallback: faster-whisper
_service = TranscriptionService(TranscriptionConfig(
    provider=TranscriptionProvider.OPENAI_GPT4O_MINI,
    fallback_provider=TranscriptionProvider.FASTER_WHISPER,
    word_timestamps=True,
))

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".webm", ".mp4"}


class TranscriptionResponse(BaseModel):
    success: bool
    text: Optional[str] = None
    segments: Optional[list] = None
    duration: Optional[float] = None
    fallback_used: Optional[bool] = None
    error: Optional[str] = None


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_sync(
    file: UploadFile = File(...),
    language: Optional[str] = None,
) -> TranscriptionResponse:
    """Synchronous transcription. Returns result immediately (use for files <5 min)."""
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported format {ext!r}. Allowed: {sorted(ALLOWED_EXTENSIONS)}")

    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        _service.config.language = language
        result = _service.transcribe(tmp_path)
        return TranscriptionResponse(**result)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@app.post("/transcribe/async")
async def transcribe_async(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    webhook_url: Optional[str] = None,
    language: Optional[str] = None,
) -> JSONResponse:
    """Async transcription. Returns job_id immediately; posts result to webhook_url when done."""
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {ext}")

    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    job_id = str(uuid.uuid4())
    background_tasks.add_task(_process_async, job_id, tmp_path, webhook_url, language)
    return JSONResponse({"job_id": job_id, "status": "queued"})


async def _process_async(job_id: str, file_path: str, webhook_url: str | None, language: str | None) -> None:
    """Background task: transcribe and deliver via webhook."""
    try:
        _service.config.language = language
        result = _service.transcribe(file_path)
        payload = {"job_id": job_id, "result": result}

        if webhook_url:
            async with httpx.AsyncClient(timeout=30) as client:
                await client.post(webhook_url, json=payload)
    finally:
        Path(file_path).unlink(missing_ok=True)
```

### `templates/transcription-service.py`

```python
"""
Production TranscriptionService: multi-provider support, fallback, large-file chunking.
Providers: OpenAI Whisper, GPT-4o Transcribe, GPT-4o Mini Transcribe,
           faster-whisper (local), AssemblyAI, Deepgram.

Usage:
    svc = TranscriptionService(TranscriptionConfig(
        provider=TranscriptionProvider.OPENAI_GPT4O_MINI,
        fallback_provider=TranscriptionProvider.FASTER_WHISPER,
        word_timestamps=True,
    ))
    result = svc.transcribe("meeting.mp3")
    print(result["text"])
"""

from __future__ import annotations

import logging
import os
import tempfile
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class TranscriptionProvider(Enum):
    OPENAI = "openai"
    OPENAI_GPT4O = "openai_gpt4o"
    OPENAI_GPT4O_MINI = "openai_gpt4o_mini"
    FASTER_WHISPER = "faster_whisper"
    ASSEMBLYAI = "assemblyai"
    DEEPGRAM = "deepgram"


@dataclass
class TranscriptionConfig:
    provider: TranscriptionProvider = TranscriptionProvider.OPENAI_GPT4O_MINI
    model_size: str = "large-v3-turbo"
    language: str | None = None
    word_timestamps: bool = False
    speaker_diarization: bool = False
    max_file_size_mb: int = 25
    fallback_provider: TranscriptionProvider | None = None
    supported_formats: list[str] = field(default_factory=lambda: [
        ".mp3", ".wav", ".m4a", ".flac", ".webm", ".mp4", ".ogg", ".opus"
    ])


class TranscriptionService:

    def __init__(self, config: TranscriptionConfig | None = None) -> None:
        self.config = config or TranscriptionConfig()
        self._init_provider(self.config.provider)

    def _init_provider(self, provider: TranscriptionProvider) -> None:
        if provider in (
            TranscriptionProvider.OPENAI,
            TranscriptionProvider.OPENAI_GPT4O,
            TranscriptionProvider.OPENAI_GPT4O_MINI,
        ):
            from openai import OpenAI  # noqa: PLC0415
            self.client = OpenAI()

        elif provider == TranscriptionProvider.FASTER_WHISPER:
            from faster_whisper import WhisperModel  # noqa: PLC0415
            self.model = WhisperModel(self.config.model_size, device="auto", compute_type="auto")

        elif provider == TranscriptionProvider.ASSEMBLYAI:
            import assemblyai as aai  # noqa: PLC0415
            aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
            self.transcriber = aai.Transcriber()

        elif provider == TranscriptionProvider.DEEPGRAM:
            from deepgram import DeepgramClient  # noqa: PLC0415
            self.dg_client = DeepgramClient(os.environ["DEEPGRAM_API_KEY"])

    def transcribe(self, audio_path: str | Path, **kwargs: Any) -> dict[str, Any]:
        """Transcribe audio with automatic fallback. Returns dict with 'text' key."""
        audio_path = Path(audio_path)
        if not audio_path.exists():
            return {"success": False, "error": f"File not found: {audio_path}"}
        if audio_path.suffix.lower() not in self.config.supported_formats:
            return {"success": False, "error": f"Unsupported format: {audio_path.suffix}"}

        size_mb = audio_path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_file_size_mb:
            return self._transcribe_chunked(audio_path)

        try:
            result = self._dispatch(audio_path, self.config.provider)
            return {"success": True, **result}
        except Exception as exc:
            logger.error("Primary provider failed: %s", exc)
            if self.config.fallback_provider:
                try:
                    self._init_provider(self.config.fallback_provider)
                    result = self._dispatch(audio_path, self.config.fallback_provider)
                    return {"success": True, "fallback_used": True, **result}
                except Exception as exc2:
                    logger.error("Fallback failed: %s", exc2)
            return {"success": False, "error": str(exc)}

    def _dispatch(self, path: Path, provider: TranscriptionProvider) -> dict[str, Any]:
        if provider == TranscriptionProvider.OPENAI:
            return self._openai(path, "whisper-1")
        elif provider == TranscriptionProvider.OPENAI_GPT4O:
            return self._openai(path, "gpt-4o-transcribe")
        elif provider == TranscriptionProvider.OPENAI_GPT4O_MINI:
            return self._openai(path, "gpt-4o-mini-transcribe")
        elif provider == TranscriptionProvider.FASTER_WHISPER:
            return self._faster_whisper(path)
        elif provider == TranscriptionProvider.ASSEMBLYAI:
            return self._assemblyai(path)
        elif provider == TranscriptionProvider.DEEPGRAM:
            return self._deepgram(path)
        raise ValueError(f"Unknown provider: {provider}")

    def _openai(self, path: Path, model: str) -> dict[str, Any]:
        fmt = "verbose_json" if self.config.word_timestamps else "json"
        with path.open("rb") as f:
            resp = self.client.audio.transcriptions.create(
                model=model,
                file=f,
                language=self.config.language,
                response_format=fmt,
                timestamp_granularities=["word", "segment"] if self.config.word_timestamps else None,
            )
        if fmt == "verbose_json":
            return {"text": resp.text, "segments": resp.segments, "duration": resp.duration, "provider": "openai", "model": model}
        return {"text": resp.text, "provider": "openai", "model": model}

    def _faster_whisper(self, path: Path) -> dict[str, Any]:
        segments, info = self.model.transcribe(
            str(path),
            language=self.config.language,
            word_timestamps=self.config.word_timestamps,
            vad_filter=True,
        )
        seg_list = []
        full_text = ""
        for seg in segments:
            seg_list.append({"start": seg.start, "end": seg.end, "text": seg.text})
            full_text += seg.text
        return {"text": full_text.strip(), "segments": seg_list, "language": info.language, "duration": info.duration, "provider": "faster_whisper"}

    def _assemblyai(self, path: Path) -> dict[str, Any]:
        import assemblyai as aai  # noqa: PLC0415
        cfg = aai.TranscriptionConfig(
            language_code=self.config.language,
            speaker_labels=self.config.speaker_diarization,
        )
        transcript = self.transcriber.transcribe(str(path), cfg)
        return {
            "text": transcript.text,
            "words": transcript.words,
            "utterances": transcript.utterances if self.config.speaker_diarization else None,
            "provider": "assemblyai",
        }

    def _deepgram(self, path: Path) -> dict[str, Any]:
        from deepgram import PrerecordedOptions  # noqa: PLC0415
        with path.open("rb") as f:
            source = {"buffer": f.read(), "mimetype": "audio/mp3"}
        options = PrerecordedOptions(
            model="nova-2",
            language=self.config.language or "en",
            smart_format=True,
            diarize=self.config.speaker_diarization,
        )
        resp = self.dg_client.listen.prerecorded.v("1").transcribe_file(source, options)
        alt = resp.results.channels[0].alternatives[0]
        return {"text": alt.transcript, "words": alt.words, "confidence": alt.confidence, "provider": "deepgram"}

    def _transcribe_chunked(self, path: Path) -> dict[str, Any]:
        """Handle files larger than max_file_size_mb via 5-minute chunks."""
        from pydub import AudioSegment  # noqa: PLC0415
        audio = AudioSegment.from_file(str(path))
        chunk_ms, overlap_ms = 5 * 60 * 1000, 5000
        chunks = []
        start = 0
        while start < len(audio):
            end = min(start + chunk_ms, len(audio))
            chunk = audio[start:end]
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                chunk.export(tmp.name, format="mp3")
                try:
                    res = self._dispatch(Path(tmp.name), self.config.provider)
                    chunks.append({"start_ms": start, "end_ms": end, "text": res["text"]})
                finally:
                    Path(tmp.name).unlink(missing_ok=True)
            start = end - overlap_ms

        return {"success": True, "text": " ".join(c["text"] for c in chunks), "chunks": chunks}
```

### `templates/stt-config.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [provider, model, mode, max_chunk_seconds, overlap_seconds, fallback]
properties:
  provider: { type: string, enum: [openai-whisper, openai-gpt4o, assemblyai, deepgram, elevenlabs-scribe, faster-whisper-local] }
  model: { type: string, minLength: 3 }
  mode: { type: string, enum: [batch, streaming] }
  max_chunk_seconds: { type: integer, minimum: 30, maximum: 600 }
  overlap_seconds: { type: integer, minimum: 0, maximum: 10 }
  diarization: { type: boolean }
  custom_vocab: { type: array, items: { type: string } }
  fallback:
    type: object
    required: [provider, trigger]
    properties:
      provider: { type: string }
      model: { type: string }
      trigger: { type: object }
```

### `templates/_smoke-test.yaml`

```yaml
provider: deepgram
model: nova-2
mode: streaming
max_chunk_seconds: 300
overlap_seconds: 5
diarization: true
custom_vocab: [ibuprofen, GERD]
fallback:
  provider: faster-whisper-local
  model: large-v3-turbo
  trigger: {consecutive_5xx: 3, timeout_seconds: 10}
```
