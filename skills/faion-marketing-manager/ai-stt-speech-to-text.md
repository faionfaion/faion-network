# AI Speech-to-Text (STT) & Voice Cloning

**High-accuracy transcription, real-time streaming, and voice cloning**

---

## STT Service Comparison

| Service | Latency | WER | Languages | Price/min | Best For |
|---------|---------|-----|-----------|-----------|----------|
| **OpenAI Whisper** | ~320ms | ~10% | 100+ | $0.006 | Batch, multilingual |
| **Deepgram Nova-3** | ~200ms | ~8% | 30+ | $0.0059 | Real-time, voice agents |
| **AssemblyAI** | ~300ms | ~5% | 20+ | $0.015 | Accuracy, features |
| **ElevenLabs Scribe** | ~250ms | ~3.5% | 32 | $0.10 | Highest accuracy |
| **Azure Speech** | ~200ms | ~8% | 100+ | $0.016 | Enterprise |
| **Google STT** | ~200ms | ~9% | 125+ | $0.016 | Multilingual |
| **AWS Transcribe** | ~300ms | ~10% | 100+ | $0.024 | AWS integration |

---

## OpenAI Whisper (STT)

### Overview

Whisper provides excellent multilingual speech recognition with 100+ language support.

**Limits:**
- Max file size: 25 MB
- Supported formats: mp3, mp4, mpeg, mpga, m4a, wav, webm

### Basic Transcription

```python
from openai import OpenAI

client = OpenAI()

# Transcribe audio file
with open("audio.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text",  # text, json, srt, verbose_json, vtt
    )

print(transcript)
```

### Word-Level Timestamps

```python
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["word", "segment"],
)

for word in transcript.words:
    print(f"{word.start:.2f}s - {word.end:.2f}s: {word.word}")
```

### Translation to English

```python
# Translate any language to English
translation = client.audio.translations.create(
    model="whisper-1",
    file=audio_file,
    response_format="text",
)
```

### Language Detection

```python
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="verbose_json",
)

print(f"Detected language: {transcript.language}")
```

### Prompt for Better Accuracy

```python
# Use prompt to improve accuracy for specific terms
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    prompt="Faion Network, SDD, solopreneur, Claude Code",
)
```

---

## Deepgram (Real-time STT)

### Overview

Deepgram Nova-3 offers the best real-time speech recognition for voice agents.

**Key Features:**
- Ultra-low latency (~200ms)
- Real-time streaming
- Speaker diarization
- Intent detection
- Summarization

### Installation

```bash
pip install deepgram-sdk
```

### Batch Transcription

```python
from deepgram import DeepgramClient, PrerecordedOptions

deepgram = DeepgramClient("your_api_key")

# Transcribe file
with open("audio.mp3", "rb") as file:
    buffer_data = file.read()

options = PrerecordedOptions(
    model="nova-3",
    language="en",
    smart_format=True,
    punctuate=True,
    paragraphs=True,
    diarize=True,       # Speaker identification
    utterances=True,    # Separate by speaker
    detect_language=True,
)

response = deepgram.listen.prerecorded.v("1").transcribe_file(
    {"buffer": buffer_data},
    options
)

print(response.results.channels[0].alternatives[0].transcript)
```

### Real-time Streaming

```python
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
import asyncio

deepgram = DeepgramClient("your_api_key")

async def main():
    connection = deepgram.listen.live.v("1")

    # Event handlers
    @connection.on(LiveTranscriptionEvents.Transcript)
    def on_transcript(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            print(f"Transcript: {transcript}")

    @connection.on(LiveTranscriptionEvents.SpeechStarted)
    def on_speech_started(self, speech_started, **kwargs):
        print("Speech started")

    @connection.on(LiveTranscriptionEvents.UtteranceEnd)
    def on_utterance_end(self, utterance_end, **kwargs):
        print("Utterance ended")

    # Configure options
    options = LiveOptions(
        model="nova-3",
        language="en",
        smart_format=True,
        interim_results=True,    # Get partial results
        endpointing=300,         # Silence detection (ms)
        vad_events=True,         # Voice activity detection
    )

    # Start connection
    await connection.start(options)

    # Send audio data (from microphone, WebSocket, etc.)
    # connection.send(audio_bytes)

    # Keep connection alive
    await asyncio.sleep(60)

    await connection.finish()

asyncio.run(main())
```

### Speaker Diarization

```python
options = PrerecordedOptions(
    model="nova-3",
    diarize=True,
    utterances=True,
)

response = deepgram.listen.prerecorded.v("1").transcribe_file(
    {"buffer": audio_data},
    options
)

# Process utterances by speaker
for utterance in response.results.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.transcript}")
```

### Keyword Boosting

```python
options = PrerecordedOptions(
    model="nova-3",
    keywords=["Faion:2.0", "SDD:1.5", "solopreneur:1.5"],
)
```

---

## AssemblyAI (High Accuracy STT)

### Overview

AssemblyAI offers the highest accuracy with advanced features like sentiment analysis and topic detection.

### Installation

```bash
pip install assemblyai
```

### Basic Transcription

```python
import assemblyai as aai

aai.settings.api_key = "your_api_key"

transcriber = aai.Transcriber()

# Transcribe from URL or file
transcript = transcriber.transcribe("https://example.com/audio.mp3")
# Or: transcript = transcriber.transcribe("./audio.mp3")

print(transcript.text)
```

### Advanced Features

```python
config = aai.TranscriptionConfig(
    language_code="en",
    speech_model=aai.SpeechModel.best,

    # Speaker diarization
    speaker_labels=True,
    speakers_expected=2,

    # Content moderation
    content_safety=True,

    # Sentiment analysis
    sentiment_analysis=True,

    # Topic detection
    iab_categories=True,

    # Auto chapters
    auto_chapters=True,

    # Summarization
    summarization=True,
    summary_type=aai.SummarizationType.bullets,

    # Entity detection
    entity_detection=True,

    # Custom vocabulary
    word_boost=["Faion", "SDD", "solopreneur"],
    boost_param="high",
)

transcript = transcriber.transcribe("audio.mp3", config=config)

# Access results
print(f"Speakers: {len(transcript.utterances)}")
for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.text}")

print(f"Summary: {transcript.summary}")
print(f"Chapters: {transcript.chapters}")
print(f"Sentiment: {transcript.sentiment_analysis_results}")
```

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

## API Credentials

### Environment Variables

```bash
# OpenAI
export OPENAI_API_KEY="your_key"

# Deepgram
export DEEPGRAM_API_KEY="your_key"

# AssemblyAI
export ASSEMBLYAI_API_KEY="your_key"

# ElevenLabs
export ELEVENLABS_API_KEY="your_key"
```

### Loading Credentials

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Or use secrets file
# source ~/.secrets/openai
# source ~/.secrets/deepgram
# source ~/.secrets/assemblyai
# source ~/.secrets/elevenlabs
```

---

## References

- [OpenAI Audio API](https://platform.openai.com/docs/guides/audio)
- [Deepgram Docs](https://developers.deepgram.com/docs)
- [AssemblyAI Docs](https://www.assemblyai.com/docs)
- [ElevenLabs Docs](https://elevenlabs.io/docs)
- [Coqui TTS](https://github.com/coqui-ai/TTS)
