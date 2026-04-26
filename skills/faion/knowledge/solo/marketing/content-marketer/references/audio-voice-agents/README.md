# Voice Agents & Real-time Streaming

**Comprehensive guide for voice cloning, real-time voice agents, and audio processing**

---

## Quick Reference

**When to use this guide:**
- Voice cloning and voice design
- Real-time voice agents
- WebSocket voice streaming
- Audio editing and manipulation
- Latency optimization for voice applications
- Cost optimization for audio services

---

## Voice Cloning

### ElevenLabs Voice Cloning

**Types:**
| Type | Audio Required | Quality | Turnaround |
|------|----------------|---------|------------|
| Instant | 1-30 min | Good | Seconds |
| Professional | 30+ min | Excellent | Hours |

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

# Instant voice clone
voice = client.clone(
    name="My Voice Clone",
    description="Cloned from podcast recordings",
    files=[
        "sample1.mp3",
        "sample2.mp3",
        "sample3.mp3",
    ],
    labels={
        "accent": "american",
        "gender": "male",
        "age": "adult",
    }
)

print(f"Voice ID: {voice.voice_id}")
```

### Coqui TTS (Open Source)

```bash
pip install TTS
```

```python
from TTS.api import TTS

# List available models
print(TTS().list_models())

# Load model
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

# Voice cloning with reference audio
tts.tts_to_file(
    text="Hello, this is my cloned voice!",
    speaker_wav="reference_voice.wav",
    language="en",
    file_path="output.wav",
)
```

### Tortoise TTS (High Quality Open Source)

```python
import torch
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice

tts = TextToSpeech()

# Load custom voice samples
voice_samples, conditioning_latents = load_voice(
    "my_voice",
    extra_voice_dirs=["./voices"]
)

# Generate with voice clone
gen = tts.tts_with_preset(
    "Hello from my cloned voice!",
    voice_samples=voice_samples,
    conditioning_latents=conditioning_latents,
    preset="fast",  # ultra_fast, fast, standard, high_quality
)
```

---

## Real-time Streaming Patterns

### Voice Agent Architecture

```
User Speech → STT (Deepgram) → LLM (Claude/GPT) → TTS (ElevenLabs) → Audio Output
                  ↓                    ↓                   ↓
              ~200ms              ~500ms              ~100ms

Target: < 1000ms total latency
```

### WebSocket Voice Agent

```python
import asyncio
import websockets
from deepgram import DeepgramClient, LiveOptions
from elevenlabs import ElevenLabs
from openai import OpenAI

class VoiceAgent:
    def __init__(self):
        self.deepgram = DeepgramClient()
        self.elevenlabs = ElevenLabs()
        self.openai = OpenAI()
        self.conversation_history = []

    async def handle_audio(self, websocket, path):
        """Handle incoming audio from WebSocket"""

        # Setup Deepgram connection
        dg_connection = self.deepgram.listen.live.v("1")

        async def on_transcript(result):
            transcript = result.channel.alternatives[0].transcript
            if transcript and result.is_final:
                # Process with LLM
                response = await self.process_with_llm(transcript)

                # Generate speech
                audio = self.generate_speech(response)

                # Send back to client
                await websocket.send(audio)

        dg_connection.on("transcript", on_transcript)

        await dg_connection.start(LiveOptions(
            model="nova-3",
            language="en",
            smart_format=True,
            interim_results=False,
            endpointing=300,
        ))

        # Forward audio chunks to Deepgram
        async for message in websocket:
            dg_connection.send(message)

        await dg_connection.finish()

    async def process_with_llm(self, user_input: str) -> str:
        """Process user input with LLM"""
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        response = self.openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant. Keep responses concise (under 100 words)."},
                *self.conversation_history
            ],
            max_tokens=150,
        )

        assistant_message = response.choices[0].message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def generate_speech(self, text: str) -> bytes:
        """Generate speech from text"""
        audio_stream = self.elevenlabs.text_to_speech.convert_as_stream(
            voice_id="21m00Tcm4TlvDq8ikWAM",
            text=text,
            model_id="eleven_flash_v2_5",
            output_format="mp3_44100_32",
        )

        return b"".join(audio_stream)

