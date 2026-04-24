# Text-to-Speech Code Examples

## OpenAI TTS

### Basic Generation

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI()

def text_to_speech(
    text: str,
    output_path: str,
    voice: str = "alloy",
    model: str = "tts-1",
    speed: float = 1.0,
    response_format: str = "mp3"
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
        speed=speed,
        response_format=response_format
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

### Streaming Playback

```python
from openai import OpenAI
import pyaudio

client = OpenAI()

def stream_tts(text: str, voice: str = "alloy"):
    """Stream audio directly to speakers."""
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=24000,  # OpenAI TTS sample rate
        output=True
    )

    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="pcm"
    ) as response:
        for chunk in response.iter_bytes(chunk_size=1024):
            stream.write(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()

# Usage
stream_tts("This streams directly to your speakers.")
```

### Async Streaming

```python
import asyncio
from openai import AsyncOpenAI
from typing import AsyncGenerator

async_client = AsyncOpenAI()

async def stream_tts_async(
    text: str,
    voice: str = "alloy"
) -> AsyncGenerator[bytes, None]:
    """Async generator for TTS streaming."""
    async with async_client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="pcm"
    ) as response:
        async for chunk in response.iter_bytes():
            yield chunk

# Usage with FastAPI
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/tts")
async def tts_endpoint(text: str, voice: str = "alloy"):
    return StreamingResponse(
        stream_tts_async(text, voice),
        media_type="audio/pcm"
    )
```

### Steerability (Tone Control)

```python
from openai import OpenAI

client = OpenAI()

def steerable_tts(text: str, tone_instruction: str, output_path: str):
    """
    Use OpenAI's steerability feature to control tone.
    Add instructions in the text itself or system context.
    """
    # Prepend tone instruction to text
    steered_text = f"[{tone_instruction}] {text}"

    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="nova",
        input=steered_text
    )

    response.stream_to_file(output_path)
    return output_path

# Usage
steerable_tts(
    "I'm so excited to share this news with you!",
    "Speak with enthusiasm and excitement",
    "excited.mp3"
)

steerable_tts(
    "I regret to inform you that the event has been cancelled.",
    "Speak in a calm, sympathetic tone",
    "sympathetic.mp3"
)
```

## ElevenLabs

### Basic Generation

```python
from elevenlabs import ElevenLabs
from elevenlabs.client import VoiceSettings

client = ElevenLabs()

def elevenlabs_tts(
    text: str,
    output_path: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Rachel
    model: str = "eleven_multilingual_v2",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    style: float = 0.5
) -> str:
    """Generate speech using ElevenLabs."""
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model,
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
elevenlabs_tts(
    "Hello, this is ElevenLabs text to speech.",
    "elevenlabs_output.mp3"
)
```

### Low-Latency Streaming (Flash v2.5)

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

def elevenlabs_stream(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM"
):
    """Stream with ultra-low latency using Flash v2.5."""
    audio_stream = client.text_to_speech.convert_as_stream(
        text=text,
        voice_id=voice_id,
        model_id="eleven_flash_v2_5",  # 75ms latency
        output_format="pcm_24000"
    )

    for chunk in audio_stream:
        yield chunk

# Usage with speaker output
import pyaudio

def play_elevenlabs_stream(text: str):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=24000,
        output=True
    )

    for chunk in elevenlabs_stream(text):
        stream.write(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()
```

### Voice Cloning

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

def clone_voice(
    audio_files: list[str],
    name: str,
    description: str = ""
) -> str:
    """
    Clone a voice from audio samples.

    For best results:
    - Use 1-3 minutes of clean audio
    - Consistent recording environment
    - Clear speech without background noise
    """
    voice = client.voices.add(
        name=name,
        description=description,
        files=audio_files,
        labels={"accent": "american", "gender": "neutral"}
    )

    return voice.voice_id

def professional_voice_clone(
    audio_files: list[str],
    name: str
) -> str:
    """
    Create professional voice clone (requires consent verification).
    Provides higher fidelity than instant cloning.
    """
    voice = client.voices.add(
        name=name,
        files=audio_files,
        remove_background_noise=True,
        model_id="eleven_multilingual_v2"
    )

    return voice.voice_id

# Usage
voice_id = clone_voice(
    ["sample1.mp3", "sample2.mp3"],
    "Custom Voice",
    "Professional narrator voice"
)

# Use cloned voice
elevenlabs_tts(
    "This is my cloned voice speaking.",
    "cloned_output.mp3",
    voice_id=voice_id
)
```

### List Available Voices

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

def list_voices():
    """List all available voices."""
    response = client.voices.get_all()

    for voice in response.voices:
        print(f"ID: {voice.voice_id}")
        print(f"Name: {voice.name}")
        print(f"Category: {voice.category}")
        print(f"Labels: {voice.labels}")
        print("---")

    return response.voices

# Get specific voice
def get_voice(voice_id: str):
    return client.voices.get(voice_id)
```

## Google Cloud TTS

### Basic Generation

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

# Usage
google_tts(
    "Hello from Google Cloud Text to Speech.",
    "google_output.mp3",
    voice_name="en-US-Neural2-F"  # Female voice
)
```

### SSML Generation

```python
from google.cloud import texttospeech

def google_tts_ssml(ssml: str, output_path: str) -> str:
    """Generate speech from SSML markup."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-D"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(output_path, "wb") as f:
        f.write(response.audio_content)

    return output_path

# Usage with SSML
ssml = """
<speak>
    Welcome to our service.
    <break time="500ms"/>
    <prosody rate="slow" pitch="high">
        This is important information!
    </prosody>
    <break time="300ms"/>
    Your order number is <say-as interpret-as="cardinal">12345</say-as>.
</speak>
"""

google_tts_ssml(ssml, "ssml_output.mp3")
```

## SSML Builder

```python
class SSMLBuilder:
    """Build SSML markup for speech synthesis."""

    def __init__(self):
        self.content = []

    def say(self, text: str):
        """Add plain text."""
        self.content.append(text)
        return self

    def pause(self, duration_ms: int):
        """Add a pause."""
        self.content.append(f'<break time="{duration_ms}ms"/>')
        return self

    def emphasis(self, text: str, level: str = "moderate"):
        """Add emphasis (strong, moderate, reduced)."""
        self.content.append(f'<emphasis level="{level}">{text}</emphasis>')
        return self

    def say_as(self, text: str, interpret_as: str):
        """
        Interpret text as specific type.
        interpret_as: date, cardinal, ordinal, characters, time, telephone
        """
        self.content.append(f'<say-as interpret-as="{interpret_as}">{text}</say-as>')
        return self

    def prosody(
        self,
        text: str,
        rate: str = None,
        pitch: str = None,
        volume: str = None
    ):
        """
        Modify prosody.
        rate: x-slow, slow, medium, fast, x-fast, or percentage
        pitch: x-low, low, medium, high, x-high, or semitones
        volume: silent, x-soft, soft, medium, loud, x-loud
        """
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

    def sub(self, text: str, alias: str):
        """Substitute pronunciation."""
        self.content.append(f'<sub alias="{alias}">{text}</sub>')
        return self

    def phoneme(self, text: str, phonetic: str, alphabet: str = "ipa"):
        """Specify phonetic pronunciation."""
        self.content.append(
            f'<phoneme alphabet="{alphabet}" ph="{phonetic}">{text}</phoneme>'
        )
        return self

    def build(self) -> str:
        """Build final SSML."""
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
    .say(".")
    .build()
)
```

## Long Text Processing

```python
from typing import List
import re
from openai import OpenAI

class LongTextTTS:
    """Handle long text for TTS with chunking."""

    def __init__(
        self,
        max_chars: int = 4096,
        overlap_chars: int = 0
    ):
        self.max_chars = max_chars
        self.overlap_chars = overlap_chars
        self.client = OpenAI()

    def synthesize(
        self,
        text: str,
        output_path: str,
        voice: str = "alloy"
    ) -> str:
        """Synthesize long text with automatic chunking."""
        from pydub import AudioSegment
        import tempfile
        import os

        chunks = self._split_text(text)
        audio_segments = []

        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i + 1}/{len(chunks)}")

            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=chunk
            )

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                temp_path = f.name
                response.stream_to_file(temp_path)

            audio_segments.append((temp_path, AudioSegment.from_mp3(temp_path)))

        # Combine audio
        combined = audio_segments[0][1]
        for _, segment in audio_segments[1:]:
            combined += segment

        combined.export(output_path, format="mp3")

        # Cleanup
        for temp_path, _ in audio_segments:
            os.remove(temp_path)

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

# Usage
processor = LongTextTTS(max_chars=4096)
processor.synthesize(
    "Very long text here...",
    "long_output.mp3",
    voice="nova"
)
```

## Caching Layer

```python
import hashlib
from pathlib import Path
from typing import Optional
import shutil

class TTSCache:
    """Simple file-based TTS cache."""

    def __init__(self, cache_dir: str = "./tts_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get_cache_key(
        self,
        text: str,
        voice: str,
        provider: str,
        **params
    ) -> str:
        """Generate cache key from parameters."""
        content = f"{text}|{voice}|{provider}|{sorted(params.items())}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(
        self,
        text: str,
        voice: str,
        provider: str,
        **params
    ) -> Optional[str]:
        """Get cached audio path if exists."""
        key = self.get_cache_key(text, voice, provider, **params)
        cache_path = self.cache_dir / f"{key}.mp3"

        if cache_path.exists():
            return str(cache_path)
        return None

    def put(
        self,
        audio_path: str,
        text: str,
        voice: str,
        provider: str,
        **params
    ) -> str:
        """Cache audio file and return cache path."""
        key = self.get_cache_key(text, voice, provider, **params)
        cache_path = self.cache_dir / f"{key}.mp3"

        shutil.copy(audio_path, cache_path)
        return str(cache_path)

    def clear(self):
        """Clear all cached files."""
        for f in self.cache_dir.glob("*.mp3"):
            f.unlink()

# Usage
cache = TTSCache()

# Check cache first
cached = cache.get("Hello world", "nova", "openai")
if cached:
    print(f"Cache hit: {cached}")
else:
    # Generate audio
    output = text_to_speech("Hello world", "temp.mp3", voice="nova")
    # Cache it
    cache.put(output, "Hello world", "nova", "openai")
```

## Real-time Conversation TTS

```python
import asyncio
from openai import AsyncOpenAI
import pyaudio

async_client = AsyncOpenAI()

class ConversationalTTS:
    """Real-time TTS for conversational AI."""

    def __init__(self, voice: str = "nova"):
        self.voice = voice
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def _init_audio_stream(self):
        if self.stream is None:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True
            )

    async def speak(self, text: str):
        """Speak text with minimal latency."""
        self._init_audio_stream()

        async with async_client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice=self.voice,
            input=text,
            response_format="pcm"
        ) as response:
            async for chunk in response.iter_bytes(chunk_size=1024):
                self.stream.write(chunk)

    async def speak_sentence_by_sentence(self, text: str):
        """Process long text sentence by sentence for faster first audio."""
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)

        for sentence in sentences:
            if sentence.strip():
                await self.speak(sentence)

    def close(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()

# Usage
async def main():
    tts = ConversationalTTS(voice="nova")

    try:
        await tts.speak("Hello! How can I help you today?")
        await tts.speak_sentence_by_sentence(
            "That's a great question. Let me explain. "
            "There are several things to consider."
        )
    finally:
        tts.close()

asyncio.run(main())
```
