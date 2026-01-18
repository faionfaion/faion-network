# M-GEN-004: Audio Transcription

## Overview

Audio transcription (Speech-to-Text) converts audio and video content into text. Modern systems handle multiple languages, speaker identification, and noisy environments. Key providers include OpenAI Whisper, Deepgram, and AssemblyAI.

**When to use:** Transcribing meetings, podcasts, interviews, video content, or building voice-enabled applications.

## Core Concepts

### 1. STT Provider Comparison

| Provider | Accuracy | Speed | Languages | Features |
|----------|----------|-------|-----------|----------|
| **OpenAI Whisper** | High | Medium | 99 | Translation, timestamps |
| **Whisper (local)** | High | Slow | 99 | Free, private |
| **Deepgram** | Very High | Very Fast | 30+ | Real-time, diarization |
| **AssemblyAI** | High | Fast | Many | Summarization, topics |
| **Google STT** | High | Fast | 125+ | Enterprise, streaming |
| **Azure Speech** | High | Fast | 100+ | Custom models |

### 2. Key Features

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Word timestamps** | Time for each word | Video subtitles |
| **Speaker diarization** | Identify who spoke | Meeting notes |
| **Punctuation** | Add punctuation | Readable output |
| **Language detection** | Auto-detect language | Multilingual content |
| **Translation** | Transcribe + translate | Localization |
| **Custom vocabulary** | Domain terms | Technical content |

### 3. Audio Quality Factors

| Factor | Impact | Mitigation |
|--------|--------|------------|
| **Background noise** | Lower accuracy | Noise reduction |
| **Multiple speakers** | Confusion | Diarization |
| **Accents** | Recognition errors | Provider selection |
| **Audio codec** | Quality loss | High bitrate source |
| **Sample rate** | Detail level | 16kHz+ recommended |

## Best Practices

### 1. Preprocess Audio

```python
from pydub import AudioSegment
import subprocess

def preprocess_audio(input_path: str, output_path: str) -> str:
    """Optimize audio for transcription."""

    audio = AudioSegment.from_file(input_path)

    # Convert to mono
    audio = audio.set_channels(1)

    # Set sample rate to 16kHz (optimal for most STT)
    audio = audio.set_frame_rate(16000)

    # Normalize volume
    audio = normalize_audio(audio)

    # Export as WAV (best compatibility)
    audio.export(output_path, format="wav")

    return output_path

def normalize_audio(audio: AudioSegment, target_dBFS: float = -20.0) -> AudioSegment:
    """Normalize audio volume."""
    change_in_dBFS = target_dBFS - audio.dBFS
    return audio.apply_gain(change_in_dBFS)

def reduce_noise(input_path: str, output_path: str) -> str:
    """Apply noise reduction using ffmpeg."""
    subprocess.run([
        "ffmpeg", "-i", input_path,
        "-af", "afftdn=nf=-25",  # FFT-based noise reduction
        "-y", output_path
    ], check=True)
    return output_path
```

### 2. Handle Long Audio

```python
def transcribe_long_audio(
    audio_path: str,
    chunk_duration_ms: int = 600000  # 10 minutes
) -> dict:
    """Transcribe long audio in chunks."""

    from pydub import AudioSegment

    audio = AudioSegment.from_file(audio_path)
    total_duration = len(audio)
    chunks = []
    transcripts = []

    # Split into chunks
    for start in range(0, total_duration, chunk_duration_ms):
        end = min(start + chunk_duration_ms, total_duration)
        chunk = audio[start:end]

        # Add overlap for context
        if start > 0:
            overlap_start = max(0, start - 5000)  # 5s overlap
            chunk = audio[overlap_start:end]

        chunk_path = f"chunk_{start}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append({
            "path": chunk_path,
            "start_ms": start,
            "end_ms": end
        })

    # Transcribe each chunk
    for chunk in chunks:
        result = transcribe_with_whisper(chunk["path"])
        result["offset_ms"] = chunk["start_ms"]
        transcripts.append(result)

    # Merge transcripts
    return merge_transcripts(transcripts)
```

### 3. Add Speaker Diarization

