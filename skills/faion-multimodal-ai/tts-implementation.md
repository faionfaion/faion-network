---
id: tts-implementation
name: "Text-to-Speech Implementation"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Text-to-Speech Implementation

Production TTS implementations with ElevenLabs, Google Cloud, streaming, and long text processing.

## ElevenLabs Integration

```python
from elevenlabs import ElevenLabs, Voice, VoiceSettings

def elevenlabs_tts(
    text: str,
    output_path: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    stability: float = 0.5,
    similarity_boost: float = 0.75
) -> str:
    """Generate speech using ElevenLabs."""
    client = ElevenLabs()

    audio = client.generate(
        text=text,
        voice=Voice(
            voice_id=voice_id,
            settings=VoiceSettings(
                stability=stability,
                similarity_boost=similarity_boost,
                style=0.5,
                use_speaker_boost=True
            )
        ),
        model="eleven_multilingual_v2"
    )

    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return output_path

def clone_voice(audio_samples: list[str], name: str, description: str = "") -> str:
    """Clone a voice from audio samples."""
    client = ElevenLabs()
    voice = client.clone(name=name, description=description, files=audio_samples)
    return voice.voice_id
```

## Google Cloud TTS

```python
from google.cloud import texttospeech

def google_tts(
    text: str,
    output_path: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Neural2-D",
    speaking_rate: float = 1.0,
    pitch: float = 0.0
) -> str:
    """Generate speech using Google Cloud TTS."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
        pitch=pitch
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(output_path, "wb") as f:
        f.write(response.audio_content)

    return output_path
```

## Long Text Processing

```python
from typing import List
import re

class LongTextTTS:
    """Handle long text for TTS with chunking."""

    def __init__(self, max_chars: int = 4096, overlap_chars: int = 50):
        self.max_chars = max_chars
        self.overlap_chars = overlap_chars
        self.client = OpenAI()

    def synthesize(self, text: str, output_path: str, voice: str = "alloy") -> str:
        """Synthesize long text with automatic chunking."""
        from pydub import AudioSegment

        chunks = self._split_text(text)
        audio_segments = []

        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i + 1}/{len(chunks)}")

            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=chunk
            )

            temp_path = f"/tmp/chunk_{i}.mp3"
            response.stream_to_file(temp_path)
            audio_segments.append(AudioSegment.from_mp3(temp_path))

        # Combine audio
        combined = audio_segments[0]
        for segment in audio_segments[1:]:
            combined += segment

        combined.export(output_path, format="mp3")

        # Cleanup
        import os
        for i in range(len(chunks)):
            os.remove(f"/tmp/chunk_{i}.mp3")

        return output_path

    def _split_text(self, text: str) -> List[str]:
        """Split text at sentence boundaries."""
        chunks = []
        current_chunk = ""

        sentences = re.split(r'(?<=[.!?])\s+', text)

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.max_chars:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
```

## Real-time Streaming

```python
import asyncio
from typing import AsyncGenerator

async def stream_tts(text: str, voice: str = "alloy") -> AsyncGenerator[bytes, None]:
    """Stream TTS audio in real-time."""
    client = OpenAI()

    async with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="pcm"
    ) as response:
        async for chunk in response.iter_bytes():
            yield chunk

async def stream_to_speaker(text: str):
    """Stream directly to speakers using pyaudio."""
    import pyaudio

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=24000,
        output=True
    )

    async for chunk in stream_tts(text):
        stream.write(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()
```

## Production TTS Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from pathlib import Path
from enum import Enum
import logging
import hashlib

class TTSProvider(Enum):
    OPENAI = "openai"
    ELEVENLABS = "elevenlabs"
    GOOGLE = "google"

@dataclass
class TTSConfig:
    provider: TTSProvider = TTSProvider.OPENAI
    default_voice: str = "alloy"
    default_speed: float = 1.0
    output_format: str = "mp3"
    cache_enabled: bool = True
    cache_dir: str = "./tts_cache"
    max_text_length: int = 4096

class TTSService:
    """Production text-to-speech service."""

    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config or TTSConfig()
        self.logger = logging.getLogger(__name__)

        if self.config.cache_enabled:
            Path(self.config.cache_dir).mkdir(exist_ok=True)

        self._init_provider()

    def _init_provider(self):
        if self.config.provider == TTSProvider.OPENAI:
            self.client = OpenAI()

    def synthesize(
        self,
        text: str,
        output_path: Optional[str] = None,
        voice: Optional[str] = None,
        speed: Optional[float] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Synthesize speech from text."""
        voice = voice or self.config.default_voice
        speed = speed or self.config.default_speed

        # Check cache
        if use_cache and self.config.cache_enabled:
            cached_path = self._get_cached(text, voice, speed)
            if cached_path:
                self.logger.info("Cache hit")
                return {"success": True, "path": cached_path, "cached": True}

        # Validate text length
        if len(text) > self.config.max_text_length:
            return self._synthesize_long(text, output_path, voice, speed)

        try:
            audio_path = self._synthesize_openai(text, output_path, voice, speed)

            if self.config.cache_enabled:
                self._cache_audio(text, voice, speed, audio_path)

            return {
                "success": True,
                "path": audio_path,
                "cached": False,
                "duration": self._get_duration(audio_path)
            }

        except Exception as e:
            self.logger.error(f"TTS failed: {e}")
            return {"success": False, "error": str(e)}

    def _synthesize_openai(self, text: str, output_path: Optional[str], voice: str, speed: float) -> str:
        response = self.client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text,
            speed=speed,
            response_format=self.config.output_format
        )

        output_path = output_path or f"/tmp/tts_{hash(text)}.{self.config.output_format}"
        response.stream_to_file(output_path)
        return output_path

    def _synthesize_long(self, text: str, output_path: Optional[str], voice: str, speed: float) -> Dict:
        processor = LongTextTTS(max_chars=self.config.max_text_length)
        output_path = output_path or f"/tmp/tts_long_{hash(text)}.mp3"
        result_path = processor.synthesize(text, output_path, voice)

        return {"success": True, "path": result_path, "cached": False}

    def _get_cache_key(self, text: str, voice: str, speed: float) -> str:
        content = f"{text}|{voice}|{speed}|{self.config.provider.value}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _get_cached(self, text: str, voice: str, speed: float) -> Optional[str]:
        key = self._get_cache_key(text, voice, speed)
        cache_path = Path(self.config.cache_dir) / f"{key}.{self.config.output_format}"

        if cache_path.exists():
            return str(cache_path)
        return None

    def _cache_audio(self, text: str, voice: str, speed: float, audio_path: str):
        import shutil
        key = self._get_cache_key(text, voice, speed)
        cache_path = Path(self.config.cache_dir) / f"{key}.{self.config.output_format}"
        shutil.copy(audio_path, cache_path)

    def _get_duration(self, audio_path: str) -> float:
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0
        except:
            return 0.0
```

## Sources

- [OpenAI TTS API Documentation](https://platform.openai.com/docs/guides/text-to-speech)
- [ElevenLabs API Documentation](https://elevenlabs.io/docs/api-reference/text-to-speech)
- [Google Cloud TTS Documentation](https://cloud.google.com/text-to-speech/docs)
- [pydub Audio Processing](https://github.com/jiaaro/pydub)
