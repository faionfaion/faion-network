# Speech-to-Text

## Summary

Speech-to-text (STT) methodology covering provider selection (OpenAI Whisper/GPT-4o, AssemblyAI, Deepgram, ElevenLabs Scribe), local model deployment (faster-whisper, whisper.cpp), integration patterns, and cost optimization. Decision axis: real-time vs. batch, accuracy vs. cost, cloud vs. self-hosted.

## Why

Modern STT APIs differ dramatically on latency (150ms vs 5s), accuracy (WER), language support (30–125 languages), and cost ($0.002–$0.04/min). Choosing the wrong provider costs 10–20x more or misses accuracy requirements. Self-hosted faster-whisper breaks even at ~500 hours/month versus API pricing.

## When To Use

- Meeting transcription, voice notes, podcast/video indexing (batch)
- Real-time captioning, voice commands, live call analysis (streaming)
- Any feature where users speak instead of type
- Audio content pipelines requiring transcript search or summarization

## When NOT To Use

- Audio is synthetic TTS output — transcribe the source text instead
- Audio quality is below 8kHz mono — accuracy will be poor across all providers; fix the recording
- Language is not in the provider's supported list — verify before building

## Content

| File | What's inside |
|------|---------------|
| `content/01-providers-comparison.xml` | Provider matrix (OpenAI/AssemblyAI/Deepgram/ElevenLabs/Deepgram/local), decision framework, audio format recommendations, cost calculator logic |
| `content/02-integration-patterns.xml` | Batch vs. streaming patterns, large-file chunking, speaker diarization, output formats (SRT/VTT), production rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/transcription-service.py` | Production TranscriptionService with multi-provider support, fallback, large-file chunking, faster-whisper |
| `templates/transcription-api.py` | FastAPI transcription endpoint with background async processing and webhook delivery |
