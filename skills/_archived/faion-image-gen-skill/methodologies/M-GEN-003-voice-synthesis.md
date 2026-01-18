# M-GEN-003: Voice Synthesis

## Overview

Voice synthesis (Text-to-Speech) converts text into natural-sounding speech. Modern systems support voice cloning, emotional control, and multilingual synthesis. Key providers include ElevenLabs, OpenAI TTS, and Play.ht.

**When to use:** Creating voiceovers, audiobooks, podcasts, virtual assistants, or accessibility features.

## Core Concepts

### 1. TTS Provider Comparison

| Provider | Strengths | Voices | Cloning | Pricing |
|----------|-----------|--------|---------|---------|
| **ElevenLabs** | Most natural | 100+ | Yes | $5-330/mo |
| **OpenAI TTS** | Good quality, cheap | 6 | No | $15/1M chars |
| **Play.ht** | Good cloning | 600+ | Yes | $31-99/mo |
| **Microsoft Azure** | Enterprise, many langs | 400+ | Yes | Pay per char |
| **Google Cloud TTS** | Reliable, scalable | 200+ | No | Pay per char |
| **Amazon Polly** | AWS integration | 60+ | No | Pay per char |

### 2. Key Voice Parameters

| Parameter | Description | Effect |
|-----------|-------------|--------|
| **Stability** | Voice consistency | Higher = more consistent |
| **Similarity** | Clone accuracy | Higher = closer to original |
| **Style** | Emotional expression | Affects delivery |
| **Speed** | Speaking rate | 0.5x to 2.0x |
| **Pitch** | Voice height | Lower/higher tone |

### 3. Voice Styles

| Style | Use Case | Description |
|-------|----------|-------------|
| **Conversational** | Assistants, chatbots | Natural, friendly |
| **Narrative** | Audiobooks, stories | Expressive, engaging |
| **Professional** | Corporate, training | Clear, authoritative |
| **Newscaster** | News, announcements | Formal, broadcast |
| **Whisper** | ASMR, intimate | Soft, close |

## Best Practices

### 1. Choose Appropriate Voice

```python
def select_voice(content_type: str, audience: str, language: str) -> dict:
    """Select appropriate voice for content."""

    voice_mapping = {
        ("marketing", "professional", "en"): {
            "provider": "elevenlabs",
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
            "style": "professional",
            "stability": 0.75,
            "similarity": 0.85
        },
        ("audiobook", "general", "en"): {
            "provider": "elevenlabs",
            "voice_id": "pNInz6obpgDQGcFmaJgB",  # Adam
            "style": "narrative",
            "stability": 0.65,
            "similarity": 0.8
        },
        ("assistant", "casual", "en"): {
            "provider": "openai",
            "voice": "alloy",
            "speed": 1.0
        },
        ("news", "formal", "en"): {
            "provider": "azure",
            "voice": "en-US-JennyNeural",
            "style": "newscast"
        }
    }

    key = (content_type, audience, language)
    return voice_mapping.get(key, voice_mapping[("assistant", "casual", "en")])
```

### 2. Prepare Text for Speech

```python
import re

def prepare_text_for_tts(text: str) -> str:
    """Prepare text for natural speech synthesis."""

    # Expand abbreviations
    abbreviations = {
        "e.g.": "for example",
        "i.e.": "that is",
        "etc.": "et cetera",
        "Dr.": "Doctor",
        "Mr.": "Mister",
        "Mrs.": "Missus",
        "vs.": "versus",
        "approx.": "approximately"
    }

    for abbr, full in abbreviations.items():
        text = text.replace(abbr, full)

    # Handle numbers
    text = re.sub(r'\$(\d+)', r'\1 dollars', text)
    text = re.sub(r'(\d+)%', r'\1 percent', text)

    # Add pauses with punctuation
    text = text.replace("...", "... ")
    text = text.replace(" - ", ", ")

    # Clean up
    text = re.sub(r'\s+', ' ', text).strip()

    return text
```

### 3. Add SSML for Control

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis">
    <voice name="en-US-JennyNeural">
        <prosody rate="medium" pitch="medium">
            Welcome to our product demo.
        </prosody>

        <break time="500ms"/>

        <emphasis level="strong">Key features include:</emphasis>

        <break time="300ms"/>

        <p>
            <s>First, seamless integration.</s>
            <s>Second, powerful analytics.</s>
            <s>Third, enterprise security.</s>
        </p>

        <prosody rate="slow" pitch="low">
            Thank you for watching.
        </prosody>
    </voice>
</speak>
```

## Common Patterns

### Pattern 1: OpenAI TTS

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI()

def generate_speech(
    text: str,
    voice: str = "alloy",
    model: str = "tts-1-hd",
    output_path: str = "output.mp3"
) -> str:
    """Generate speech using OpenAI TTS."""

    response = client.audio.speech.create(
        model=model,  # "tts-1" (fast) or "tts-1-hd" (quality)
        voice=voice,  # alloy, echo, fable, onyx, nova, shimmer
        input=text,
        speed=1.0  # 0.25 to 4.0
    )

    response.stream_to_file(output_path)
    return output_path

# Available voices
voices = {
    "alloy": "Neutral, balanced",
    "echo": "Male, warm",
    "fable": "Narrative, expressive",
    "onyx": "Male, deep",
    "nova": "Female, friendly",
    "shimmer": "Female, soft"
}
```

