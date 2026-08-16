# Text-to-Speech Basics

## Summary

**One-sentence:** Routes a single TTS call to OpenAI TTS, ElevenLabs, or Google Cloud TTS with a sha256-keyed cache and an explicit SSML-routing rule.

**One-paragraph:** Converts ≤4000-character text to natural speech using OpenAI TTS (fast, no SSML, 6 voices, $0.015/1k chars), ElevenLabs (best quality, multilingual, voice cloning), or Google Cloud TTS (400+ voices, SSML supported). Covers voice selection, content-hash caching (sha256 of text + voice + speed + model), text preprocessing for symbols and Markdown, and the hard SSML routing rule: never pass SSML to OpenAI — only to Google or Azure. Output is an audio file path plus duration estimate, deterministic per input.

**Ефективно для:** агента контент-конвеєра, що вибирає TTS-провайдера, кешує генерацію та готує текст до синтезу — закриває петлю між LLM-виходом і озвучкою без подвійних рахунків.

## Applies If (ALL must hold)

- Converting article, news, or notification text to audio in an agent pipeline.
- Text fits in a single API call (≤4000 characters; longer text goes to `tts-implementation`).
- Output format is a saved audio file (mp3 / opus / wav / pcm), not a live duplex stream.
- A deterministic cache key (text + voice + speed + model) is acceptable.
- The agent has at least one provider API key (OpenAI / ElevenLabs / Google Cloud).

## Skip If (ANY kills it)

- Text exceeds 4000 characters — use `tts-implementation` which provides LongTextTTS chunking.
- Sub-200ms first-byte latency required — OpenAI TTS adds 300-800ms minimum; cache phrases instead.
- A specific person's voice is required — use ElevenLabs voice cloning in `tts-implementation`.
- SSML markup (pauses, prosody, say-as) is needed against OpenAI TTS — OpenAI reads SSML literally.
- Heavy domain abbreviations (API, ETA, DB) without preprocessing — they are read literally.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Text payload | UTF-8 string, ≤4000 chars | upstream LLM / preprocessor |
| Voice label | semantic key (`news`, `assistant`, `narrator`) | content type router |
| Provider credentials | env var (`OPENAI_API_KEY`, `ELEVEN_API_KEY`) | secrets manager |
| Output path | filesystem path with rw access | pipeline orchestrator |
| Optional speed | float 0.25-4.0 | caller default 1.0 |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/structured-output-basics` | upstream LLM output is the text payload; needs to be JSON-shaped, then text-extracted before TTS |
| `geek/ai/multimodal-ai/tts-implementation` | downstream path when payload exceeds 4000 chars or streaming is required |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: model tier, SSML routing, cache key, preprocess, char cap, rate-limit delay | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema of synthesize() result + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: SSML to OpenAI, raw Markdown, async-on-sync, missing voice map, cache key without provider | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure: preprocess → select voice → check cache → call provider → save → log | ~700 |
| `content/05-examples.xml` | medium | One worked synthesize() call with cache hit + cache miss paths | ~500 |
| `content/06-decision-tree.xml` | essential | Provider routing decision: SSML required? voice clone? language coverage? cost cap? | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `select-voice` | haiku | Lookup against semantic voice map; deterministic. |
| `preprocess-text` | sonnet | Strip Markdown, expand abbreviations; per-input judgment. |
| `route-provider` | sonnet | Decision-tree walk: SSML, language, voice clone, cost. |
| `synthesize-call` | haiku | Single API call with retry; mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tts_basic.py` | OpenAI TTS wrapper with cache + preprocess hooks; ≤60 lines. |
| `templates/voice-map.py` | Semantic voice routing by content type (`news`, `assistant`, `narrator`). |
| `templates/prompt-tts.txt` | Agent task prompt for the TTS subagent (structured input/output contract). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tts-basics.py` | Validate synthesize() output JSON against 02-output-contract schema. | Post-call, before downstream consumes path. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[tts-implementation]] — production layer for long-form, streaming, voice cloning.
- [[voice-basics]] — wraps TTS into a conversational STT→LLM→TTS loop.
- [[structured-output-basics]] — upstream JSON schema enforcement before text reaches TTS.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides provider routing before the synthesize call: SSML markup present → Google or Azure (never OpenAI); voice clone required → ElevenLabs; language not covered by OpenAI (≤30 supported) → Google or ElevenLabs; cost cap below $0.020/1k chars → OpenAI tts-1; default → OpenAI tts-1 with semantic voice map. Use the tree at the routing step inside the synthesize() entry point — before any API call.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tts_basic.py`