# Run server
async def main():
    agent = VoiceAgent()
    async with websockets.serve(agent.handle_audio, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
```

### Turn-Taking Detection

```python
class TurnTakingDetector:
    def __init__(
        self,
        silence_threshold: float = 0.3,  # seconds
        energy_threshold: float = 0.01,
    ):
        self.silence_threshold = silence_threshold
        self.energy_threshold = energy_threshold
        self.last_speech_time = 0
        self.is_user_speaking = False

    def process_audio(self, audio_chunk: bytes, timestamp: float) -> str:
        """Detect turn-taking events"""
        energy = self.calculate_energy(audio_chunk)

        if energy > self.energy_threshold:
            self.is_user_speaking = True
            self.last_speech_time = timestamp
            return "speech_continued"

        elif self.is_user_speaking:
            silence_duration = timestamp - self.last_speech_time

            if silence_duration > self.silence_threshold:
                self.is_user_speaking = False
                return "turn_ended"

            return "silence"

        return "no_speech"

    def calculate_energy(self, audio_chunk: bytes) -> float:
        """Calculate RMS energy of audio chunk"""
        import numpy as np
        samples = np.frombuffer(audio_chunk, dtype=np.int16)
        return np.sqrt(np.mean(samples.astype(float) ** 2)) / 32768
```

### Interruption Handling

```python
class InterruptionHandler:
    def __init__(self, agent_audio_queue: asyncio.Queue):
        self.is_agent_speaking = False
        self.audio_queue = agent_audio_queue

    async def handle_user_speech(self, is_speaking: bool):
        """Handle user interruption during agent speech"""
        if is_speaking and self.is_agent_speaking:
            # User started speaking while agent is speaking
            await self.interrupt_agent()

    async def interrupt_agent(self):
        """Stop agent audio playback"""
        self.is_agent_speaking = False

        # Clear audio queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except asyncio.QueueEmpty:
                break

        print("Agent interrupted by user")

    async def play_agent_response(self, audio_chunks):
        """Play agent response with interruption support"""
        self.is_agent_speaking = True

        for chunk in audio_chunks:
            if not self.is_agent_speaking:
                break  # Interrupted

            await self.audio_queue.put(chunk)
            await asyncio.sleep(0.01)

        self.is_agent_speaking = False
```

---

## Audio Editing

### pydub (Audio Manipulation)

```bash
pip install pydub
```

```python
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
from pydub.silence import split_on_silence

# Load audio
audio = AudioSegment.from_file("input.mp3")

# Basic operations
audio = audio + 10  # Increase volume by 10dB
audio = audio - 5   # Decrease volume by 5dB
audio = audio.fade_in(1000).fade_out(1000)  # Fade in/out
audio = audio.set_frame_rate(44100)  # Resample
audio = audio.set_channels(1)  # Convert to mono

# Concatenation
combined = audio1 + audio2

# Slicing
first_10_seconds = audio[:10000]  # milliseconds

# Split on silence
chunks = split_on_silence(
    audio,
    min_silence_len=500,
    silence_thresh=-40,
    keep_silence=200,
)

# Effects
audio = normalize(audio)
audio = compress_dynamic_range(audio, threshold=-20, ratio=4.0)

# Export
audio.export("output.mp3", format="mp3", bitrate="192k")
audio.export("output.wav", format="wav")
```

### librosa (Audio Analysis)

```bash
pip install librosa
```

```python
import librosa
import numpy as np

# Load audio
y, sr = librosa.load("audio.mp3", sr=None)

# Get duration
duration = librosa.get_duration(y=y, sr=sr)

# Extract features
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# Pitch detection
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

# Speech/music detection
# (Use onset detection for speech segmentation)
onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)
```

### soundfile (Read/Write Audio)

```python
import soundfile as sf

# Read audio
data, samplerate = sf.read("audio.wav")

# Write audio
sf.write("output.wav", data, samplerate)

# Get info without loading
info = sf.info("audio.wav")
print(f"Duration: {info.duration}s, Channels: {info.channels}")
```

---

## Latency Optimization

### Best Practices for Low Latency

| Optimization | Impact | Implementation |
|--------------|--------|----------------|
| **Streaming TTS** | -200ms | Use `eleven_flash_v2_5` with streaming |
| **Streaming STT** | -150ms | Use Deepgram Nova-3 live |
| **Sentence chunking** | -300ms | Generate TTS per sentence |
| **Prefetch** | -100ms | Start TTS before LLM completes |
| **WebSocket** | -50ms | Use persistent connections |
| **Edge deployment** | -100ms | Deploy STT/TTS at edge |

### Sentence-Level Streaming

```python
import re

def stream_by_sentence(text: str, tts_client):
    """Stream TTS generation by sentence for lower latency"""

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:
        if sentence.strip():
            audio_stream = tts_client.text_to_speech.convert_as_stream(
                voice_id="21m00Tcm4TlvDq8ikWAM",
                text=sentence,
                model_id="eleven_flash_v2_5",
            )

            for chunk in audio_stream:
                yield chunk
