# purpose: production TranscriptionService with multi-provider + fallback + large-file chunking
# consumes: audio bytes + provider config
# produces: code (drop-in service wrapping STT providers)
# depends-on: provider SDKs (openai, assemblyai, deepgram, faster-whisper), pydantic
# token-budget-impact: ~800 tokens if loaded into LLM context
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
