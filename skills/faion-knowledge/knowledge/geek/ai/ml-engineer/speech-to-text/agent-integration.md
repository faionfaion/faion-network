# Agent Integration — Speech-to-Text

## When to use
- Agent receives voice input from a user (browser microphone, phone call, uploaded audio)
- Processing audio artifacts: meeting recordings, podcast episodes, call center recordings
- Building a voice agent pipeline: user speech → STT → LLM → TTS → response
- Content indexing: transcribe video/audio libraries for semantic search
- Accessibility feature: real-time captions for live streams or video conferencing

## When NOT to use
- Input is already text — no transcription needed
- Audio is music, sound effects, or non-speech content — STT will produce garbage
- Real-time latency requirement is <50ms — no current STT solution achieves this; use silence detection and buffering instead
- Language is highly specialized with domain jargon and no custom vocabulary support available — consider fine-tuned local models
- Budget is zero and volume exceeds free tiers — self-host Whisper instead of paying API fees

## Where it fails / limitations
- Accents, dialects, and background noise degrade accuracy 10-30% vs clean studio audio
- Speaker diarization ("who said what") is available only on AssemblyAI, GPT-4o Transcribe, and Google — not base Whisper
- Whisper timestamps have ~0.5-1s drift over long recordings; post-process with alignment tools (wav2vec2) for subtitle-grade precision
- Real-time streaming STT adds 200-500ms buffering latency before the first partial transcript is returned
- Language detection is automatic in most APIs but can mis-detect short utterances or code-switching (mixing languages)
- File size limits: OpenAI Whisper API caps at 25MB per file — split long audio before submission
- Self-hosted `faster-whisper` on CPU is 5-10x slower than real-time for Large-v3; use GPU or Turbo variant

## Agentic workflow
STT fits as the first stage in a voice agent pipeline. A subagent receives a raw audio file path or base64-encoded audio blob, calls the chosen STT API, and returns structured output: `{transcript, language, duration_s, segments, speakers}`. For streaming voice agents, run STT in a separate async worker that emits partial transcript events to the LLM pipeline, enabling the LLM to start reasoning before transcription completes. Use VAD (Voice Activity Detection) upstream to trim silence and segment long recordings before passing to STT.

### Recommended subagents
- `faion-sdd-executor-agent` — can orchestrate STT as part of a larger media processing pipeline

### Prompt pattern
```python
# STT subagent task specification
task = {
    "action": "transcribe",
    "audio_path": "/tmp/meeting.mp3",
    "provider": "openai",          # or "assemblyai", "deepgram"
    "options": {
        "language": "en",          # None for auto-detect
        "diarization": False,
        "timestamps": "word",      # "none" | "segment" | "word"
    },
    "output_schema": {
        "transcript": "str",
        "segments": "list[{start, end, text}]",
        "language": "str",
    }
}
```

