"""
TTS basics: text_to_speech() for OpenAI + SSMLBuilder for Google/Azure.
SSMLBuilder output is NOT compatible with OpenAI TTS — route SSML to Google/Azure only.
"""
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
