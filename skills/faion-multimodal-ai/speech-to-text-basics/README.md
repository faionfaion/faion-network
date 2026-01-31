---
id: speech-to-text-basics
name: "Speech-to-Text Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Speech-to-Text Basics

Convert audio to text using Whisper API and local models with timestamps, translation, and optimization.

## OpenAI Whisper API

```python
from openai import OpenAI
from pathlib import Path

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
    language: ISO-639-1 code (e.g., "en", "es", "uk")
    prompt: Guide transcription with context
    """
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language,
            response_format=response_format,
            prompt=prompt
        )

    return response if response_format == "text" else response

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

def translate_audio(audio_path: str) -> str:
    """Translate audio to English."""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.translations.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text
```

## Local Whisper

```python
import whisper
import torch

class LocalWhisper:
    """Local Whisper transcription."""

    def __init__(self, model_size: str = "base", device: str = None):
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

```python
from faster_whisper import WhisperModel
from typing import Generator, Dict

class FasterWhisperTranscriber:
    """Optimized Whisper using CTranslate2."""

    def __init__(
        self,
        model_size: str = "base",
        device: str = "auto",
        compute_type: str = "auto"
    ):
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

        # Collect segments
        all_segments = []
        full_text = ""

        for segment in segments:
            all_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "words": [
                    {"word": w.word, "start": w.start, "end": w.end, "probability": w.probability}
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

    def transcribe_stream(self, audio_path: str, **kwargs) -> Generator[Dict, None, None]:
        """Stream transcription segments."""
        segments, info = self.model.transcribe(audio_path, **kwargs)

        for segment in segments:
            yield {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            }
```

## Best Practices

1. **Audio Quality** - Use clear recordings, minimize noise, prefer lossless formats
2. **Performance** - Use faster-whisper for speed, appropriate model size, cache transcriptions
3. **Accuracy** - Provide language hint, use prompts for domain terms, post-process results
4. **Cost Optimization** - Use local models for high volume, compress audio, cache results

## Common Pitfalls

- Not specifying language code
- Poor audio quality
- Missing timestamp information
- Using large models unnecessarily

## Sources

- [OpenAI Whisper API Documentation](https://platform.openai.com/docs/guides/speech-to-text)
- [Whisper GitHub Repository](https://github.com/openai/whisper)
- [faster-whisper GitHub](https://github.com/guillaumekln/faster-whisper)
- [Whisper Model Performance Comparison](https://github.com/openai/whisper#available-models-and-languages)
