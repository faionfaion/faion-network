# Agent Integration — Text-to-Speech

## When to use
- Automated podcast/audiobook generation from text content pipelines (neromedia-style)
- Voice narration for video generation workflows (pair with video-generation methodology)
- Accessibility layer for web or app content that must be audible
- IVR or conversational voice bot responses that require low-latency audio
- Agent workflows that produce audio reports or briefings delivered via Telegram or email

## When NOT to use
- One-off manual narration where a human voice actor produces higher perceived quality
- Real-time <75ms latency required and ElevenLabs Flash is not in budget
- Languages with <5% coverage in target voice model (check provider language list first)
- High-volume pipelines where cost per character exceeds budget ceiling (use Google/Azure instead of ElevenLabs)
- When voice consistency across sessions is critical but cloning samples are unavailable

## Where it fails / limitations
- Abbreviations (Dr., LLC, API) are often mispronounced — requires SSML `<sub>` or text normalization
- Long inputs (>5000 chars) must be chunked at sentence boundaries; mid-sentence splits produce artifacts
- Voice cloning requires consent from the voice owner — legal risk if skipped
- ElevenLabs stability parameter below 0.4 produces expressive but inconsistent output across regenerations
- OpenAI TTS has no emotion/SSML control; steerability via prompt is inconsistent
- Cached audio becomes stale if underlying text changes without cache invalidation

## Agentic workflow
An agent receives a text article or script, normalizes abbreviations and special characters, chunks the text at sentence boundaries, calls the TTS API in sequence (or parallel for long documents), assembles audio segments in order, and uploads the final file. For real-time applications, the agent streams PCM chunks directly to the audio sink without assembly. Caching by content hash prevents redundant API calls for repeated phrases.

### Recommended subagents
- `faion-sdd-executor-agent` — suitable for batch audio generation tasks in media pipelines

### Prompt pattern
```python
# ElevenLabs streaming TTS — agent integration pattern
from elevenlabs import ElevenLabs, VoiceSettings
import hashlib, os

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

def tts_cached(text: str, voice_id: str, cache_dir: str = ".tts_cache") -> bytes:
    key = hashlib.sha256(f"{voice_id}:{text}".encode()).hexdigest()
    path = f"{cache_dir}/{key}.mp3"
    if os.path.exists(path):
        return open(path, "rb").read()
    audio = b"".join(client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(stability=0.6, similarity_boost=0.8),
    ))
    os.makedirs(cache_dir, exist_ok=True)
    open(path, "wb").write(audio)
    return audio
```

```python
# Text normalization before TTS
import re

def normalize_for_tts(text: str) -> str:
    replacements = {
        r"\bDr\.": "Doctor",
        r"\bAPI\b": "A P I",
        r"\bURL\b": "U R L",
        r"\bLLC\b": "L L C",
        r"\bAI\b": "A I",
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    return text
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `elevenlabs` Python SDK | ElevenLabs API (streaming, voice cloning, projects) | `pip install elevenlabs` / elevenlabs.io/docs |
| `openai` Python SDK | OpenAI TTS (tts-1, tts-1-hd) | `pip install openai` / platform.openai.com/docs/guides/text-to-speech |
| `google-cloud-texttospeech` | Google TTS (Neural2, WaveNet, SSML) | `pip install google-cloud-texttospeech` / cloud.google.com/text-to-speech |
| `azure-cognitiveservices-speech` | Azure TTS (500+ voices, SSML, viseme) | `pip install azure-cognitiveservices-speech` / azure.microsoft.com |
| `TTS` (Coqui) | Self-hosted open-source TTS (XTTS v2) | `pip install TTS` / github.com/coqui-ai/TTS |
| `ffmpeg` | Audio format conversion, concatenation | system package / ffmpeg.org |
| `pydub` | Python audio manipulation (split, join, normalize) | `pip install pydub` / github.com/jiaaro/pydub |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ElevenLabs | SaaS | Yes | REST API + Python SDK; streaming supported; Flash v2.5 for <100ms |
| OpenAI TTS | SaaS | Yes | Simple REST API; 6 voices; steer tone via prompt |
| Google Cloud TTS | SaaS | Yes | SSML support; cheapest per-char for high volume; 400+ voices |
| Azure Cognitive Speech | SaaS | Yes | Widest language coverage (140+); SSML + viseme for lip-sync |
| PlayHT | SaaS | Yes | 900+ voices; REST API; voice cloning; 142 languages |
| Deepgram Aura | SaaS | Yes | Lowest latency for English; 12 voices; suited for real-time |
| Coqui XTTS v2 | OSS | Yes | Self-hosted; no per-char cost; GPU required for real-time |

## Templates & scripts
See `templates.md` for full streaming and batch production templates.

Text chunker for TTS (handles sentence boundaries):

```python
import re

def chunk_text(text: str, max_chars: int = 4000) -> list[str]:
    """Split text at sentence boundaries without exceeding max_chars."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks, current = [], ""
    for sentence in sentences:
        if len(current) + len(sentence) + 1 > max_chars:
            if current:
                chunks.append(current.strip())
            current = sentence
        else:
            current = f"{current} {sentence}" if current else sentence
    if current:
        chunks.append(current.strip())
    return chunks
```

## Best practices
- Normalize all abbreviations before synthesis — maintain a domain-specific replacement dict
- Use content-hash-based caching: same text + voice + params always yields same audio
- Choose PCM format for streaming (lowest overhead); mp3 for stored files (smallest size)
- Buffer 2-3 audio chunks before starting playback to absorb network jitter
- For cloned voices: always obtain written consent and store it alongside the voice ID
- Test voices with actual production content, not generic demo text — quality varies by domain
- Use ElevenLabs Projects for long-form content (audiobooks, courses) — handles chapter management natively

## AI-agent gotchas
- TTS APIs are synchronous for short text but some providers (ElevenLabs Projects) are async — agent must poll for completion
- ElevenLabs character limits differ by tier; agent must check remaining characters before submitting a batch job
- Parallel TTS calls to ElevenLabs may hit rate limits (tier-dependent); implement exponential backoff
- Audio file paths in agent outputs must be absolute or presigned URLs — relative paths break when caller is on a different host
- Coqui XTTS requires GPU; agent running on CPU-only infra must delegate to a GPU worker
- Human review required before publishing cloned voice content — verify consent records exist

## References
- https://elevenlabs.io/docs/api-reference/text-to-speech/convert
- https://platform.openai.com/docs/guides/text-to-speech
- https://cloud.google.com/text-to-speech/docs/ssml
- https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/
- https://github.com/coqui-ai/TTS