```python
# Instruct the orchestrator LLM
"""
You will receive audio transcription results in this format:
{"transcript": "...", "segments": [...], "language": "en"}
Summarize the key decisions made in the meeting. Cite segment timestamps.
"""
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` Python SDK | Whisper + GPT-4o Transcribe API | `pip install openai` / [docs](https://platform.openai.com/docs/guides/speech-to-text) |
| `faster-whisper` | Self-hosted, 4x faster than openai-whisper | `pip install faster-whisper` / [github](https://github.com/guillaumekln/faster-whisper) |
| `whisper.cpp` | CPU-optimized, no Python dependency | [github](https://github.com/ggerganov/whisper.cpp) |
| `assemblyai` SDK | AssemblyAI API (diarization, summaries) | `pip install assemblyai` / [docs](https://www.assemblyai.com/docs) |
| `deepgram-sdk` | Deepgram streaming + batch | `pip install deepgram-sdk` / [docs](https://developers.deepgram.com) |
| `pyannote-audio` | Speaker diarization for local Whisper output | `pip install pyannote.audio` / [github](https://github.com/pyannote/pyannote-audio) |
| `ffmpeg` | Audio format conversion and preprocessing | system package / [docs](https://ffmpeg.org/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Whisper API | SaaS | Yes | $0.006/min; 25MB limit; 99+ languages; simple REST |
| GPT-4o Transcribe | SaaS | Yes | $0.006/min; better accuracy + diarization; same API |
| AssemblyAI | SaaS | Yes | Best diarization; async + streaming; webhooks for long files |
| Deepgram | SaaS | Yes | Real-time streaming; custom vocabulary; $0.0043/min |
| ElevenLabs Scribe | SaaS | Yes | 150ms latency; best for voice agent pipelines |
| Google Speech-to-Text | SaaS | Yes | 125+ languages; streaming; enterprise compliance |
| faster-whisper | OSS | Yes | Self-hosted; 4x faster; GPU recommended for production |
| Whisper Large-v3 (HF) | OSS | Yes | Maximum accuracy; 1.55B params; requires GPU |

## Templates & scripts
```python
# transcribe.py — OpenAI Whisper with chunking for large files (≤45 lines)
import os
from pathlib import Path
from openai import OpenAI
import subprocess

client = OpenAI()
MAX_MB = 24  # stay under 25MB API limit

def split_audio(path: str, chunk_mins: int = 10) -> list[str]:
    """Split audio into chunks using ffmpeg."""
    out_pattern = path.replace(".", f"_chunk%03d.")
    subprocess.run([
        "ffmpeg", "-i", path,
        "-f", "segment", "-segment_time", str(chunk_mins * 60),
        "-c", "copy", out_pattern, "-y"
    ], check=True, capture_output=True)
    return sorted(Path(path).parent.glob("*_chunk*.mp3"))

def transcribe(audio_path: str, language: str = "en") -> dict:
    path = Path(audio_path)
    size_mb = path.stat().st_size / 1024 / 1024
    chunks = split_audio(audio_path) if size_mb > MAX_MB else [path]

    segments = []
    for chunk in chunks:
        with open(chunk, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1", file=f,
                language=language, response_format="verbose_json",
                timestamp_granularities=["segment"]
            )
        segments.extend(result.segments)

    return {
        "transcript": " ".join(s.text for s in segments),
        "segments": [{"start": s.start, "end": s.end, "text": s.text} for s in segments],
        "language": language,
    }
```

## Best practices
- Normalize audio to 16kHz mono WAV before sending to any STT API — reduces token count and improves accuracy
- Use `verbose_json` response format to get segment-level timestamps; plain `json` loses timing data
- Run VAD (e.g., silero-vad) to strip silence before batch transcription — cuts costs 20-40% on sparse audio
- Cache transcripts: audio files are immutable, so a content-hash key gives permanent cache validity
- For >1 hour recordings, use AssemblyAI async submit + webhook callback instead of synchronous APIs
- Always specify `language` explicitly if known — auto-detection adds latency and occasionally fails on short clips
- Store raw transcript + word-level timestamps; re-derive summaries/segments on demand rather than storing all variants
- Use `pyannote-audio` for speaker diarization on self-hosted Whisper pipelines (requires HuggingFace token)

## AI-agent gotchas
- Audio blobs passed as base64 in JSON messages grow context size rapidly — always save to disk and pass file paths
- STT errors are silent: the API returns `200 OK` with a short or empty transcript for inaudible audio — validate output length
- Language mis-detection on short (<5s) audio clips causes garbled output; pass `language` explicitly for voice agents
- OpenAI Whisper API has no streaming support — use Deepgram or ElevenLabs Scribe for real-time agent pipelines
- `faster-whisper` on CPU with Large-v3 is 5-10x slower than real-time; use `large-v3-turbo` for production without GPU
- Segment timestamps from Whisper drift cumulatively in recordings >30 min; realign with forced-alignment tools for subtitles
- File upload via multipart form requires `Content-Type: audio/mpeg` (or correct MIME); wrong MIME returns HTTP 400

## References
- [OpenAI Speech-to-Text](https://platform.openai.com/docs/guides/speech-to-text)
- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [faster-whisper GitHub](https://github.com/guillaumekln/faster-whisper)
- [AssemblyAI Docs](https://www.assemblyai.com/docs)
- [Deepgram Docs](https://developers.deepgram.com)
- [ElevenLabs Scribe](https://elevenlabs.io/realtime-speech-to-text)
- [pyannote-audio (diarization)](https://github.com/pyannote/pyannote-audio)
- [silero-vad (VAD)](https://github.com/snakers4/silero-vad)
