# Speech-to-Text Code Examples

## OpenAI Whisper API

### Basic Transcription

```python
from openai import OpenAI

client = OpenAI()

def transcribe_audio(
    audio_path: str,
    language: str = None,
    response_format: str = "text",
    prompt: str = None
) -> str:
    """
    Transcribe audio using Whisper API.

    response_format: "text", "json", "verbose_json", "srt", "vtt"
    """
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language,  # ISO-639-1 code (e.g., "en", "es", "uk")
            response_format=response_format,
            prompt=prompt  # Guide transcription with context
        )

    if response_format == "text":
        return response
    return response
```

### With Timestamps

```python
def transcribe_with_timestamps(audio_path: str) -> dict:
    """Get transcription with word-level timestamps."""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"]
        )

    return {
        "text": response.text,
        "segments": response.segments,
        "words": response.words,
        "duration": response.duration
    }
```

### Translation to English

```python
def translate_audio(audio_path: str) -> str:
    """Translate audio to English."""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.translations.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text
```

### GPT-4o Transcribe (2025+)

```python
def transcribe_gpt4o(
    audio_path: str,
    with_diarization: bool = False
) -> dict:
    """
    Transcribe using GPT-4o models.
    Better accuracy than Whisper, optional speaker diarization.
    """
    model = "gpt-4o-transcribe"

    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            response_format="verbose_json",
            # Enable diarization for speaker identification
            # speaker_labels=with_diarization  # Check current API docs
        )

    return {
        "text": response.text,
        "segments": response.segments,
        "duration": response.duration
    }
```

## Local Whisper

### Basic Local Transcription

```python
import whisper
import torch

class LocalWhisper:
    """Local Whisper transcription."""

    def __init__(
        self,
        model_size: str = "base",
        device: str = None
    ):
        """
        model_size: "tiny", "base", "small", "medium", "large", "large-v3"
        """
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.model = whisper.load_model(model_size, device=device)

    def transcribe(
        self,
        audio_path: str,
        language: str = None,
        task: str = "transcribe",  # or "translate"
        word_timestamps: bool = False
    ) -> dict:
        """Transcribe audio file."""
        result = self.model.transcribe(
            audio_path,
            language=language,
            task=task,
            word_timestamps=word_timestamps
        )

        return {
            "text": result["text"],
            "segments": result["segments"],
            "language": result["language"]
        }
```

## Faster Whisper (Optimized)

### Production-Grade Local

```python
from faster_whisper import WhisperModel
from typing import Generator, Dict

class FasterWhisperTranscriber:
    """Optimized Whisper using CTranslate2."""

    def __init__(
        self,
        model_size: str = "large-v3-turbo",
        device: str = "auto",
        compute_type: str = "auto"
    ):
        """
        model_size: "tiny", "base", "small", "medium", "large-v3", "large-v3-turbo"
        compute_type: "float16", "int8", "int8_float16", "auto"
        """
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

    def transcribe(
        self,
        audio_path: str,
        language: str = None,
        beam_size: int = 5,
        word_timestamps: bool = False,
        vad_filter: bool = True
    ) -> Dict:
        """Transcribe audio with optimized performance."""
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=beam_size,
            word_timestamps=word_timestamps,
            vad_filter=vad_filter
        )

        all_segments = []
        full_text = ""

        for segment in segments:
            all_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "words": [
                    {
                        "word": w.word,
                        "start": w.start,
                        "end": w.end,
                        "probability": w.probability
                    }
                    for w in (segment.words or [])
                ]
            })
            full_text += segment.text

        return {
            "text": full_text.strip(),
            "segments": all_segments,
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration
        }

    def transcribe_stream(
        self,
        audio_path: str,
        **kwargs
    ) -> Generator[Dict, None, None]:
        """Stream transcription segments."""
        segments, info = self.model.transcribe(audio_path, **kwargs)

        for segment in segments:
            yield {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            }
```

## Long Audio Processing

### Chunked Transcription

```python
from pydub import AudioSegment
from pathlib import Path
import tempfile
from typing import List, Dict
from openai import OpenAI

class LongAudioTranscriber:
    """Handle long audio files by chunking."""

    def __init__(
        self,
        chunk_duration_ms: int = 300000,  # 5 minutes
        overlap_ms: int = 5000  # 5 seconds
    ):
        self.chunk_duration = chunk_duration_ms
        self.overlap = overlap_ms
        self.client = OpenAI()

    def transcribe(self, audio_path: str) -> Dict:
        """Transcribe long audio file."""
        audio = AudioSegment.from_file(audio_path)
        duration_ms = len(audio)

        # Check if chunking needed (Whisper limit is 25MB)
        if duration_ms <= self.chunk_duration:
            return self._transcribe_chunk(audio_path)

        chunks = self._split_audio(audio)
        results = []

        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i + 1}/{len(chunks)}")

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                chunk["audio"].export(f.name, format="mp3")
                result = self._transcribe_chunk(f.name)

                results.append({
                    "start_ms": chunk["start"],
                    "end_ms": chunk["end"],
                    "text": result
                })

                Path(f.name).unlink()

        return self._merge_results(results)

    def _split_audio(self, audio: AudioSegment) -> List[Dict]:
        """Split audio into overlapping chunks."""
        chunks = []
        duration_ms = len(audio)
        start = 0

        while start < duration_ms:
            end = min(start + self.chunk_duration, duration_ms)
            chunk = audio[start:end]

            chunks.append({
                "audio": chunk,
                "start": start,
                "end": end
            })

            start = end - self.overlap

        return chunks

    def _transcribe_chunk(self, audio_path: str) -> str:
        """Transcribe single chunk."""
        with open(audio_path, "rb") as f:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return response

    def _merge_results(self, results: List[Dict]) -> Dict:
        """Merge chunk results."""
        full_text = results[0]["text"]

        for i in range(1, len(results)):
            full_text += " " + results[i]["text"]

        return {
            "text": full_text,
            "chunks": results
        }
```