```python
def transcribe_with_diarization(
    audio_path: str,
    num_speakers: int = None
) -> dict:
    """Transcribe with speaker identification."""

    import assemblyai as aai

    aai.settings.api_key = "your-api-key"

    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speakers_expected=num_speakers  # Optional hint
    )

    transcript = aai.Transcriber().transcribe(audio_path, config)

    # Format output with speakers
    formatted = []
    current_speaker = None

    for utterance in transcript.utterances:
        if utterance.speaker != current_speaker:
            current_speaker = utterance.speaker
            formatted.append(f"\n[Speaker {current_speaker}]")

        formatted.append(utterance.text)

    return {
        "text": " ".join(formatted),
        "utterances": [
            {
                "speaker": u.speaker,
                "text": u.text,
                "start": u.start,
                "end": u.end
            }
            for u in transcript.utterances
        ]
    }
```

## Common Patterns

### Pattern 1: OpenAI Whisper API

```python
from openai import OpenAI

client = OpenAI()

def transcribe_with_whisper(
    audio_path: str,
    language: str = None,
    prompt: str = None
) -> dict:
    """Transcribe using OpenAI Whisper API."""

    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language,  # Optional: "en", "es", etc.
            prompt=prompt,  # Optional: context/vocabulary hint
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"]
        )

    return {
        "text": response.text,
        "language": response.language,
        "duration": response.duration,
        "segments": response.segments,
        "words": response.words
    }

def translate_with_whisper(audio_path: str) -> dict:
    """Transcribe and translate to English."""

    with open(audio_path, "rb") as audio_file:
        response = client.audio.translations.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json"
        )

    return {
        "text": response.text,
        "original_language": "detected",
        "translated_to": "en"
    }
```

### Pattern 2: Local Whisper

```python
import whisper

def transcribe_local(
    audio_path: str,
    model_size: str = "large-v3",
    device: str = "cuda"
) -> dict:
    """Transcribe using local Whisper model."""

    # Load model (downloads on first use)
    model = whisper.load_model(model_size, device=device)

    # Transcribe
    result = model.transcribe(
        audio_path,
        language=None,  # Auto-detect
        task="transcribe",
        word_timestamps=True,
        verbose=False
    )

    return {
        "text": result["text"],
        "language": result["language"],
        "segments": result["segments"]
    }

# Model sizes and tradeoffs
model_options = {
    "tiny": {"speed": "fastest", "accuracy": "low", "vram": "1GB"},
    "base": {"speed": "fast", "accuracy": "medium", "vram": "1GB"},
    "small": {"speed": "medium", "accuracy": "good", "vram": "2GB"},
    "medium": {"speed": "slow", "accuracy": "high", "vram": "5GB"},
    "large-v3": {"speed": "slowest", "accuracy": "best", "vram": "10GB"}
}
```

### Pattern 3: Deepgram Real-time

```python
from deepgram import Deepgram
import asyncio

async def transcribe_realtime(audio_stream):
    """Real-time transcription with Deepgram."""

    dg = Deepgram("your-api-key")

    async def on_transcript(data):
        transcript = data.get("channel", {}).get("alternatives", [{}])[0]
        if transcript.get("transcript"):
            print(f"[{transcript.get('is_final', False)}] {transcript['transcript']}")

    # Create WebSocket connection
    socket = await dg.transcription.live({
        "punctuate": True,
        "interim_results": True,
        "language": "en",
        "model": "nova-2",
        "smart_format": True
    })

    socket.register_handler(socket.event.TRANSCRIPT_RECEIVED, on_transcript)

    # Send audio chunks
    async for chunk in audio_stream:
        socket.send(chunk)

    await socket.finish()
```

### Pattern 4: Subtitle Generation