```

### Prefetch Pattern

```python
async def prefetch_tts(llm_stream, tts_client):
    """Start TTS generation as soon as first sentence is available"""

    buffer = ""

    async for token in llm_stream:
        buffer += token

        # Check for sentence boundary
        if any(buffer.endswith(p) for p in ['. ', '! ', '? ']):
            # Start TTS immediately
            audio_task = asyncio.create_task(
                generate_tts_async(buffer.strip(), tts_client)
            )
            yield audio_task
            buffer = ""

    # Handle remaining text
    if buffer.strip():
        audio_task = asyncio.create_task(
            generate_tts_async(buffer.strip(), tts_client)
        )
        yield audio_task
```

---

## Error Recovery

### Robust Voice Agent

```python
class RobustVoiceAgent:
    def __init__(self):
        self.fallback_responses = [
            "I'm sorry, I didn't catch that. Could you repeat?",
            "Let me think about that for a moment.",
            "I'm having trouble understanding. Can you try again?",
        ]
        self.retry_count = 0
        self.max_retries = 3

    async def process_with_fallback(self, audio_chunk: bytes) -> bytes:
        try:
            # Primary STT
            transcript = await self.stt_primary(audio_chunk)

            if not transcript or len(transcript) < 2:
                return self.get_fallback_audio("no_speech")

            # LLM processing
            response = await self.llm_process(transcript)

            # TTS
            audio = await self.tts_generate(response)

            self.retry_count = 0
            return audio

        except Exception as e:
            self.retry_count += 1

            if self.retry_count >= self.max_retries:
                return self.get_fallback_audio("error")

            # Try fallback STT service
            try:
                transcript = await self.stt_fallback(audio_chunk)
                response = await self.llm_process(transcript)
                return await self.tts_generate(response)
            except:
                return self.get_fallback_audio("retry")

    def get_fallback_audio(self, reason: str) -> bytes:
        """Return pre-generated fallback audio"""
        import random
        response = random.choice(self.fallback_responses)
        # Use cached or pre-generated audio for faster response
        return self.cached_audio.get(response)
```

---

## Cost Optimization

### Service Selection by Use Case

| Use Case | Recommended | Monthly Cost (10h audio) |
|----------|-------------|--------------------------|
| **Podcast transcription** | Whisper | $3.60 |
| **Voice agent (quality)** | Deepgram + ElevenLabs | $35 + $180 |
| **Voice agent (budget)** | Deepgram + OpenAI TTS | $35 + $9 |
| **Batch TTS** | OpenAI TTS | $9/100k chars |
| **Premium TTS** | ElevenLabs | $22/month (10k chars) |

### Caching Strategy

```python
import hashlib
from functools import lru_cache

class TTSCache:
    def __init__(self, cache_dir: str = "./tts_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_cache_key(self, text: str, voice_id: str, model: str) -> str:
        """Generate cache key from parameters"""
        content = f"{text}:{voice_id}:{model}"
        return hashlib.md5(content.encode()).hexdigest()

    def get_cached(self, text: str, voice_id: str, model: str) -> bytes | None:
        """Get cached audio if exists"""
        key = self.get_cache_key(text, voice_id, model)
        path = os.path.join(self.cache_dir, f"{key}.mp3")

        if os.path.exists(path):
            with open(path, "rb") as f:
                return f.read()
        return None

    def cache_audio(self, text: str, voice_id: str, model: str, audio: bytes):
        """Cache generated audio"""
        key = self.get_cache_key(text, voice_id, model)
        path = os.path.join(self.cache_dir, f"{key}.mp3")

        with open(path, "wb") as f:
            f.write(audio)
```

---

## Related Agents

| Agent | Purpose |
|-------|---------|
| faion-tts-agent | Text-to-speech synthesis |
| faion-stt-agent | Speech-to-text transcription |
| faion-voice-agent-builder-agent | Build complete voice agents |

---

## Related Files

- [audio-tts-services.md](audio-tts-services.md) - Text-to-speech services
- [audio-stt-services.md](audio-stt-services.md) - Speech-to-text services

---

## References

- [ElevenLabs Docs](https://elevenlabs.io/docs)
- [Deepgram Docs](https://developers.deepgram.com/docs)
- [Coqui TTS](https://github.com/coqui-ai/TTS)


## Sources

- [Bland AI Voice Agents](https://www.bland.ai/blog)
- [Vapi AI Voice Platform](https://vapi.ai/blog)
- [Retell AI Conversational](https://www.retellai.com/blog)
- [Air AI Phone Agents](https://www.air.ai/)
- [ElevenLabs Conversational AI](https://elevenlabs.io/blog)
