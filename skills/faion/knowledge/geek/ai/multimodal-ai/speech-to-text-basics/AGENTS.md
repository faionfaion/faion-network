# Speech-to-Text Basics

## Summary

Transcribing audio to text using OpenAI Whisper API, local Whisper, or faster-whisper (CTranslate2). Covers API parameters for timestamps and translation, local model selection by hardware, and the 25MB file-size limit that forces pre-splitting.

## Why

Whisper is the de-facto standard for multilingual transcription, but the API is batch-only (no streaming) and has a 25MB file limit. Specifying the language code explicitly saves ~200ms and prevents misidentification between similar languages (Ukrainian/Russian, Serbian/Croatian).

## When To Use

- Transcribing recorded audio: interviews, meetings, podcasts, call recordings
- Building voice input pipelines where microphone audio is the primary channel
- Generating searchable transcripts with timestamps for media libraries
- Multilingual transcription or audio-to-English translation
- Pre-processing audio before LLM analysis (summarize, extract, classify)

## When NOT To Use

- Real-time streaming requirements below 300ms — use Deepgram or AssemblyAI WebSocket streaming instead
- Audio files exceeding 25MB per file — must split first with pydub
- Extremely noisy audio (SNR below 5dB) — accuracy degrades to unusable
- High-volume production (>10k hours/month) — local faster-whisper on GPU is significantly cheaper

## Content

| File | What's inside |
|------|---------------|
| `content/01-api-usage.xml` | Whisper API transcription, timestamps, translation; LocalWhisper class; FasterWhisperTranscriber with streaming |
| `content/02-rules.xml` | Language parameter rule, file size limit, format requirements, local model sizing guide |

## Templates

| File | Purpose |
|------|---------|
| `templates/whisper-api.py` | transcribe_audio, transcribe_with_timestamps, translate_audio functions |
| `templates/faster-whisper.py` | FasterWhisperTranscriber with VAD filter and streaming |
| `templates/split-audio.py` | pydub helper to split audio into chunks under 24MB |
