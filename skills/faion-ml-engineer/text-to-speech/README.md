# Text-to-Speech

## Overview

Text-to-Speech (TTS) converts written text into natural-sounding audio. Modern AI-powered TTS systems offer human-like voices, emotional expression, and multiple language support for applications like audiobooks, voice assistants, and accessibility tools.

## When to Use

- Voice assistants and chatbots
- Audiobook generation
- Video narration
- Accessibility features
- Podcast production
- Interactive voice response (IVR)
- E-learning content
- Real-time conversational AI

## TTS Provider Comparison (2025-2026)

| Provider | Voices | Languages | Latency | Voice Cloning | Cost |
|----------|--------|-----------|---------|---------------|------|
| ElevenLabs | 5,000+ | 70+ | 75ms (Flash v2.5) | Yes (instant + pro) | $0.18-0.30/1K chars |
| OpenAI TTS | 6 | 50+ | ~500ms | No | $0.015-0.030/1K chars |
| Google TTS | 400+ | 50+ | ~200ms | No | $0.004-0.016/1K chars |
| Azure TTS | 500+ | 140+ | ~200ms | Yes (Custom Neural) | $0.004-0.016/1K chars |
| Coqui/XTTS | Many | 50+ | Local | Yes | Free (self-hosted) |
| PlayHT | 900+ | 142 | ~150ms | Yes | $0.10-0.20/1K chars |
| Deepgram Aura | 12+ | 12 | 250ms | No | $0.0135/1K chars |

## Provider Selection Guide

| Use Case | Recommended Provider | Reason |
|----------|---------------------|--------|
| Maximum quality/realism | ElevenLabs | Best emotional expression, nuanced intonation |
| Real-time streaming (<100ms) | ElevenLabs Flash v2.5 | 75ms latency optimized |
| OpenAI ecosystem | OpenAI TTS | Native integration, steerability |
| Budget production | Google/Azure TTS | Lowest cost per character |
| Voice cloning required | ElevenLabs | Instant + professional cloning |
| Privacy/self-hosted | Coqui XTTS | Open source, local inference |
| Multilingual (140+ langs) | Azure TTS | Widest language coverage |

## Voice Characteristics

| Attribute | Description | Control Method |
|-----------|-------------|----------------|
| Pitch | High/low voice frequency | SSML `<prosody pitch>` |
| Speed | Words per minute (0.25x-4x) | API param, SSML `<prosody rate>` |
| Tone | Emotional quality | Voice selection, prompting (OpenAI) |
| Stability | Voice consistency | ElevenLabs stability param |
| Similarity | Clone accuracy | ElevenLabs similarity_boost |
| Style | Expressiveness | ElevenLabs style param |

## Key Features by Provider

### ElevenLabs

- **Flash v2.5**: Ultra-low 75ms latency for real-time apps
- **Multilingual v2**: Highest quality, nuanced expression
- **Voice Cloning**: Instant (seconds of audio) + Professional (high-fidelity)
- **Projects**: Long-form audiobook creation with chapter management
- **Voice Library**: 5,000+ community voices
- **Streaming**: Real-time audio streaming

### OpenAI TTS

- **Voices**: alloy, echo, fable, onyx, nova, shimmer
- **Models**: tts-1 (fast), tts-1-hd (quality)
- **Steerability**: Prompt-based tone control ("speak calmly")
- **Speed**: 0.25x to 4.0x
- **Formats**: mp3, opus, aac, flac, wav, pcm
- **Streaming**: Real-time with PCM output

### Google Cloud TTS

- **Neural2/Polyglot**: High-quality neural voices
- **WaveNet**: Realistic intonation
- **SSML**: Full SSML 1.1 support
- **Custom Voice**: Train on your data (requires volume)

### Azure TTS

- **Neural voices**: 500+ voices
- **Custom Neural Voice**: Clone with 30 min audio
- **SSML**: Advanced SSML with neural effects
- **Viseme**: Lip-sync data for avatars

## Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples (OpenAI, ElevenLabs, Google) |
| [templates.md](templates.md) | Production-ready templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for TTS tasks |

## Best Practices

1. **Voice Selection**
   - Match voice to content type (narration vs conversational)
   - Test multiple voices with actual content
   - Consider audience preferences and cultural context

2. **Text Preparation**
   - Clean and normalize text before synthesis
   - Use SSML for pronunciation control
   - Handle abbreviations explicitly (e.g., "Dr." to "Doctor")

3. **Quality vs Latency**
   - Use HD/Multilingual models for pre-generated content
   - Use Flash/tts-1 for real-time applications
   - Streaming reduces perceived latency

4. **Cost Optimization**
   - Cache repeated phrases (greetings, common responses)
   - Use content-based cache keys (hash text+voice+params)
   - Batch similar requests where possible
   - Use local models (Coqui) for development

5. **Streaming Best Practices**
   - Use PCM format for lowest latency
   - Buffer 2-3 chunks before playback
   - Handle network interruptions gracefully

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Abbreviations read literally | Preprocess or use SSML `<sub>` |
| No emotional control | Use ElevenLabs or OpenAI steerability |
| Long text API limits | Chunk at sentence boundaries |
| Regenerating same audio | Implement content-based caching |
| High latency in real-time | Use streaming + Flash models |
| Inconsistent voice in clone | Increase stability parameter |

## References

- [ElevenLabs Documentation](https://elevenlabs.io/docs)
- [ElevenLabs API Reference](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
- [OpenAI TTS Guide](https://platform.openai.com/docs/guides/text-to-speech)
- [Google Cloud TTS](https://cloud.google.com/text-to-speech/docs)
- [Azure Speech Service](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [SSML Reference](https://cloud.google.com/text-to-speech/docs/ssml)
- [Coqui TTS](https://github.com/coqui-ai/TTS)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| TTS model selection | haiku | Tool selection |
| Voice synthesis tuning | sonnet | Quality optimization |
| Real-time streaming | sonnet | Performance pattern |
