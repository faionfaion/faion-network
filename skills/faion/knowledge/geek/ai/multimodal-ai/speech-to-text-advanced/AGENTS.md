# Speech-to-Text Advanced

## Summary

Long audio processing (>25MB), speaker diarization, and a production `TranscriptionService` with
provider routing (OpenAI, faster-whisper, local Whisper). Covers chunked transcription via
`LongAudioTranscriber`, speaker labeling via `SpeakerDiarizer` (pyannote 3.1), and known bugs in
the template implementations that agents must patch before using.

## Why

Whisper API rejects files above 25MB and returns no speaker attribution. Chunking with overlap
prevents boundary-word loss; diarization adds "who said what" labels required for meeting and
interview pipelines. Without pre-caching the pyannote model (~1.5GB) the first diarization
request fails mid-run in production.

## When To Use

- Audio files larger than 25MB need transcription (Whisper API hard limit).
- Multi-speaker recordings (meetings, podcasts, interviews) need speaker attribution.
- Long-form transcription (1+ hour files) requiring timestamps and segment structure.
- Building a production STT service with provider fallback (cloud vs. local GPU).

## When NOT To Use

- Audio under 25MB, single speaker — use `speech-to-text-basics` direct API call; `LongAudioTranscriber` adds unnecessary overhead.
- Real-time (live) transcription — Whisper is batch-only; use Deepgram or AssemblyAI streaming.
- GPU unavailable and diarization needed — pyannote on CPU is ~10x real-time; impractical.
- Language is non-standard or heavily accented without prior quality validation.

## Content

| File | What's inside |
|------|---------------|
| `content/01-chunking.xml` | `LongAudioTranscriber` logic, overlap strategy, known bug fix for `_transcribe_chunk`. |
| `content/02-diarization.xml` | `SpeakerDiarizer` setup, HuggingFace token requirement, alignment logic, pyannote gotchas. |
| `content/03-service.xml` | `TranscriptionService` provider routing, production rules, preprocessing best practices. |

## Templates

| File | Purpose |
|------|---------|
| `templates/transcription_service.py` | `TranscriptionService`, `LongAudioTranscriber`, `SpeakerDiarizer` with bug fixes applied. |
| `templates/prompt-transcribe.txt` | Agent task prompt for transcription subagent with strategy routing. |