### Pattern 2: ElevenLabs Advanced

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="your-api-key")

def generate_elevenlabs_speech(
    text: str,
    voice_id: str,
    stability: float = 0.5,
    similarity: float = 0.75,
    style: float = 0.0,
    output_path: str = "output.mp3"
) -> str:
    """Generate high-quality speech with ElevenLabs."""

    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings={
            "stability": stability,
            "similarity_boost": similarity,
            "style": style,
            "use_speaker_boost": True
        }
    )

    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return output_path

# Voice cloning
def clone_voice(
    name: str,
    audio_files: list[str],
    description: str = ""
) -> str:
    """Clone a voice from audio samples."""

    voice = client.voices.clone(
        name=name,
        description=description,
        files=[open(f, "rb") for f in audio_files],
        labels={"accent": "american", "gender": "male"}
    )

    return voice.voice_id
```

### Pattern 3: Long-Form Content

```python
def generate_audiobook_chapter(
    chapter_text: str,
    voice_config: dict,
    max_chunk_size: int = 5000
) -> str:
    """Generate audiobook chapter with consistent quality."""

    # Split into chunks at sentence boundaries
    chunks = split_text_at_sentences(chapter_text, max_chunk_size)

    audio_files = []

    for i, chunk in enumerate(chunks):
        # Prepare text
        prepared = prepare_text_for_tts(chunk)

        # Generate audio
        output = f"chapter_part_{i}.mp3"
        generate_elevenlabs_speech(
            text=prepared,
            voice_id=voice_config["voice_id"],
            stability=voice_config.get("stability", 0.65),
            similarity=voice_config.get("similarity", 0.8),
            output_path=output
        )

        audio_files.append(output)

    # Concatenate with crossfade
    final_audio = concatenate_audio_files(audio_files, crossfade_ms=100)

    return final_audio

def split_text_at_sentences(text: str, max_size: int) -> list:
    """Split text at sentence boundaries."""
    import nltk
    nltk.download('punkt', quiet=True)

    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_size:
            current_chunk += " " + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
```

### Pattern 4: Multilingual Synthesis

```python
def generate_multilingual_content(
    text: str,
    target_languages: list[str],
    base_voice: str = "multilingual"
) -> dict:
    """Generate same content in multiple languages."""

    results = {}

    # ElevenLabs multilingual model
    for lang in target_languages:
        # Translate text
        translated = translate_text(text, target_lang=lang)

        # Generate speech
        audio_path = generate_elevenlabs_speech(
            text=translated,
            voice_id=get_voice_for_language(base_voice, lang),
            output_path=f"output_{lang}.mp3"
        )

        results[lang] = {
            "text": translated,
            "audio": audio_path
        }

    return results

def get_voice_for_language(base_voice: str, language: str) -> str:
    """Get appropriate voice for language."""
    # ElevenLabs multilingual voices work across languages
    # Or use language-specific voices
    language_voices = {
        "en": "21m00Tcm4TlvDq8ikWAM",  # Rachel
        "es": "pNInz6obpgDQGcFmaJgB",  # Adam (multilingual)
        "fr": "pNInz6obpgDQGcFmaJgB",
        "de": "pNInz6obpgDQGcFmaJgB",
    }
    return language_voices.get(language, language_voices["en"])
```

### Pattern 5: Real-time Streaming

```python
import asyncio
import websockets

async def stream_tts(text: str, voice_id: str):
    """Stream TTS for real-time applications."""

    url = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    async with websockets.connect(url) as ws:
        # Send configuration
        await ws.send(json.dumps({
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }))

        # Receive audio chunks
        while True:
            try:
                chunk = await ws.recv()
                if isinstance(chunk, bytes):
                    yield chunk
            except websockets.exceptions.ConnectionClosed:
                break

# Usage in async context
async def play_streaming_audio(text: str):
    import pyaudio

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)

    async for chunk in stream_tts(text, "voice_id"):
        stream.write(chunk)

    stream.stop_stream()
    stream.close()
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Raw text input | Unnatural pronunciation | Prepare text, use SSML |
| Ignoring pacing | Rushed or slow speech | Add pauses, adjust speed |
| Wrong voice for content | Mismatched tone | Match voice to content type |
| No quality check | Poor pronunciation | Review and iterate |
| Single long generation | Memory/timeout issues | Chunk and concatenate |

## Tools & References

### Related Skills
- faion-audio-skill
- faion-openai-api-skill

### Related Agents
- faion-tts-agent
- faion-voice-agent-builder-agent

### External Resources
- [ElevenLabs](https://elevenlabs.io/)
- [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech)
- [Play.ht](https://play.ht/)
- [SSML Reference](https://www.w3.org/TR/speech-synthesis11/)

## Checklist

- [ ] Selected appropriate TTS provider
- [ ] Chose voice matching content type
- [ ] Prepared text for speech
- [ ] Added SSML for control (if needed)
- [ ] Configured voice parameters
- [ ] Generated audio in chunks
- [ ] Reviewed pronunciation
- [ ] Concatenated with proper pacing
- [ ] Exported in target format
- [ ] Tested across devices

---

*Methodology: M-GEN-003 | Category: Multimodal/Generation*
*Related: faion-tts-agent, faion-audio-skill*
