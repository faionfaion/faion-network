# Text-to-Speech

## Summary

**One-sentence:** Ship TTS by picking provider (latency / voice quality / cost), caching audio by text-hash, gating voice cloning behind explicit consent, and wiring a fallback for outage resilience.

**One-paragraph:** TTS provider choice spans 5× cost and 10× latency: OpenAI tts-1 ($15/M chars, ≈800ms first byte), ElevenLabs Turbo v2 ($0.18/1k chars, ≈400ms with streaming), Google Cloud (Chirp 3, $16/M, ≈600ms), Azure ($16/M, neural voices), Deepgram Aura ($0.135/1k, ≈200ms), local Coqui XTTS (free, GPU-bound). Cache audio output by text-hash because identical strings recur 40-70% in real traffic. Voice cloning requires consent record per voice. Streaming TTS to the user reduces perceived latency by ≈70%. Output: a `tts-config.yaml` declaring provider + voice + cache + fallback + consent.

**Ефективно для:**

- Voice agents та IVR — latency ≤500ms критичний; Deepgram Aura або ElevenLabs Turbo дають real-time.
- Audiobook / podcast generation — quality &gt; latency; ElevenLabs multilingual або Google Chirp 3 з 25+ голосами.
- Notifications / accessibility — кешуй; одна й та сама фраза перевикористовується 100×.
- Brand voice — voice cloning з консент-логом + ElevenLabs Voice Lab.

## Applies If (ALL must hold)

- Need to convert text → spoken audio in product flow
- Latency budget defined per use case (real-time vs batch)
- Voice quality requirements articulated (neural vs basic)

## Skip If (ANY kills it)

- Use case is dual-purpose (display text + read aloud); start with display text and add TTS later
- All target languages out of provider support
- Voice cloning required but no consent process exists — legal / ethics block

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `use-case-constraints.yaml` | YAML | latency, voice quality, cost cap |
| `voice-catalog.yaml` | YAML | provider voice IDs + language coverage |
| `consent-record.yaml` | YAML | per-voice consent metadata (cloning use) |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `speech-to-text` | Sibling in voice-agent stack |
| `cost-optimization` | Provider rate comparison |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: latency-bucket pick, voice consent, cache-by-hash, streaming for real-time, mandatory fallback | 1100 |
| `content/02-output-contract.xml` | essential | tts-config.yaml schema | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: no cache, cloning without consent, real-time on tts-1, hard-coded provider, missing language fallback | 900 |
| `content/04-procedure.xml` | essential | 5 steps: scope → bench → pick → cache+fallback → ship | 700 |
| `content/05-examples.xml` | essential | Worked example: voice agent with ElevenLabs Turbo + OpenAI fallback + Redis cache | 500 |
| `content/06-decision-tree.xml` | essential | Routes by latency + voice quality + cloning need | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `voice_quality_blind_test` | n/a (human) | Subjective |
| `provider_compare_drafting` | sonnet | Trade-offs |
| `tts_config_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/tts-cached.py` | TTS call with text-hash cache layer |
| `templates/chunk-text.py` | Long-text → sentence chunks for streamed TTS |
| `templates/tts-config.schema.yaml` | Schema for tts-config |
| `templates/_smoke-test.yaml` | Minimum-viable tts-config |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-text-to-speech.py` | Lint tts-config | Pre-commit |

## Related

- [[speech-to-text]] — paired in voice agents
- external: [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech) · [ElevenLabs](https://elevenlabs.io/) · [Deepgram Aura](https://deepgram.com/product/voice-ai)

## Decision tree

See `content/06-decision-tree.xml`. Routes by (a) latency budget, (b) voice-cloning need, (c) on-prem requirement → {Aura, ElevenLabs Turbo, OpenAI tts-1, Google Chirp, Coqui local}.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tts-cached.py`

