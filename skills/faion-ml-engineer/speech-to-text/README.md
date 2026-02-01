# Speech-to-Text

Speech-to-Text (STT) converts audio recordings into text transcriptions. Modern AI-powered STT systems provide high accuracy across many languages with features like speaker diarization, timestamps, and translation.

## Quick Reference

| Resource | Description |
|----------|-------------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples (Python) |
| [templates.md](templates.md) | Production-ready templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for transcription tasks |

## When to Use

- Meeting transcription
- Voice note processing
- Podcast/video transcription
- Voice command recognition
- Call center analysis
- Accessibility features
- Content indexing
- Real-time captioning

## Services Comparison (2026)

### OpenAI Models

| Model | Price | Features |
|-------|-------|----------|
| Whisper | $0.006/min | 99+ languages, timestamps |
| GPT-4o Transcribe | $0.006/min | Advanced accuracy, diarization |
| GPT-4o Mini Transcribe | $0.003/min | Cost-effective, good accuracy |

### Third-Party APIs

| Service | Latency | Languages | Price | Best For |
|---------|---------|-----------|-------|----------|
| AssemblyAI | ~300ms | 100+ | $0.002-0.04/min | Diarization, summaries |
| ElevenLabs Scribe | 150ms | 90+ | Variable | Real-time, low latency |
| Deepgram | Real-time | 30+ | $0.0043/min | Custom vocab, speed |
| Google Speech | Streaming | 125+ | $0.004-0.016/min | Enterprise, diarization |
| Azure Speech | Real-time | 85+ | $0.016/min | Microsoft ecosystem |
| Gladia | Streaming | Multi | Variable | Async + live streaming |
| Soniox | Real-time | 60+ | Variable | Mixed-language speech |

### Local Models

| Model | Parameters | Speed | Best For |
|-------|------------|-------|----------|
| Whisper Large-v3 | 1.55B | 1x real-time | Max accuracy |
| Whisper Large-v3 Turbo | 809M | 216x real-time | Production balance |
| faster-whisper | Varies | 4x faster | Self-hosted production |
| whisper.cpp | Varies | CPU optimized | Edge/mobile |
| Moonshine | 27M-200M | Fast | Mobile/embedded |

## Audio Formats

| Format | Quality | Size | Notes |
|--------|---------|------|-------|
| WAV | Lossless | Large | Best for accuracy |
| FLAC | Lossless | Medium | Recommended |
| MP3 | Good | Medium | Universal support |
| M4A | Good | Medium | Apple ecosystem |
| WebM | Variable | Small | Web applications |

## Decision Framework

```
Need real-time transcription?
├── Yes → Latency < 200ms needed?
│   ├── Yes → ElevenLabs Scribe (150ms)
│   └── No → AssemblyAI, Deepgram, or OpenAI Realtime
└── No → Batch processing
    ├── High volume (500+ hrs/month)?
    │   ├── Yes → Self-hosted Whisper
    │   └── No → OpenAI API
    └── Need speaker diarization?
        ├── Yes → AssemblyAI or GPT-4o with diarization
        └── No → Whisper or GPT-4o Mini
```

## Key Statistics (December 2025)

- Whisper: 4.1M monthly downloads on HuggingFace
- Combined Whisper variants: 10M+ monthly downloads
- Whisper Large-v3: 635% more training data (5M+ hours)
- Market projection: $73B by 2031

## References

- [OpenAI Speech-to-Text](https://platform.openai.com/docs/guides/speech-to-text)
- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [faster-whisper](https://github.com/guillaumekln/faster-whisper)
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp)
- [pyannote-audio](https://github.com/pyannote/pyannote-audio)
- [AssemblyAI Streaming](https://www.assemblyai.com/products/streaming-speech-to-text)
- [ElevenLabs Scribe](https://elevenlabs.io/realtime-speech-to-text)
- [Deepgram](https://deepgram.com/)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| STT model selection | haiku | Tool selection |
| Audio preprocessing | sonnet | Data preparation |
| Language handling | sonnet | Multilingual setup |
