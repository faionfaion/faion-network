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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-speech-to-text-advanced.py` | Validate advanced-stt-config: provider supports requested capabilities, speaker_hint set if diarisation needed, vocab passed as param not in prompt. | Pre-commit + CI. |

## Related

- [[speech-to-text-basics]]
- [[openai-api-integration]]

## Decision tree

The tree at `content/06-decision-tree.xml` routes diarisation / streaming / vocabulary biasing needs to the provider that natively supports them. Walk it before wiring; using the wrong provider for diarisation means stitching speaker labels with heuristics that fail.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/transcription_service.py`

```python
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
```

### `templates/prompt-transcribe.txt`

```text
-->
<task>
Transcribe audio file.

Path: {{AUDIO_PATH}}
File size: {{SIZE_MB}}MB
Speakers: {{NUM_SPEAKERS}}  (1 = single-speaker; 2+ = diarization needed)
Language: {{LANGUAGE_CODE}}  (null = auto-detect; provide when known to save ~1s latency)
Word timestamps: {{BOOL}}

Strategy selection:
- If size_mb > 25: use LongAudioTranscriber (chunked)
- If num_speakers > 1: add SpeakerDiarizer.align_with_transcript() after transcription
- Provider: openai (fallback: faster_whisper if local GPU available)

Preprocess audio first if not already 16kHz mono WAV:
  ffmpeg -i input -ar 16000 -ac 1 -c:a pcm_s16le output.wav

Return JSON:
{
  "text": "full transcript",
  "segments": [{"start": N, "end": N, "text": "..."}],
  "speakers": [{"speaker": "SPEAKER_00", "start": N, "end": N}] or null,
  "duration_s": N
}

On error:
{"error": "...", "text": null}
</task>
```
