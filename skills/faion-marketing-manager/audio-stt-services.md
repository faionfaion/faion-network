# Speech-to-Text (STT) Services

**Comprehensive guide for speech-to-text transcription using Whisper, Deepgram, and AssemblyAI**

---

## Quick Reference

**When to use this guide:**
- Speech-to-text transcription (STT)
- Audio transcription with speaker diarization
- Real-time voice recognition
- Podcast/content production transcription
- Multilingual transcription

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

### Real-time Streaming

```python
def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        print(f"Final: {transcript.text}")
    else:
        print(f"Partial: {transcript.text}", end="\r")

def on_error(error: aai.RealtimeError):
    print(f"Error: {error}")

transcriber = aai.RealtimeTranscriber(
    sample_rate=16000,
    on_data=on_data,
    on_error=on_error,
)

transcriber.connect()

# Send audio chunks
# transcriber.stream(audio_bytes)

transcriber.close()
```

---

## Speaker Diarization

### pyannote-audio (Open Source)

```bash
pip install pyannote.audio
```

```python
from pyannote.audio import Pipeline

# Initialize pipeline (requires HuggingFace token)
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="your_hf_token"
)

# Run diarization
diarization = pipeline("audio.wav")

# Print results
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"{turn.start:.1f}s - {turn.end:.1f}s: {speaker}")
```

### Combining with Whisper

```python
from pyannote.audio import Pipeline
import whisper

# Diarization
diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1"
)
diarization = diarization_pipeline("audio.wav")

# Transcription
whisper_model = whisper.load_model("large-v3")
result = whisper_model.transcribe("audio.wav")

# Combine: assign speakers to transcript segments
def assign_speakers(transcript, diarization):
    """Assign speakers to transcript segments based on timing"""
    for segment in transcript["segments"]:
        start = segment["start"]
        end = segment["end"]

        # Find speaker for this segment
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            if turn.start <= start and turn.end >= end:
                segment["speaker"] = speaker
                break

    return transcript

result = assign_speakers(result, diarization)
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
```

### Loading Credentials

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Or use secrets file
# source ~/.secrets/openai
# source ~/.secrets/deepgram
```

---

## Related Files

- [audio-tts-services.md](audio-tts-services.md) - Text-to-speech services
- [audio-voice-agents.md](audio-voice-agents.md) - Voice cloning, real-time streaming, voice agents

---

## References

- [OpenAI Audio API](https://platform.openai.com/docs/guides/audio)
- [Deepgram Docs](https://developers.deepgram.com/docs)
- [AssemblyAI Docs](https://www.assemblyai.com/docs)
- [pyannote-audio](https://github.com/pyannote/pyannote-audio)
