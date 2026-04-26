# Agent Integration — Text-to-Speech Basics

## When to use
- Converting article or news content to audio for podcast-style delivery
- Building voice notifications or status readouts in agent pipelines
- Generating narration tracks for video content automation
- Creating audio previews of generated text for human review
- Adding voice responses to a chatbot or assistant interface

## When NOT to use
- Sub-second response latency is required — OpenAI TTS adds 300–800ms minimum; use cached audio for known phrases
- The text contains heavy domain-specific abbreviations without preprocessing — APIs read "Dr." as "Doctor" correctly but "ETA", "API", "DB" are read literally and sound odd
- Voice quality is mission-critical and a specific person's voice is required — use ElevenLabs voice cloning (tts-implementation), not generic voices
- Text exceeds 4096 characters in a single pass — use `LongTextTTS` chunking (tts-implementation); passing long text to the basic API truncates or errors

## Where it fails / limitations
- OpenAI TTS `speed` parameter range is 0.25–4.0; values outside this range raise a validation error
- `SSMLBuilder.build()` generates Google Cloud-compatible SSML — OpenAI TTS does not support SSML; passing SSML tags to OpenAI will be read verbatim
- Voice consistency across sessions: OpenAI voices (alloy, nova, etc.) are deterministic per text but have no persistent identity across model updates
- `tts-1` vs `tts-1-hd`: `tts-1-hd` has ~2× latency; use `tts-1` for streaming/real-time, `tts-1-hd` for final production audio
- No emotion or prosody control in OpenAI TTS — same flat delivery regardless of exclamation marks or SSML markup
- Google Cloud TTS Neural2 voices are higher quality than Standard; Studio voices are highest but cost more and have usage caps

## Agentic workflow
A Claude subagent receives text content and voice/format requirements, calls `text_to_speech()`, and returns the audio file path. For content pipelines, an orchestrator agent preprocesses text (expand abbreviations, normalize numbers, add pauses at paragraph breaks) before passing to TTS. Voice selection is handled by a routing rule: `nova` for conversational, `onyx` for formal narration, `alloy` as neutral default. Generated audio is cached by content hash to avoid regenerating identical phrases.

### Recommended subagents
- `haiku` — Execute TTS API call: receive text + voice params, return file path
- `sonnet` — Text preprocessing: expand abbreviations, normalize numbers, insert SSML-style pause markers for Google TTS
- `haiku` — Cache lookup: hash text+voice+speed → check cache dir → return cached path or None

### Prompt pattern
```xml
<task>
Convert text to speech.
Text: {{TEXT}}
Voice: {{VOICE}}  (alloy|echo|fable|onyx|nova|shimmer)
Model: {{MODEL}}  (tts-1 for speed, tts-1-hd for quality)
Speed: {{SPEED}}  (0.25–4.0, default 1.0)
Output: {{OUTPUT_PATH}}

Return: {"path": "...", "duration_estimate_s": N}
On error: {"error": "..."}
</task>
```

```python
# Voice selection rule for agents
VOICE_MAP = {
    "news": "onyx",          # authoritative male
    "assistant": "nova",     # friendly female
    "narrator": "fable",     # storytelling
    "neutral": "alloy",      # balanced, default
    "whisper": "shimmer",    # soft, gentle
}
voice = VOICE_MAP.get(content_type, "alloy")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| openai (Python SDK) | OpenAI TTS API client | `pip install openai` / platform.openai.com/docs/guides/text-to-speech |
| google-cloud-texttospeech | Google Cloud TTS client | `pip install google-cloud-texttospeech` |
| pydub | Audio duration check, format convert, concatenate | `pip install pydub` |
| ffmpeg | Format conversion, trim, normalize audio level | `apt install ffmpeg` |
| elevenlabs | ElevenLabs TTS SDK | `pip install elevenlabs` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI TTS (tts-1, tts-1-hd) | SaaS | Yes — Python SDK | Fastest setup; 6 voices; no SSML; $0.015/1k chars (HD: $0.030) |
| ElevenLabs | SaaS | Yes — Python SDK | Best voice quality + cloning; multilingual; higher cost |
| Google Cloud TTS | SaaS | Yes — Python SDK | SSML support; 400+ voices; Neural2 + Studio tiers |
| Azure Cognitive Services TTS | SaaS | Yes — REST/SDK | SSML + neural voices; good multilingual coverage |
| Coqui TTS | OSS | Yes — Python | Self-hosted; quality lower than cloud; zero API cost |
| Kokoro TTS | OSS | Yes — local | Small (~80MB) high-quality model; runs on CPU; MIT license |
| Amazon Polly | SaaS | Yes — boto3 | AWS-native; SSML support; Neural voices; pay-per-char |

## Templates & scripts
See `templates.md` for `text_to_speech()`, `SSMLBuilder`, `stream_to_file` patterns.

Inline: audio duration check after generation (8 lines):
```python
from pydub import AudioSegment

def get_audio_duration(path: str) -> float:
    """Return duration in seconds."""
    audio = AudioSegment.from_file(path)
    return len(audio) / 1000.0

# Usage after TTS call:
duration = get_audio_duration(output_path)
assert duration > 0.1, f"TTS output suspiciously short: {duration}s"
```

## Best practices
- Cache by `sha256(text + voice + speed + model)` — TTS output is deterministic; caching eliminates cost for repeated phrases
- Preprocess text before TTS: expand contractions, replace symbols ($→ dollars, % → percent), spell out abbreviations (API → A-P-I or "API")
- Use `response_format="pcm"` for streaming playback (lower latency); use `mp3` for storage
- For narration of structured content: insert explicit pause markers between sections by splitting text and concatenating audio segments with pydub silence
- Test all 6 OpenAI voices against your content type before committing — voice-content mismatch is jarring to listeners
- Use `tts-1` for draft/preview generation; switch to `tts-1-hd` only for final production assets
- Limit single API call to 4000 chars max (not 4096) to avoid off-by-one truncation on some client versions

## AI-agent gotchas
- `SSMLBuilder` output is not compatible with OpenAI TTS — agents must route SSML to Google Cloud or Azure, not OpenAI
- `stream_to_file` is synchronous and blocks the event loop — wrap in `asyncio.to_thread()` for async pipelines
- OpenAI TTS does not return duration; agents must measure audio duration locally (pydub) if needed for downstream timing
- Rate limits: OpenAI TTS is 50 RPM on tier 1; batch generation of 100 short clips will hit limits; add 1.2s delay between calls
- Voice names are provider-specific and non-portable: "nova" (OpenAI) ≠ "en-US-Neural2-D" (Google) — parameterize by semantic label (news/assistant/narrator) not provider name
- Generated audio files use the process's temp dir by default — in containerized environments, `/tmp` may have limited space for long audio
- Agents must not pass raw Markdown or HTML to TTS — asterisks, hashes, and angle brackets are read literally

## References
- https://platform.openai.com/docs/guides/text-to-speech
- https://platform.openai.com/docs/api-reference/audio/createSpeech
- https://cloud.google.com/text-to-speech/docs/ssml
- https://cloud.google.com/text-to-speech/docs/voices
- https://elevenlabs.io/docs/api-reference/text-to-speech
- https://github.com/coqui-ai/TTS