```python
"""TTS basics: text_to_speech() for OpenAI + SSMLBuilder for Google/Azure."""
from openai import OpenAI
from pathlib import Path


def text_to_speech(
    text: str,
    output_path: str,
    voice: str = "alloy",
    model: str = "tts-1",
    speed: float = 1.0,
    response_format: str = "mp3",
) -> str:
    """
    Convert text to speech using OpenAI TTS.
    voice: alloy | echo | fable | onyx | nova | shimmer
    model: tts-1 (faster/cheaper) | tts-1-hd (production quality)
    speed: 0.25–4.0 (default 1.0)
    response_format: mp3 | opus | aac | flac | wav | pcm
    """
    client = OpenAI()
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        speed=speed,
        response_format=response_format,
    )
    response.stream_to_file(output_path)
    return output_path


class SSMLBuilder:
    """
    Build SSML markup for Google Cloud or Azure TTS.
    DO NOT pass output to OpenAI TTS — SSML tags are read verbatim by OpenAI.
    """

    def __init__(self):
        self.content = []

    def say(self, text: str) -> "SSMLBuilder":
        self.content.append(text)
        return self

    def pause(self, duration_ms: int) -> "SSMLBuilder":
        self.content.append(f'<break time="{duration_ms}ms"/>')
        return self

    def emphasis(self, text: str, level: str = "moderate") -> "SSMLBuilder":
        """level: strong | moderate | reduced"""
        self.content.append(f'<emphasis level="{level}">{text}</emphasis>')
        return self

    def say_as(self, text: str, interpret_as: str) -> "SSMLBuilder":
        """interpret_as: date | cardinal | characters | ordinal | etc."""
        self.content.append(f'<say-as interpret-as="{interpret_as}">{text}</say-as>')
        return self

    def prosody(
        self,
        text: str,
        rate: str | None = None,
        pitch: str | None = None,
        volume: str | None = None,
    ) -> "SSMLBuilder":
        """rate/pitch/volume: slow|medium|fast or low|medium|high"""
        attrs = []
        if rate:
            attrs.append(f'rate="{rate}"')
        if pitch:
            attrs.append(f'pitch="{pitch}"')
        if volume:
            attrs.append(f'volume="{volume}"')
        attr_str = " ".join(attrs)
        self.content.append(f'<prosody {attr_str}>{text}</prosody>')
        return self

    def build(self) -> str:
        return f'<speak>{"".join(self.content)}</speak>'
```

### `templates/voice-map.py`

```python
"""Semantic voice routing: labels stay portable across providers."""

OPENAI_VOICE_MAP: dict[str, str] = {
    "news": "onyx",       # authoritative male
    "assistant": "nova",  # friendly female
    "narrator": "fable",  # storytelling tone
    "neutral": "alloy",   # balanced default
    "whisper": "shimmer", # soft, gentle
    "formal": "echo",     # neutral male
}

GOOGLE_VOICE_MAP: dict[str, str] = {
    "news": "en-US-Neural2-D",
    "assistant": "en-US-Neural2-F",
    "narrator": "en-US-Neural2-J",
    "neutral": "en-US-Neural2-A",
}


def select_voice(
    content_type: str,
    provider: str = "openai",
) -> str:
    """
    Return provider-specific voice name for a semantic content type.
    Falls back to neutral/alloy if content_type is unknown.
    """
    if provider == "openai":
        return OPENAI_VOICE_MAP.get(content_type, "alloy")
    elif provider == "google":
        return GOOGLE_VOICE_MAP.get(content_type, "en-US-Neural2-A")
    raise ValueError(f"Unknown provider: {provider}")
```

### `templates/prompt-tts.txt`

```text
<task>
Convert text to speech.

Text: {{TEXT}}
Voice type: {{VOICE_TYPE}}  (news|assistant|narrator|neutral|whisper|formal)
Model: {{MODEL}}  (tts-1 for speed, tts-1-hd for production quality)
Speed: {{SPEED}}  (0.25–4.0, default 1.0)
Output path: {{OUTPUT_PATH}}

Rules:
- Preprocess text: strip Markdown/HTML, expand abbreviations (API → A-P-I), replace $ with "dollars"
- Select OpenAI voice from VOICE_TYPE using voice-map.py
- Cache by sha256(text + voice + speed + model) before calling API
- Return cached path if hit

Return JSON:
{"path": "...", "duration_s": N, "cached": true|false}

On error:
{"error": "...", "path": null}
</task>
```
