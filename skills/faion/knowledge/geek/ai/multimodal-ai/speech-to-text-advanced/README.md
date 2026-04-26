---
id: speech-to-text-advanced
name: "Speech-to-Text Advanced"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Speech-to-Text Advanced

Long audio processing, speaker diarization, and production STT services.

## Long Audio Processing

```python
from pydub import AudioSegment
from pathlib import Path
import tempfile
from typing import List, Dict

class LongAudioTranscriber:
    """Handle long audio files by chunking."""

    def __init__(self, chunk_duration_ms: int = 300000, overlap_ms: int = 5000):
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

        # Chunk and transcribe
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

            chunks.append({"audio": chunk, "start": start, "end": end})
            start = end - self.overlap

        return chunks

    def _transcribe_chunk(self, audio_path: str) -> str:
        with open(audio_path, "rb") as f:
            response = self.client.audio.transcriptions.create(model="whisper-1", file=f)
        return response

    def _merge_results(self, results: List[Dict]) -> Dict:
        full_text = results[0]["text"]
        for i in range(1, len(results)):
            full_text += " " + results[i]["text"]

        return {"text": full_text, "chunks": results}
```

## Speaker Diarization

```python
from pyannote.audio import Pipeline
from typing import Dict, List
import torch

class SpeakerDiarizer:
    """Add speaker labels to transcription."""

    def __init__(self, hf_token: str):
        """Requires HuggingFace token with pyannote access."""
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

    def align_with_transcript(self, audio_path: str, transcript_segments: List[Dict]) -> List[Dict]:
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

## Production Transcription Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from enum import Enum
import logging

class TranscriptionProvider(Enum):
    OPENAI = "openai"
    LOCAL = "local"
    FASTER_WHISPER = "faster_whisper"

@dataclass
class TranscriptionConfig:
    provider: TranscriptionProvider = TranscriptionProvider.OPENAI
    model_size: str = "base"
    language: Optional[str] = None
    word_timestamps: bool = False
    speaker_diarization: bool = False
    max_file_size_mb: int = 25
    supported_formats: List[str] = None

    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = [".mp3", ".wav", ".m4a", ".flac", ".webm", ".mp4"]

class TranscriptionService:
    """Production speech-to-text service."""

    def __init__(self, config: Optional[TranscriptionConfig] = None):
        self.config = config or TranscriptionConfig()
        self.logger = logging.getLogger(__name__)
        self._init_provider()

    def _init_provider(self):
        if self.config.provider == TranscriptionProvider.OPENAI:
            self.client = OpenAI()
        elif self.config.provider == TranscriptionProvider.FASTER_WHISPER:
            self.transcriber = FasterWhisperTranscriber(model_size=self.config.model_size)
        elif self.config.provider == TranscriptionProvider.LOCAL:
            self.transcriber = LocalWhisper(model_size=self.config.model_size)

    def transcribe(self, audio_path: Union[str, Path], **kwargs) -> Dict[str, Any]:
        """Transcribe audio file."""
        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if audio_path.suffix.lower() not in self.config.supported_formats:
            raise ValueError(f"Unsupported format: {audio_path.suffix}")

        # Check file size
        size_mb = audio_path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_file_size_mb:
            self.logger.info(f"Large file ({size_mb:.1f}MB), using chunked processing")
            return self._transcribe_large(audio_path, **kwargs)

        try:
            if self.config.provider == TranscriptionProvider.OPENAI:
                result = self._transcribe_openai(audio_path, **kwargs)
            else:
                result = self._transcribe_local(audio_path, **kwargs)

            return {"success": True, **result}

        except Exception as e:
            self.logger.error(f"Transcription failed: {e}")
            return {"success": False, "error": str(e)}

    def _transcribe_openai(self, audio_path: Path, **kwargs) -> Dict:
        response_format = "verbose_json" if self.config.word_timestamps else "json"

        with open(audio_path, "rb") as f:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=self.config.language,
                response_format=response_format,
                timestamp_granularities=["word", "segment"] if self.config.word_timestamps else None
            )

        if response_format == "verbose_json":
            return {
                "text": response.text,
                "segments": response.segments,
                "words": getattr(response, "words", None),
                "duration": response.duration
            }
        return {"text": response.text}

    def _transcribe_local(self, audio_path: Path, **kwargs) -> Dict:
        return self.transcriber.transcribe(
            str(audio_path),
            language=self.config.language,
            word_timestamps=self.config.word_timestamps
        )

    def _transcribe_large(self, audio_path: Path, **kwargs) -> Dict:
        processor = LongAudioTranscriber()
        return processor.transcribe(str(audio_path))
```

## Best Practices

1. **Production** - Implement retries, handle rate limits, monitor quality, validate file sizes
2. **Performance** - Chunk long audio, use faster-whisper for speed, cache transcriptions
3. **Quality** - Use speaker diarization for meetings, post-process transcripts, validate output

## Common Pitfalls

- Not chunking large files
- Missing timing information
- Not using diarization for multi-speaker audio
- Loading entire large files into memory

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Transcribe audio files | haiku | API calls and file handling |
| Implement speaker diarization | sonnet | Algorithm configuration and integration |
| Build multi-speaker transcription system | opus | Architecture and optimization |

## Sources

- [pyannote-audio Documentation](https://github.com/pyannote/pyannote-audio)
- [pydub Audio Processing](https://github.com/jiaaro/pydub)
- [Whisper Long-Form Transcription](https://github.com/openai/whisper#longer-than-30s)
- [Speaker Diarization Guide](https://huggingface.co/pyannote/speaker-diarization)