```python
"""TTS with content-hash caching to avoid redundant API calls."""
import hashlib
import os
from pathlib import Path

from elevenlabs.client import ElevenLabs
from elevenlabs import stream


CACHE_DIR = Path(os.environ.get("TTS_CACHE_DIR", "/tmp/tts-cache"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

DEFAULT_VOICE = "JBFqnCBsd6RMkjVDRZzb"   # Rachel
DEFAULT_MODEL = "eleven_flash_v2_5"
DEFAULT_FORMAT = "mp3_44100_128"


def _cache_key(text: str, voice_id: str, model_id: str, output_format: str) -> str:
    raw = f"{text}|{voice_id}|{model_id}|{output_format}"
    return hashlib.sha256(raw.encode()).hexdigest()


def synthesize(
    text: str,
    voice_id: str = DEFAULT_VOICE,
    model_id: str = DEFAULT_MODEL,
    output_format: str = DEFAULT_FORMAT,
) -> bytes:
    """Generate TTS audio with cache. Returns audio bytes."""
    key = _cache_key(text, voice_id, model_id, output_format)
    cache_path = CACHE_DIR / f"{key}.mp3"

    if cache_path.exists():
        return cache_path.read_bytes()

    audio = b"".join(client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id=model_id,
        output_format=output_format,
    ))
    cache_path.write_bytes(audio)
    return audio


def synthesize_streaming(
    text: str,
    voice_id: str = DEFAULT_VOICE,
    model_id: str = DEFAULT_MODEL,
) -> None:
    """Stream TTS audio to speakers with minimal latency. Does not cache."""
    audio_stream = client.text_to_speech.stream(
        voice_id=voice_id,
        text=text,
        model_id=model_id,
        output_format="mp3_44100_128",
    )
    stream(audio_stream)
```

### `templates/chunk-text.py`

````python
"""Text normalization and sentence-boundary chunking for TTS pipelines."""
import re
from typing import Generator


def normalize_for_tts(text: str) -> str:
    """Clean LLM output and markdown for TTS consumption."""
    # Strip markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)          # **bold**
    text = re.sub(r'\*(.*?)\*', r'\1', text)               # *italic*
    text = re.sub(r'`[^`]+`', '', text)                    # `inline code`
    text = re.sub(r'```[\s\S]*?```', '', text)             # code blocks
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # [text](url)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)  # headings

    # Expand common abbreviations for clearer speech
    abbreviations = {
        "e.g.": "for example",
        "i.e.": "that is",
        "vs.": "versus",
        "etc.": "and so on",
        "Dr.": "Doctor",
        "Mr.": "Mister",
        "Mrs.": "Missus",
        "API": "A P I",
        "URL": "U R L",
        "UI": "U I",
    }
    for abbr, expansion in abbreviations.items():
        text = text.replace(abbr, expansion)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def chunk_for_streaming(
    text: str,
    max_sentences: int = 2,
    min_chars: int = 20,
) -> Generator[str, None, None]:
    """
    Split text at sentence boundaries for streaming TTS.
    Yields chunks of max_sentences sentences, never mid-word.
    """
    # Split on sentence-ending punctuation followed by space
    sentence_re = re.compile(r'(?<=[.!?])\s+')
    sentences = [s.strip() for s in sentence_re.split(text.strip()) if s.strip()]

    buffer: list[str] = []
    for sentence in sentences:
        buffer.append(sentence)
        chunk = ' '.join(buffer)
        if len(buffer) >= max_sentences and len(chunk) >= min_chars:
            yield chunk
            buffer = []

    if buffer:
        remaining = ' '.join(buffer)
        if remaining:
            yield remaining


def prepare_for_tts(text: str, chunk: bool = True) -> list[str]:
    """Full pipeline: normalize then optionally chunk into streaming segments."""
    normalized = normalize_for_tts(text)
    if not chunk:
        return [normalized]
    return list(chunk_for_streaming(normalized))
````

### `templates/tts-config.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [provider, model, voice, cache, fallback]
properties:
  provider: {type: string, enum: [openai, elevenlabs, google, azure, deepgram, local-coqui]}
  model: {type: string}
  voice:
    type: object
    required: [id, clone_consent]
    properties:
      id: {type: string}
      clone_consent: {type: boolean}
  cache:
    type: object
    required: [enabled]
    properties:
      enabled: {type: boolean}
      ttl_days: {type: integer, minimum: 1}
  fallback:
    type: object
    required: [provider]
    properties:
      provider: {type: string}
      model: {type: string}
```

### `templates/_smoke-test.yaml`

```yaml
provider: elevenlabs
model: eleven_turbo_v2
voice: {id: rachel, clone_consent: true}
cache: {enabled: true, ttl_days: 30}
fallback: {provider: openai, model: tts-1}
```
