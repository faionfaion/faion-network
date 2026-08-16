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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-speech-to-text-basics.py` | Validate stt-config: provider, language, format, timestamps enabled. | Pre-commit + CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[speech-to-text-advanced]]
- [[openai-api-integration]]

## Decision tree

The tree at `content/06-decision-tree.xml` routes: privacy / volume / latency drive API vs local. Walk it before wiring the SDK so the cost-curve break (>10k hr/month) doesn't catch you off-guard.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/whisper-api.py`

```python
"""
from openai import OpenAI

client = OpenAI()


def transcribe_audio(audio_path: str, language: str = "en",
                     response_format: str = "text",
                     prompt: str = None) -> str:
    """
    Transcribe audio using Whisper API.
    language: ISO-639-1 code (e.g., "en", "uk", "es"). Always specify explicitly.
    response_format: "text" | "json" | "verbose_json" | "srt" | "vtt"
    prompt: domain terms, speaker names — keep under 100 tokens.
    """
    kwargs = {
        "model": "whisper-1",
        "language": language,
        "response_format": response_format,
    }
    if prompt:
        kwargs["prompt"] = prompt
    with open(audio_path, "rb") as audio_file:
        kwargs["file"] = audio_file
        response = client.audio.transcriptions.create(**kwargs)
    return response if response_format == "text" else response


def transcribe_with_timestamps(audio_path: str, language: str = "en") -> dict:
    """Get transcription with word and segment timestamps."""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language,
            response_format="verbose_json",       # required for timestamps
            timestamp_granularities=["word", "segment"]
        )
    return {
        "text": response.text,
        "segments": response.segments,
        # response.words is Word objects, not dicts — serialize manually if needed
        "words": [{"word": w.word, "start": w.start, "end": w.end}
                  for w in (response.words or [])],
        "duration": response.duration,
        "language": response.language
    }


def translate_audio(audio_path: str) -> str:
    """Translate non-English audio to English."""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.translations.create(
            model="whisper-1", file=audio_file
        )
    return response.text
```

### `templates/faster-whisper.py`

```python
"""
from faster_whisper import WhisperModel
from typing import Generator


class FasterWhisperTranscriber:
    """Optimized Whisper using CTranslate2 — 4x faster than original."""

    def __init__(self, model_size: str = "base",
                 device: str = "auto", compute_type: str = "auto"):
        """
        model_size: "tiny" | "base" | "small" | "medium" | "large-v3"
        device: "auto" | "cpu" | "cuda"
        Note: large-v3 on CPU requires ~10GB RAM — use base/small for CPU.
        """
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_path: str, language: str = None,
                   beam_size: int = 5, word_timestamps: bool = False,
                   vad_filter: bool = True) -> dict:
        """
        vad_filter=True removes silence (20-40% speed improvement on long files).
        Warning: vad_filter can silently drop segments under 0.5s.
        """
        segments, info = self.model.transcribe(
            audio_path,
            language=language,  # specify explicitly for accuracy + speed
            beam_size=beam_size,
            word_timestamps=word_timestamps,
            vad_filter=vad_filter
        )
        all_segments = []
        full_text = ""
        for segment in segments:
            seg = {"start": segment.start, "end": segment.end, "text": segment.text}
            if word_timestamps and segment.words:
                seg["words"] = [
                    {"word": w.word, "start": w.start, "end": w.end,
                     "probability": w.probability}
                    for w in segment.words
                ]
            all_segments.append(seg)
            full_text += segment.text
        return {
            "text": full_text.strip(),
            "segments": all_segments,
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration
        }

    def transcribe_stream(self, audio_path: str,
                          language: str = None) -> Generator[dict, None, None]:
        """Stream segments as they complete (still processes full file)."""
        segments, _ = self.model.transcribe(audio_path, language=language)
        for segment in segments:
            yield {"start": segment.start, "end": segment.end, "text": segment.text}
```

### `templates/split-audio.py`

```python
"""
from pydub import AudioSegment
import math
import os


def split_audio(path: str, chunk_min: int = 10,
                out_dir: str = "/tmp") -> list[str]:
    """
    Split audio file into chunks of ~chunk_min minutes.
    Exports as MP3 at 64kbps to stay well under 25MB Whisper API limit.
    Returns list of chunk file paths in order.
    """
    audio = AudioSegment.from_file(path)
    chunk_ms = chunk_min * 60 * 1000
    n = math.ceil(len(audio) / chunk_ms)
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i in range(n):
        chunk = audio[i * chunk_ms:(i + 1) * chunk_ms]
        p = os.path.join(out_dir, f"chunk_{i:03d}.mp3")
        chunk.export(p, format="mp3", bitrate="64k")
        paths.append(p)
    return paths


def merge_transcripts(transcripts: list[dict],
                      chunk_duration_s: float) -> dict:
    """
    Merge transcript chunks with adjusted timestamps.
    transcripts: list of verbose_json transcript dicts (one per chunk).
    chunk_duration_s: duration of each chunk in seconds.
    """
    merged_segments = []
    full_text = ""
    for i, transcript in enumerate(transcripts):
        offset = i * chunk_duration_s
        for segment in transcript.get("segments", []):
            merged_segments.append({
                "start": segment["start"] + offset,
                "end": segment["end"] + offset,
                "text": segment["text"]
            })
        full_text += transcript.get("text", "")
    return {"text": full_text.strip(), "segments": merged_segments}
```
