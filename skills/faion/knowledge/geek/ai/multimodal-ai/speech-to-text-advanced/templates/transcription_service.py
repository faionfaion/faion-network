"""
Production transcription service: OpenAI Whisper, LongAudioTranscriber, SpeakerDiarizer.
All known template bugs are fixed here.
"""
from __future__ import annotations

import logging
import tempfile
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from openai import OpenAI
from pydub import AudioSegment


class TranscriptionProvider(Enum):
    OPENAI = "openai"
    FASTER_WHISPER = "faster_whisper"
    LOCAL = "local"


@dataclass
class TranscriptionConfig:
    provider: TranscriptionProvider = TranscriptionProvider.OPENAI
    model_size: str = "base"
    language: str | None = None
    word_timestamps: bool = False
    speaker_diarization: bool = False
    max_file_size_mb: int = 25
    supported_formats: list[str] = field(
        default_factory=lambda: [".mp3", ".wav", ".m4a", ".flac", ".webm", ".mp4", ".ogg"]
    )


class LongAudioTranscriber:
    """Chunk-and-merge for audio files exceeding the 25MB Whisper API limit."""

    def __init__(self, chunk_duration_ms: int = 300_000, overlap_ms: int = 3_000):
        self.chunk_duration = chunk_duration_ms
        self.overlap = overlap_ms
        self.client = OpenAI()

    def transcribe(self, audio_path: str) -> dict[str, Any]:
        audio = AudioSegment.from_file(audio_path)
        if len(audio) <= self.chunk_duration:
            return {"text": self._transcribe_chunk(audio_path)}
        return self._merge_results(self._process_chunks(audio))

    def _process_chunks(self, audio: AudioSegment) -> list[dict]:
        results = []
        start = 0
        tmpdir = tempfile.mkdtemp()  # unique dir — safe for concurrent callers
        while start < len(audio):
            end = min(start + self.chunk_duration, len(audio))
            chunk_path = str(Path(tmpdir) / f"chunk_{start}.mp3")
            audio[start:end].export(chunk_path, format="mp3")
            results.append({"start": start, "end": end, "text": self._transcribe_chunk(chunk_path)})
            Path(chunk_path).unlink()
            start = end - self.overlap
        return results

    def _transcribe_chunk(self, audio_path: str) -> str:
        with open(audio_path, "rb") as f:
            response = self.client.audio.transcriptions.create(model="whisper-1", file=f)
        return response.text  # BUG FIX: was return response (object not string)

    def _merge_results(self, results: list[dict]) -> dict:
        full_text = " ".join(r["text"] for r in results)
        return {"text": full_text, "chunks": results}


class SpeakerDiarizer:
    """Speaker diarization via pyannote 3.1. Requires GPU and HuggingFace token."""

    def __init__(self, hf_token: str):
        import torch
        from pyannote.audio import Pipeline

        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token,
        )
        if not torch.cuda.is_available():
            raise RuntimeError("GPU required for production diarization. pyannote on CPU is ~10x real-time.")
        self.pipeline.to("cuda")

    def diarize(self, audio_path: str, num_speakers: int | None = None) -> list[dict]:
        kwargs = {"num_speakers": num_speakers} if num_speakers else {}
        diarization = self.pipeline(audio_path, **kwargs)
        return [
            {"speaker": spk, "start": turn.start, "end": turn.end}
            for turn, _, spk in diarization.itertracks(yield_label=True)
        ]

    def align_with_transcript(self, audio_path: str, segments: list[dict]) -> list[dict]:
        speaker_segs = self.diarize(audio_path)
        for seg in segments:
            mid = (seg["start"] + seg["end"]) / 2
            seg["speaker"] = "UNKNOWN"
            for sp in speaker_segs:
                # boundary check: ensure mid is strictly inside the segment
                if sp["start"] < mid < sp["end"]:
                    seg["speaker"] = sp["speaker"]
                    break
        return segments


class TranscriptionService:
    """Production STT service with provider routing and file validation."""

    def __init__(self, config: TranscriptionConfig | None = None):
        self.config = config or TranscriptionConfig()
        self.logger = logging.getLogger(__name__)
        if self.config.provider == TranscriptionProvider.OPENAI:
            self.client = OpenAI()

    def transcribe(self, audio_path: str | Path, **kwargs) -> dict[str, Any]:
        audio_path = Path(audio_path)
        if not audio_path.exists():
            return {"success": False, "error": f"File not found: {audio_path}"}
        if audio_path.suffix.lower() not in self.config.supported_formats:
            return {"success": False, "error": f"Unsupported format: {audio_path.suffix}. Convert to mp3/wav first."}
        size_mb = audio_path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_file_size_mb:
            self.logger.info(f"Large file ({size_mb:.1f}MB) — using chunked processing")
            result = LongAudioTranscriber().transcribe(str(audio_path))
            return {"success": True, **result}
        try:
            return {"success": True, **self._transcribe_openai(audio_path)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _transcribe_openai(self, audio_path: Path) -> dict:
        response_format = "verbose_json" if self.config.word_timestamps else "json"
        with open(audio_path, "rb") as f:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=self.config.language,
                response_format=response_format,
                timestamp_granularities=(["word", "segment"] if self.config.word_timestamps else None),
            )
        if response_format == "verbose_json":
            words = getattr(response, "words", None)
            if words is None and self.config.word_timestamps:
                self.logger.warning("word_timestamps requested but response.words is None")
            return {"text": response.text, "segments": response.segments, "words": words, "duration": response.duration}
        return {"text": response.text}
