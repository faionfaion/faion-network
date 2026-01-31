---
id: tts-basics
name: "Text-to-Speech Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Text-to-Speech Basics

Convert text to natural speech using OpenAI TTS, ElevenLabs, and Google Cloud TTS with voice selection and SSML control.

## OpenAI TTS Implementation

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI()

def text_to_speech(
    text: str,
    output_path: str,
    voice: str = "alloy",
    model: str = "tts-1",
    speed: float = 1.0
) -> str:
    """
    Convert text to speech using OpenAI TTS.

    voice: "alloy", "echo", "fable", "onyx", "nova", "shimmer"
    model: "tts-1" (faster), "tts-1-hd" (higher quality)
    speed: 0.25 to 4.0
    response_format: "mp3", "opus", "aac", "flac", "wav", "pcm"
    """
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        speed=speed
    )

    response.stream_to_file(output_path)
    return output_path

# Usage
text_to_speech(
    "Hello, this is a test of text to speech.",
    "output.mp3",
    voice="nova",
    model="tts-1-hd"
)
```

## SSML for Advanced Control

```python
class SSMLBuilder:
    """Build SSML markup for speech synthesis."""

    def __init__(self):
        self.content = []

    def say(self, text: str):
        self.content.append(text)
        return self

    def pause(self, duration_ms: int):
        self.content.append(f'<break time="{duration_ms}ms"/>')
        return self

    def emphasis(self, text: str, level: str = "moderate"):
        """level: strong, moderate, reduced"""
        self.content.append(f'<emphasis level="{level}">{text}</emphasis>')
        return self

    def say_as(self, text: str, interpret_as: str):
        """interpret_as: date, cardinal, characters, etc."""
        self.content.append(f'<say-as interpret-as="{interpret_as}">{text}</say-as>')
        return self

    def prosody(self, text: str, rate: str = None, pitch: str = None, volume: str = None):
        """rate/pitch/volume: slow/medium/fast or low/medium/high"""
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
        content_str = "".join(self.content)
        return f'<speak>{content_str}</speak>'

# Usage
ssml = (
    SSMLBuilder()
    .say("Welcome to our service.")
    .pause(500)
    .prosody("This is important!", pitch="high", rate="slow")
    .pause(300)
    .say("Your order number is ")
    .say_as("12345", "cardinal")
    .build()
)
```

## Best Practices

1. **Voice Selection** - Match voice to content type, consider audience, test multiple voices
2. **Text Preparation** - Clean/normalize text, use SSML for control, handle abbreviations
3. **Quality vs Speed** - Use HD for final content, standard for real-time, consider streaming
4. **Caching** - Cache repeated phrases, use content-based keys, set appropriate TTLs
5. **Cost Management** - Batch requests, use local models for development, monitor usage

## Common Pitfalls

- Missing SSML control over pronunciation
- Voice mismatch with content type
- Exceeding API text limits
- Not caching repeated audio
- Ignoring latency in real-time apps
- Abbreviations read literally

## Sources

- [OpenAI TTS API Documentation](https://platform.openai.com/docs/guides/text-to-speech)
- [OpenAI TTS Voice Samples](https://platform.openai.com/docs/guides/text-to-speech/voice-options)
- [SSML Reference Guide](https://cloud.google.com/text-to-speech/docs/ssml)
- [Google Cloud TTS Documentation](https://cloud.google.com/text-to-speech/docs)
- [ElevenLabs Documentation](https://elevenlabs.io/docs)