```python
def generate_subtitles(
    audio_path: str,
    format: str = "srt",
    max_chars_per_line: int = 42
) -> str:
    """Generate subtitles from audio."""

    # Transcribe with word timestamps
    result = transcribe_with_whisper(audio_path)

    if format == "srt":
        return generate_srt(result["segments"], max_chars_per_line)
    elif format == "vtt":
        return generate_vtt(result["segments"], max_chars_per_line)
    else:
        raise ValueError(f"Unknown format: {format}")

def generate_srt(segments: list, max_chars: int) -> str:
    """Generate SRT subtitle file."""

    srt_lines = []

    for i, segment in enumerate(segments, 1):
        start = format_timestamp_srt(segment["start"])
        end = format_timestamp_srt(segment["end"])
        text = wrap_text(segment["text"].strip(), max_chars)

        srt_lines.append(f"{i}")
        srt_lines.append(f"{start} --> {end}")
        srt_lines.append(text)
        srt_lines.append("")

    return "\n".join(srt_lines)

def format_timestamp_srt(seconds: float) -> str:
    """Format seconds to SRT timestamp."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
```

### Pattern 5: Meeting Transcription

```python
class MeetingTranscriber:
    """Full meeting transcription pipeline."""

    def __init__(self, assemblyai_key: str):
        import assemblyai as aai
        aai.settings.api_key = assemblyai_key
        self.transcriber = aai.Transcriber()

    def transcribe_meeting(
        self,
        audio_path: str,
        generate_summary: bool = True
    ) -> dict:
        """Transcribe meeting with all features."""

        config = aai.TranscriptionConfig(
            speaker_labels=True,
            auto_chapters=True,
            entity_detection=True,
            sentiment_analysis=True,
            summarization=generate_summary,
            summary_model=aai.SummarizationModel.informative,
            summary_type=aai.SummarizationType.bullets
        )

        transcript = self.transcriber.transcribe(audio_path, config)

        return {
            "text": transcript.text,
            "utterances": [
                {
                    "speaker": u.speaker,
                    "text": u.text,
                    "start": u.start,
                    "end": u.end,
                    "sentiment": u.sentiment
                }
                for u in transcript.utterances
            ],
            "chapters": [
                {
                    "headline": c.headline,
                    "summary": c.summary,
                    "start": c.start,
                    "end": c.end
                }
                for c in transcript.chapters
            ],
            "summary": transcript.summary,
            "entities": transcript.entities,
            "duration": transcript.audio_duration
        }

    def generate_meeting_notes(self, transcription: dict) -> str:
        """Generate formatted meeting notes."""

        notes = ["# Meeting Notes\n"]

        # Summary
        if transcription.get("summary"):
            notes.append("## Summary")
            notes.append(transcription["summary"])
            notes.append("")

        # Key Topics (chapters)
        if transcription.get("chapters"):
            notes.append("## Key Topics")
            for chapter in transcription["chapters"]:
                notes.append(f"### {chapter['headline']}")
                notes.append(chapter["summary"])
                notes.append("")

        # Action Items (extract from text)
        action_items = self._extract_action_items(transcription["text"])
        if action_items:
            notes.append("## Action Items")
            for item in action_items:
                notes.append(f"- [ ] {item}")
            notes.append("")

        return "\n".join(notes)
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Raw upload | Poor quality | Preprocess audio |
| Ignoring context | Misheard terms | Provide vocabulary prompt |
| Single chunk | Timeout, memory | Chunk long audio |
| No speaker labels | Confused attribution | Use diarization |
| Missing timestamps | Hard to navigate | Request word timestamps |

## Tools & References

### Related Skills
- faion-audio-skill
- faion-openai-api-skill

### Related Agents
- faion-stt-agent

### External Resources
- [OpenAI Whisper](https://platform.openai.com/docs/guides/speech-to-text)
- [Deepgram](https://deepgram.com/)
- [AssemblyAI](https://www.assemblyai.com/)
- [Whisper GitHub](https://github.com/openai/whisper)

## Checklist

- [ ] Preprocessed audio (mono, 16kHz)
- [ ] Selected appropriate provider
- [ ] Configured language/vocabulary
- [ ] Enabled word timestamps
- [ ] Added speaker diarization (if needed)
- [ ] Handled long audio chunking
- [ ] Post-processed transcript
- [ ] Generated subtitles/notes
- [ ] Validated accuracy
- [ ] Stored with metadata

---

*Methodology: M-GEN-004 | Category: Multimodal/Generation*
*Related: faion-stt-agent, faion-audio-skill*
