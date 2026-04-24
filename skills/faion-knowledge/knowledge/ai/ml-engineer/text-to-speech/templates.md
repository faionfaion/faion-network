# Text-to-Speech Templates

## Production TTS Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from pathlib import Path
from enum import Enum
import logging
import hashlib
import shutil
from abc import ABC, abstractmethod

class TTSProvider(Enum):
    OPENAI = "openai"
    ELEVENLABS = "elevenlabs"
    GOOGLE = "google"
    AZURE = "azure"

@dataclass
class Voice:
    id: str
    name: str
    provider: TTSProvider
    language: str = "en"
    gender: str = "neutral"

@dataclass
class TTSConfig:
    provider: TTSProvider = TTSProvider.OPENAI
    default_voice: str = "nova"
    default_speed: float = 1.0
    output_format: str = "mp3"
    cache_enabled: bool = True
    cache_dir: str = "./tts_cache"
    max_text_length: int = 4096

@dataclass
class TTSResult:
    success: bool
    path: Optional[str] = None
    duration: float = 0.0
    cached: bool = False
    error: Optional[str] = None
    characters: int = 0

class TTSProviderBase(ABC):
    """Abstract base class for TTS providers."""

    @abstractmethod
    def synthesize(
        self,
        text: str,
        output_path: str,
        voice: str,
        speed: float,
        **kwargs
    ) -> str:
        pass

    @abstractmethod
    def get_voices(self) -> List[Voice]:
        pass

class OpenAITTSProvider(TTSProviderBase):
    """OpenAI TTS implementation."""

    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI()

    def synthesize(
        self,
        text: str,
        output_path: str,
        voice: str = "nova",
        speed: float = 1.0,
        model: str = "tts-1-hd",
        response_format: str = "mp3",
        **kwargs
    ) -> str:
        response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            speed=speed,
            response_format=response_format
        )
        response.stream_to_file(output_path)
        return output_path

    def get_voices(self) -> List[Voice]:
        return [
            Voice("alloy", "Alloy", TTSProvider.OPENAI, "en", "neutral"),
            Voice("echo", "Echo", TTSProvider.OPENAI, "en", "male"),
            Voice("fable", "Fable", TTSProvider.OPENAI, "en", "neutral"),
            Voice("onyx", "Onyx", TTSProvider.OPENAI, "en", "male"),
            Voice("nova", "Nova", TTSProvider.OPENAI, "en", "female"),
            Voice("shimmer", "Shimmer", TTSProvider.OPENAI, "en", "female"),
        ]

class ElevenLabsTTSProvider(TTSProviderBase):
    """ElevenLabs TTS implementation."""

    def __init__(self):
        from elevenlabs import ElevenLabs
        self.client = ElevenLabs()

    def synthesize(
        self,
        text: str,
        output_path: str,
        voice: str = "21m00Tcm4TlvDq8ikWAM",
        speed: float = 1.0,
        model: str = "eleven_multilingual_v2",
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        **kwargs
    ) -> str:
        from elevenlabs.client import VoiceSettings

        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=voice,
            model_id=model,
            voice_settings=VoiceSettings(
                stability=stability,
                similarity_boost=similarity_boost,
                style=0.5,
                use_speaker_boost=True
            )
        )

        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        return output_path

    def get_voices(self) -> List[Voice]:
        response = self.client.voices.get_all()
        return [
            Voice(
                v.voice_id,
                v.name,
                TTSProvider.ELEVENLABS,
                v.labels.get("language", "en") if v.labels else "en",
                v.labels.get("gender", "neutral") if v.labels else "neutral"
            )
            for v in response.voices
        ]