## Speaker Diarization

### Using pyannote

```python
from pyannote.audio import Pipeline
from typing import Dict, List
import torch

class SpeakerDiarizer:
    """Add speaker labels to transcription."""

    def __init__(self, hf_token: str):
        """
        Requires HuggingFace token with pyannote access.
        """
        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        )

        if torch.cuda.is_available():
            self.pipeline.to(torch.device("cuda"))

    def diarize(self, audio_path: str) -> List[Dict]:
        """Get speaker segments."""
        diarization = self.pipeline(audio_path)

        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({
                "speaker": speaker,
                "start": turn.start,
                "end": turn.end
            })

        return segments

    def align_with_transcript(
        self,
        audio_path: str,
        transcript_segments: List[Dict]
    ) -> List[Dict]:
        """Align speaker labels with transcript."""
        speaker_segments = self.diarize(audio_path)

        for segment in transcript_segments:
            segment_mid = (segment["start"] + segment["end"]) / 2

            for speaker_seg in speaker_segments:
                if speaker_seg["start"] <= segment_mid <= speaker_seg["end"]:
                    segment["speaker"] = speaker_seg["speaker"]
                    break
            else:
                segment["speaker"] = "UNKNOWN"

        return transcript_segments
```

## Real-Time Streaming

### AssemblyAI WebSocket

```python
import asyncio
import websockets
import json
import pyaudio

class AssemblyAIStreaming:
    """Real-time transcription with AssemblyAI."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.sample_rate = 16000
        self.chunk_size = 1024

    async def stream_microphone(self):
        """Stream microphone audio for real-time transcription."""
        url = f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={self.sample_rate}"

        async with websockets.connect(
            url,
            extra_headers={"Authorization": self.api_key}
        ) as ws:
            # Start audio capture
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )

            print("Listening... (Ctrl+C to stop)")

            async def send_audio():
                while True:
                    data = stream.read(self.chunk_size)
                    await ws.send(data)
                    await asyncio.sleep(0.01)

            async def receive_transcript():
                async for message in ws:
                    msg = json.loads(message)
                    if msg.get("message_type") == "FinalTranscript":
                        print(f"Final: {msg['text']}")
                    elif msg.get("message_type") == "PartialTranscript":
                        print(f"Partial: {msg['text']}", end="\r")

            await asyncio.gather(send_audio(), receive_transcript())


# Usage
# streamer = AssemblyAIStreaming(api_key="your-key")
# asyncio.run(streamer.stream_microphone())
```

### Deepgram Streaming

```python
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
import asyncio

class DeepgramStreaming:
    """Real-time transcription with Deepgram."""

    def __init__(self, api_key: str):
        self.client = DeepgramClient(api_key)

    async def stream_file(self, audio_path: str):
        """Stream audio file for transcription."""
        connection = self.client.listen.live.v("1")

        def on_message(self, result, **kwargs):
            transcript = result.channel.alternatives[0].transcript
            if transcript:
                print(f"Transcript: {transcript}")

        def on_error(self, error, **kwargs):
            print(f"Error: {error}")

        connection.on(LiveTranscriptionEvents.Transcript, on_message)
        connection.on(LiveTranscriptionEvents.Error, on_error)

        options = LiveOptions(
            model="nova-2",
            language="en-US",
            smart_format=True,
            interim_results=True
        )

        await connection.start(options)

        # Stream audio data
        with open(audio_path, "rb") as f:
            while chunk := f.read(4096):
                await connection.send(chunk)
                await asyncio.sleep(0.1)

        await connection.finish()
```

## Audio Preprocessing

### Quality Enhancement

```python
from pydub import AudioSegment
import numpy as np

def preprocess_audio(
    audio_path: str,
    output_path: str,
    target_sample_rate: int = 16000,
    normalize: bool = True,
    remove_silence: bool = False
) -> str:
    """Preprocess audio for better transcription."""
    audio = AudioSegment.from_file(audio_path)

    # Convert to mono
    if audio.channels > 1:
        audio = audio.set_channels(1)

    # Resample
    audio = audio.set_frame_rate(target_sample_rate)

    # Normalize volume
    if normalize:
        audio = audio.normalize()

    # Remove leading/trailing silence
    if remove_silence:
        audio = audio.strip_silence(
            silence_len=500,
            silence_thresh=-40
        )

    # Export as mp3 (good quality, smaller size)
    audio.export(output_path, format="mp3", bitrate="128k")

    return output_path
```