class TTSService:
    """Production text-to-speech service with caching and multi-provider support."""

    PROVIDERS = {
        TTSProvider.OPENAI: OpenAITTSProvider,
        TTSProvider.ELEVENLABS: ElevenLabsTTSProvider,
    }

    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config or TTSConfig()
        self.logger = logging.getLogger(__name__)

        if self.config.cache_enabled:
            Path(self.config.cache_dir).mkdir(exist_ok=True)

        self._init_provider()

    def _init_provider(self):
        """Initialize TTS provider."""
        provider_class = self.PROVIDERS.get(self.config.provider)
        if not provider_class:
            raise ValueError(f"Unsupported provider: {self.config.provider}")
        self.provider = provider_class()

    def synthesize(
        self,
        text: str,
        output_path: Optional[str] = None,
        voice: Optional[str] = None,
        speed: Optional[float] = None,
        use_cache: bool = True,
        **kwargs
    ) -> TTSResult:
        """Synthesize speech from text."""
        voice = voice or self.config.default_voice
        speed = speed or self.config.default_speed

        # Check cache
        if use_cache and self.config.cache_enabled:
            cached_path = self._get_cached(text, voice, speed)
            if cached_path:
                self.logger.info("Cache hit for TTS request")
                return TTSResult(
                    success=True,
                    path=cached_path,
                    cached=True,
                    characters=len(text),
                    duration=self._get_duration(cached_path)
                )

        # Validate text length
        if len(text) > self.config.max_text_length:
            return self._synthesize_long(text, output_path, voice, speed, **kwargs)

        try:
            # Generate output path if not provided
            if output_path is None:
                output_path = f"/tmp/tts_{hash(text)}.{self.config.output_format}"

            # Synthesize
            audio_path = self.provider.synthesize(
                text=text,
                output_path=output_path,
                voice=voice,
                speed=speed,
                **kwargs
            )

            # Cache if enabled
            if self.config.cache_enabled:
                self._cache_audio(text, voice, speed, audio_path)

            return TTSResult(
                success=True,
                path=audio_path,
                cached=False,
                characters=len(text),
                duration=self._get_duration(audio_path)
            )

        except Exception as e:
            self.logger.error(f"TTS synthesis failed: {e}")
            return TTSResult(success=False, error=str(e))

    def _synthesize_long(
        self,
        text: str,
        output_path: Optional[str],
        voice: str,
        speed: float,
        **kwargs
    ) -> TTSResult:
        """Handle long text with chunking."""
        from pydub import AudioSegment
        import tempfile
        import os
        import re

        chunks = self._split_text(text)
        audio_segments = []
        total_chars = 0

        try:
            for i, chunk in enumerate(chunks):
                self.logger.info(f"Processing chunk {i + 1}/{len(chunks)}")

                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    temp_path = f.name

                self.provider.synthesize(
                    text=chunk,
                    output_path=temp_path,
                    voice=voice,
                    speed=speed,
                    **kwargs
                )

                audio_segments.append((temp_path, AudioSegment.from_mp3(temp_path)))
                total_chars += len(chunk)

            # Combine audio
            combined = audio_segments[0][1]
            for _, segment in audio_segments[1:]:
                combined += segment

            # Export
            if output_path is None:
                output_path = f"/tmp/tts_long_{hash(text)}.mp3"

            combined.export(output_path, format="mp3")

            return TTSResult(
                success=True,
                path=output_path,
                cached=False,
                characters=total_chars,
                duration=len(combined) / 1000.0
            )

        finally:
            # Cleanup temp files
            for temp_path, _ in audio_segments:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    def _split_text(self, text: str) -> List[str]:
        """Split text at sentence boundaries."""
        import re

        chunks = []
        current_chunk = ""
        sentences = re.split(r'(?<=[.!?])\s+', text)

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.config.max_text_length:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _get_cache_key(self, text: str, voice: str, speed: float) -> str:
        """Generate cache key."""
        content = f"{text}|{voice}|{speed}|{self.config.provider.value}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _get_cached(self, text: str, voice: str, speed: float) -> Optional[str]:
        """Get cached audio file."""
        key = self._get_cache_key(text, voice, speed)
        cache_path = Path(self.config.cache_dir) / f"{key}.{self.config.output_format}"

        if cache_path.exists():
            return str(cache_path)
        return None

    def _cache_audio(self, text: str, voice: str, speed: float, audio_path: str):
        """Cache audio file."""
        key = self._get_cache_key(text, voice, speed)
        cache_path = Path(self.config.cache_dir) / f"{key}.{self.config.output_format}"
        shutil.copy(audio_path, cache_path)

    def _get_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds."""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0
        except Exception:
            return 0.0

    def get_available_voices(self) -> List[Voice]:
        """Get available voices for current provider."""
        return self.provider.get_voices()

    def clear_cache(self):
        """Clear all cached files."""
        cache_dir = Path(self.config.cache_dir)
        for f in cache_dir.glob(f"*.{self.config.output_format}"):
            f.unlink()

# Usage example
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # OpenAI TTS
    service = TTSService(TTSConfig(
        provider=TTSProvider.OPENAI,
        default_voice="nova",
        cache_enabled=True
    ))

    result = service.synthesize(
        "Hello, this is a test of the production TTS service.",
        voice="nova"
    )

    if result.success:
        print(f"Audio saved to: {result.path}")
        print(f"Duration: {result.duration:.2f}s")
        print(f"Characters: {result.characters}")
        print(f"Cached: {result.cached}")
    else:
        print(f"Error: {result.error}")
```

## FastAPI TTS Endpoint

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional
import asyncio
from openai import AsyncOpenAI

app = FastAPI(title="TTS API")
async_client = AsyncOpenAI()

class TTSRequest(BaseModel):
    text: str = Field(..., max_length=4096)
    voice: str = Field(default="nova", pattern="^(alloy|echo|fable|onyx|nova|shimmer)$")
    speed: float = Field(default=1.0, ge=0.25, le=4.0)
    model: str = Field(default="tts-1", pattern="^(tts-1|tts-1-hd)$")
    format: str = Field(default="mp3", pattern="^(mp3|opus|aac|flac|wav|pcm)$")

class TTSResponse(BaseModel):
    success: bool
    file_id: str
    duration: float
    characters: int

@app.post("/v1/tts", response_model=TTSResponse)
async def create_tts(request: TTSRequest, background_tasks: BackgroundTasks):
    """Generate TTS audio file."""
    import tempfile
    import uuid

    file_id = str(uuid.uuid4())
    output_path = f"/tmp/tts_{file_id}.{request.format}"

    try:
        response = await async_client.audio.speech.create(
            model=request.model,
            voice=request.voice,
            input=request.text,
            speed=request.speed,
            response_format=request.format
        )

        with open(output_path, "wb") as f:
            async for chunk in response.iter_bytes():
                f.write(chunk)

        # Schedule cleanup after 1 hour
        background_tasks.add_task(cleanup_file, output_path, delay=3600)

        return TTSResponse(
            success=True,
            file_id=file_id,
            duration=0.0,  # Calculate if needed
            characters=len(request.text)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/tts/{file_id}")
async def get_tts_file(file_id: str, format: str = "mp3"):
    """Download TTS audio file."""
    file_path = f"/tmp/tts_{file_id}.{format}"

    if not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path,
        media_type=f"audio/{format}",
        filename=f"speech.{format}"
    )

@app.get("/v1/tts/stream")
async def stream_tts(
    text: str,
    voice: str = "nova",
    speed: float = 1.0
):
    """Stream TTS audio in real-time."""
    async def generate():
        async with async_client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice=voice,
            input=text,
            speed=speed,
            response_format="mp3"
        ) as response:
            async for chunk in response.iter_bytes(chunk_size=1024):
                yield chunk

    return StreamingResponse(
        generate(),
        media_type="audio/mpeg",
        headers={"Transfer-Encoding": "chunked"}
    )

async def cleanup_file(path: str, delay: int):
    """Cleanup temporary file after delay."""
    await asyncio.sleep(delay)
    if Path(path).exists():
        Path(path).unlink()

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "tts"}
```

## Voice Cloning Service

```python
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
from elevenlabs import ElevenLabs
from elevenlabs.client import VoiceSettings
import logging

@dataclass
class VoiceCloneConfig:
    name: str
    description: str = ""
    labels: dict = None
    remove_background_noise: bool = True

@dataclass
class ClonedVoice:
    voice_id: str
    name: str
    created: bool
    samples_used: int

class VoiceCloningService:
    """Service for managing voice cloning with ElevenLabs."""

    def __init__(self):
        self.client = ElevenLabs()
        self.logger = logging.getLogger(__name__)

    def clone_instant(
        self,
        audio_files: List[str],
        config: VoiceCloneConfig
    ) -> ClonedVoice:
        """
        Create instant voice clone from audio samples.

        Requirements:
        - Minimum 30 seconds of audio
        - Clean audio, minimal background noise
        - Consistent speaking style
        """
        if not audio_files:
            raise ValueError("At least one audio file is required")

        self.logger.info(f"Creating instant clone: {config.name}")

        voice = self.client.voices.add(
            name=config.name,
            description=config.description,
            files=audio_files,
            labels=config.labels or {},
            remove_background_noise=config.remove_background_noise
        )

        return ClonedVoice(
            voice_id=voice.voice_id,
            name=voice.name,
            created=True,
            samples_used=len(audio_files)
        )

    def get_voice(self, voice_id: str):
        """Get voice details."""
        return self.client.voices.get(voice_id)

    def delete_voice(self, voice_id: str) -> bool:
        """Delete a cloned voice."""
        try:
            self.client.voices.delete(voice_id)
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete voice: {e}")
            return False

    def list_cloned_voices(self) -> List[ClonedVoice]:
        """List all cloned voices."""
        response = self.client.voices.get_all()
        return [
            ClonedVoice(
                voice_id=v.voice_id,
                name=v.name,
                created=False,
                samples_used=len(v.samples) if v.samples else 0
            )
            for v in response.voices
            if v.category == "cloned"
        ]

    def synthesize_with_clone(
        self,
        text: str,
        voice_id: str,
        output_path: str,
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        style: float = 0.0
    ) -> str:
        """Synthesize speech using cloned voice."""
        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=stability,
                similarity_boost=similarity_boost,
                style=style,
                use_speaker_boost=True
            )
        )

        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        return output_path

# Usage
if __name__ == "__main__":
    service = VoiceCloningService()

    # Clone voice
    voice = service.clone_instant(
        audio_files=["sample1.mp3", "sample2.mp3"],
        config=VoiceCloneConfig(
            name="My Custom Voice",
            description="Professional narrator voice",
            labels={"accent": "american", "gender": "male"}
        )
    )

    print(f"Created voice: {voice.voice_id}")

    # Use cloned voice
    service.synthesize_with_clone(
        text="This is my cloned voice speaking.",
        voice_id=voice.voice_id,
        output_path="cloned_speech.mp3"
    )
```

## Multi-Provider TTS Router

```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from enum import Enum
import logging

class UseCase(Enum):
    REALTIME = "realtime"
    NARRATION = "narration"
    AUDIOBOOK = "audiobook"
    ACCESSIBILITY = "accessibility"
    VOICE_ASSISTANT = "voice_assistant"
    PODCAST = "podcast"

@dataclass
class ProviderConfig:
    provider: str
    model: str
    voice: str
    kwargs: dict = None

class TTSRouter:
    """Route TTS requests to optimal provider based on use case."""

    # Default routing table
    ROUTING_TABLE: Dict[UseCase, ProviderConfig] = {
        UseCase.REALTIME: ProviderConfig(
            provider="elevenlabs",
            model="eleven_flash_v2_5",
            voice="21m00Tcm4TlvDq8ikWAM",
            kwargs={"output_format": "pcm_24000"}
        ),
        UseCase.NARRATION: ProviderConfig(
            provider="elevenlabs",
            model="eleven_multilingual_v2",
            voice="21m00Tcm4TlvDq8ikWAM",
            kwargs={"stability": 0.6, "similarity_boost": 0.8}
        ),
        UseCase.AUDIOBOOK: ProviderConfig(
            provider="elevenlabs",
            model="eleven_multilingual_v2",
            voice="EXAVITQu4vr4xnSDxMaL",
            kwargs={"stability": 0.7, "style": 0.3}
        ),
        UseCase.ACCESSIBILITY: ProviderConfig(
            provider="openai",
            model="tts-1",
            voice="nova",
            kwargs={"speed": 0.9}
        ),
        UseCase.VOICE_ASSISTANT: ProviderConfig(
            provider="openai",
            model="tts-1",
            voice="alloy",
            kwargs={"response_format": "pcm"}
        ),
        UseCase.PODCAST: ProviderConfig(
            provider="openai",
            model="tts-1-hd",
            voice="onyx",
            kwargs={"speed": 0.95}
        ),
    }

    def __init__(self, providers: Dict[str, Callable] = None):
        self.logger = logging.getLogger(__name__)
        self.providers = providers or {}

        # Initialize default providers
        self._init_default_providers()

    def _init_default_providers(self):
        """Initialize default provider implementations."""
        try:
            from openai import OpenAI
            openai_client = OpenAI()

            def openai_synthesize(text, output_path, **kwargs):
                response = openai_client.audio.speech.create(
                    input=text,
                    **kwargs
                )
                response.stream_to_file(output_path)
                return output_path

            self.providers["openai"] = openai_synthesize
        except ImportError:
            self.logger.warning("OpenAI not available")

        try:
            from elevenlabs import ElevenLabs
            elevenlabs_client = ElevenLabs()

            def elevenlabs_synthesize(text, output_path, voice_id, **kwargs):
                audio = elevenlabs_client.text_to_speech.convert(
                    text=text,
                    voice_id=voice_id,
                    **kwargs
                )
                with open(output_path, "wb") as f:
                    for chunk in audio:
                        f.write(chunk)
                return output_path

            self.providers["elevenlabs"] = elevenlabs_synthesize
        except ImportError:
            self.logger.warning("ElevenLabs not available")

    def synthesize(
        self,
        text: str,
        use_case: UseCase,
        output_path: str,
        override_config: Optional[ProviderConfig] = None
    ) -> str:
        """Synthesize speech using optimal provider for use case."""
        config = override_config or self.ROUTING_TABLE.get(use_case)

        if not config:
            raise ValueError(f"No configuration for use case: {use_case}")

        provider_fn = self.providers.get(config.provider)
        if not provider_fn:
            raise ValueError(f"Provider not available: {config.provider}")

        kwargs = {
            "model": config.model,
            "voice": config.voice,
            **(config.kwargs or {})
        }

        # Adjust for ElevenLabs voice_id vs OpenAI voice
        if config.provider == "elevenlabs":
            kwargs["voice_id"] = kwargs.pop("voice")
            kwargs["model_id"] = kwargs.pop("model")

        return provider_fn(text, output_path, **kwargs)

    def get_recommended_config(self, use_case: UseCase) -> ProviderConfig:
        """Get recommended configuration for use case."""
        return self.ROUTING_TABLE.get(use_case)

# Usage
if __name__ == "__main__":
    router = TTSRouter()

    # Real-time conversation
    router.synthesize(
        "Hello! How can I help you?",
        UseCase.REALTIME,
        "realtime_output.pcm"
    )

    # Audiobook narration
    router.synthesize(
        "Chapter One. It was a dark and stormy night...",
        UseCase.AUDIOBOOK,
        "audiobook_output.mp3"
    )
```

## Text Preprocessor

```python
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class PreprocessConfig:
    expand_abbreviations: bool = True
    expand_numbers: bool = True
    normalize_punctuation: bool = True
    max_chunk_length: int = 4096

class TextPreprocessor:
    """Preprocess text for optimal TTS synthesis."""

    # Common abbreviations
    ABBREVIATIONS = {
        "Dr.": "Doctor",
        "Mr.": "Mister",
        "Mrs.": "Misses",
        "Ms.": "Miz",
        "Prof.": "Professor",
        "Jr.": "Junior",
        "Sr.": "Senior",
        "vs.": "versus",
        "etc.": "etcetera",
        "e.g.": "for example",
        "i.e.": "that is",
        "St.": "Street",
        "Ave.": "Avenue",
        "Blvd.": "Boulevard",
        "Mt.": "Mount",
        "ft.": "feet",
        "lb.": "pounds",
        "oz.": "ounces",
        "Jan.": "January",
        "Feb.": "February",
        "Mar.": "March",
        "Apr.": "April",
        "Aug.": "August",
        "Sept.": "September",
        "Oct.": "October",
        "Nov.": "November",
        "Dec.": "December",
    }

    def __init__(self, config: PreprocessConfig = None):
        self.config = config or PreprocessConfig()

    def process(self, text: str) -> str:
        """Full preprocessing pipeline."""
        if self.config.expand_abbreviations:
            text = self._expand_abbreviations(text)

        if self.config.expand_numbers:
            text = self._expand_numbers(text)

        if self.config.normalize_punctuation:
            text = self._normalize_punctuation(text)

        return text.strip()

    def chunk(self, text: str) -> List[str]:
        """Split text into TTS-friendly chunks."""
        text = self.process(text)
        return self._split_at_sentences(text, self.config.max_chunk_length)

    def _expand_abbreviations(self, text: str) -> str:
        """Expand common abbreviations."""
        for abbr, expansion in self.ABBREVIATIONS.items():
            text = text.replace(abbr, expansion)
        return text

    def _expand_numbers(self, text: str) -> str:
        """
        Expand numbers to words for better pronunciation.
        Note: For complex number handling, use SSML <say-as>.
        """
        # Currency
        text = re.sub(
            r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',
            lambda m: f"{m.group(1).replace(',', '')} dollars",
            text
        )

        # Percentages
        text = re.sub(
            r'(\d+(?:\.\d+)?)\s*%',
            lambda m: f"{m.group(1)} percent",
            text
        )

        # Times (12:30)
        text = re.sub(
            r'(\d{1,2}):(\d{2})\s*(am|pm|AM|PM)?',
            lambda m: self._time_to_words(m.group(1), m.group(2), m.group(3)),
            text
        )

        # Large numbers with commas
        text = re.sub(
            r'(\d{1,3}(?:,\d{3})+)',
            lambda m: m.group(1).replace(',', ''),
            text
        )

        return text

    def _time_to_words(self, hour: str, minute: str, period: str = None) -> str:
        """Convert time to spoken form."""
        h = int(hour)
        m = int(minute)

        if m == 0:
            result = f"{h} o'clock"
        elif m == 30:
            result = f"{h} thirty"
        else:
            result = f"{h} {m}"

        if period:
            result += f" {period.upper()}"

        return result

    def _normalize_punctuation(self, text: str) -> str:
        """Normalize punctuation for TTS."""
        # Multiple spaces to single
        text = re.sub(r'\s+', ' ', text)

        # Multiple periods to single
        text = re.sub(r'\.{2,}', '.', text)

        # Em dashes to commas (for pause)
        text = text.replace('—', ', ')
        text = text.replace('–', ', ')

        # Remove brackets (TTS often reads them literally)
        text = re.sub(r'\[([^\]]+)\]', r'\1', text)
        text = re.sub(r'\(([^\)]+)\)', r', \1, ', text)

        return text

    def _split_at_sentences(self, text: str, max_length: int) -> List[str]:
        """Split text at sentence boundaries."""
        chunks = []
        current = ""

        sentences = re.split(r'(?<=[.!?])\s+', text)

        for sentence in sentences:
            if len(current) + len(sentence) <= max_length:
                current += sentence + " "
            else:
                if current:
                    chunks.append(current.strip())
                current = sentence + " "

        if current:
            chunks.append(current.strip())

        return chunks

# Usage
if __name__ == "__main__":
    preprocessor = TextPreprocessor()

    text = """
    Dr. Smith met Mr. Johnson at 3:30pm on Jan. 15th.
    The project costs $1,500,000 and is 75% complete...
    [Note: This is confidential] They discussed the plan.
    """

    processed = preprocessor.process(text)
    print(processed)

    chunks = preprocessor.chunk(text * 10)  # Long text
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}: {len(chunk)} chars")
```
