# Speech-to-Text Templates

## Production Transcription Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from enum import Enum
import logging
import os

class TranscriptionProvider(Enum):
    OPENAI = "openai"
    OPENAI_GPT4O = "openai_gpt4o"
    OPENAI_GPT4O_MINI = "openai_gpt4o_mini"
    LOCAL = "local"
    FASTER_WHISPER = "faster_whisper"
    ASSEMBLYAI = "assemblyai"
    DEEPGRAM = "deepgram"


@dataclass
class TranscriptionConfig:
    provider: TranscriptionProvider = TranscriptionProvider.OPENAI
    model_size: str = "large-v3-turbo"  # For local models
    language: Optional[str] = None
    word_timestamps: bool = False
    speaker_diarization: bool = False
    max_file_size_mb: int = 25
    supported_formats: List[str] = None
    fallback_provider: Optional[TranscriptionProvider] = None

    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = [
                ".mp3", ".wav", ".m4a", ".flac",
                ".webm", ".mp4", ".ogg", ".opus"
            ]


class TranscriptionService:
    """Production speech-to-text service with fallback support."""

    def __init__(self, config: Optional[TranscriptionConfig] = None):
        self.config = config or TranscriptionConfig()
        self.logger = logging.getLogger(__name__)
        self._init_provider()

    def _init_provider(self):
        """Initialize transcription provider."""
        if self.config.provider in [
            TranscriptionProvider.OPENAI,
            TranscriptionProvider.OPENAI_GPT4O,
            TranscriptionProvider.OPENAI_GPT4O_MINI
        ]:
            from openai import OpenAI
            self.client = OpenAI()

        elif self.config.provider == TranscriptionProvider.FASTER_WHISPER:
            from faster_whisper import WhisperModel
            self.model = WhisperModel(
                self.config.model_size,
                device="auto",
                compute_type="auto"
            )

        elif self.config.provider == TranscriptionProvider.ASSEMBLYAI:
            import assemblyai as aai
            aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
            self.transcriber = aai.Transcriber()

        elif self.config.provider == TranscriptionProvider.DEEPGRAM:
            from deepgram import DeepgramClient
            self.client = DeepgramClient(os.environ["DEEPGRAM_API_KEY"])

    def transcribe(
        self,
        audio_path: Union[str, Path],
        **kwargs
    ) -> Dict[str, Any]:
        """Transcribe audio file with automatic fallback."""
        audio_path = Path(audio_path)

        # Validate
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if audio_path.suffix.lower() not in self.config.supported_formats:
            raise ValueError(f"Unsupported format: {audio_path.suffix}")

        # Check file size
        size_mb = audio_path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_file_size_mb:
            self.logger.info(f"Large file ({size_mb:.1f}MB), chunking")
            return self._transcribe_large(audio_path, **kwargs)

        # Try primary provider
        try:
            result = self._transcribe_with_provider(
                audio_path,
                self.config.provider,
                **kwargs
            )
            return {"success": True, **result}

        except Exception as e:
            self.logger.error(f"Primary provider failed: {e}")

            # Try fallback
            if self.config.fallback_provider:
                try:
                    result = self._transcribe_with_provider(
                        audio_path,
                        self.config.fallback_provider,
                        **kwargs
                    )
                    return {"success": True, "fallback_used": True, **result}
                except Exception as e2:
                    self.logger.error(f"Fallback failed: {e2}")

            return {"success": False, "error": str(e)}

    def _transcribe_with_provider(
        self,
        audio_path: Path,
        provider: TranscriptionProvider,
        **kwargs
    ) -> Dict:
        """Route to appropriate provider."""
        if provider == TranscriptionProvider.OPENAI:
            return self._transcribe_openai(audio_path, "whisper-1", **kwargs)
        elif provider == TranscriptionProvider.OPENAI_GPT4O:
            return self._transcribe_openai(audio_path, "gpt-4o-transcribe", **kwargs)
        elif provider == TranscriptionProvider.OPENAI_GPT4O_MINI:
            return self._transcribe_openai(audio_path, "gpt-4o-mini-transcribe", **kwargs)
        elif provider == TranscriptionProvider.FASTER_WHISPER:
            return self._transcribe_faster_whisper(audio_path, **kwargs)
        elif provider == TranscriptionProvider.ASSEMBLYAI:
            return self._transcribe_assemblyai(audio_path, **kwargs)
        elif provider == TranscriptionProvider.DEEPGRAM:
            return self._transcribe_deepgram(audio_path, **kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def _transcribe_openai(
        self,
        audio_path: Path,
        model: str,
        **kwargs
    ) -> Dict:
        """Transcribe using OpenAI."""
        response_format = "verbose_json" if self.config.word_timestamps else "json"

        with open(audio_path, "rb") as f:
            response = self.client.audio.transcriptions.create(
                model=model,
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
                "duration": response.duration,
                "provider": "openai",
                "model": model
            }
        return {"text": response.text, "provider": "openai", "model": model}

    def _transcribe_faster_whisper(self, audio_path: Path, **kwargs) -> Dict:
        """Transcribe using faster-whisper."""
        segments, info = self.model.transcribe(
            str(audio_path),
            language=self.config.language,
            word_timestamps=self.config.word_timestamps,
            vad_filter=True
        )

        all_segments = []
        full_text = ""

        for segment in segments:
            all_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            })
            full_text += segment.text

        return {
            "text": full_text.strip(),
            "segments": all_segments,
            "language": info.language,
            "duration": info.duration,
            "provider": "faster_whisper"
        }

    def _transcribe_assemblyai(self, audio_path: Path, **kwargs) -> Dict:
        """Transcribe using AssemblyAI."""
        import assemblyai as aai

        config = aai.TranscriptionConfig(
            language_code=self.config.language,
            speaker_labels=self.config.speaker_diarization
        )

        transcript = self.transcriber.transcribe(str(audio_path), config=config)

        return {
            "text": transcript.text,
            "words": transcript.words,
            "utterances": transcript.utterances if self.config.speaker_diarization else None,
            "provider": "assemblyai"
        }

    def _transcribe_deepgram(self, audio_path: Path, **kwargs) -> Dict:
        """Transcribe using Deepgram."""
        from deepgram import PrerecordedOptions

        with open(audio_path, "rb") as f:
            source = {"buffer": f.read(), "mimetype": "audio/mp3"}

        options = PrerecordedOptions(
            model="nova-2",
            language=self.config.language or "en",
            smart_format=True,
            diarize=self.config.speaker_diarization
        )

        response = self.client.listen.prerecorded.v("1").transcribe_file(
            source, options
        )

        result = response.results.channels[0].alternatives[0]

        return {
            "text": result.transcript,
            "words": result.words,
            "confidence": result.confidence,
            "provider": "deepgram"
        }

    def _transcribe_large(self, audio_path: Path, **kwargs) -> Dict:
        """Handle large files with chunking."""
        from pydub import AudioSegment
        import tempfile

        audio = AudioSegment.from_file(str(audio_path))
        chunk_duration = 5 * 60 * 1000  # 5 minutes
        overlap = 5000  # 5 seconds

        chunks = []
        start = 0
        duration_ms = len(audio)

        while start < duration_ms:
            end = min(start + chunk_duration, duration_ms)
            chunk = audio[start:end]

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                chunk.export(f.name, format="mp3")
                result = self._transcribe_with_provider(
                    Path(f.name),
                    self.config.provider
                )
                chunks.append({
                    "start_ms": start,
                    "end_ms": end,
                    "text": result["text"]
                })
                Path(f.name).unlink()

            start = end - overlap

        full_text = " ".join(c["text"] for c in chunks)
        return {"text": full_text, "chunks": chunks}
```

## FastAPI Transcription Endpoint

```python
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import tempfile
import os
from pathlib import Path

app = FastAPI(title="Transcription API")

# Initialize service
service = TranscriptionService(TranscriptionConfig(
    provider=TranscriptionProvider.OPENAI_GPT4O_MINI,
    fallback_provider=TranscriptionProvider.FASTER_WHISPER,
    word_timestamps=True
))


class TranscriptionRequest(BaseModel):
    language: Optional[str] = None
    word_timestamps: bool = False
    speaker_diarization: bool = False


class TranscriptionResponse(BaseModel):
    success: bool
    text: Optional[str] = None
    segments: Optional[list] = None
    duration: Optional[float] = None
    error: Optional[str] = None


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = None
):
    """Transcribe uploaded audio file."""
    # Validate file type
    allowed_extensions = [".mp3", ".wav", ".m4a", ".flac", ".webm"]
    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format. Allowed: {allowed_extensions}"
        )

    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Update config with request params
        service.config.language = language

        # Transcribe
        result = service.transcribe(tmp_path)

        return TranscriptionResponse(
            success=result["success"],
            text=result.get("text"),
            segments=result.get("segments"),
            duration=result.get("duration"),
            error=result.get("error")
        )

    finally:
        # Cleanup
        os.unlink(tmp_path)


@app.post("/transcribe/async")
async def transcribe_async(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    webhook_url: Optional[str] = None
):
    """Queue transcription for background processing."""
    # Save file
    file_ext = Path(file.filename).suffix.lower()
    with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # Generate job ID
    import uuid
    job_id = str(uuid.uuid4())

    # Queue background task
    background_tasks.add_task(
        process_transcription,
        job_id,
        tmp_path,
        webhook_url
    )

    return {"job_id": job_id, "status": "queued"}


async def process_transcription(job_id: str, file_path: str, webhook_url: str):
    """Background transcription task."""
    import httpx

    try:
        result = service.transcribe(file_path)

        # Send webhook if configured
        if webhook_url:
            async with httpx.AsyncClient() as client:
                await client.post(webhook_url, json={
                    "job_id": job_id,
                    "result": result
                })

    finally:
        os.unlink(file_path)
```

## CLI Tool Template

```python
#!/usr/bin/env python3
"""
Speech-to-text CLI tool.

Usage:
    stt transcribe audio.mp3
    stt transcribe audio.mp3 --output transcript.txt
    stt transcribe audio.mp3 --format srt
    stt transcribe audio.mp3 --provider assemblyai
"""

import click
from pathlib import Path
import json


@click.group()
def cli():
    """Speech-to-Text CLI."""
    pass


@cli.command()
@click.argument("audio_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--format", "-f", type=click.Choice(["text", "json", "srt", "vtt"]), default="text")
@click.option("--language", "-l", help="Language code (e.g., en, uk, es)")
@click.option("--provider", "-p", type=click.Choice(["openai", "gpt4o", "gpt4o-mini", "local", "assemblyai"]), default="openai")
@click.option("--timestamps/--no-timestamps", default=False)
@click.option("--diarize/--no-diarize", default=False, help="Enable speaker diarization")
def transcribe(audio_file, output, format, language, provider, timestamps, diarize):
    """Transcribe an audio file."""
    click.echo(f"Transcribing: {audio_file}")

    # Map provider
    provider_map = {
        "openai": TranscriptionProvider.OPENAI,
        "gpt4o": TranscriptionProvider.OPENAI_GPT4O,
        "gpt4o-mini": TranscriptionProvider.OPENAI_GPT4O_MINI,
        "local": TranscriptionProvider.FASTER_WHISPER,
        "assemblyai": TranscriptionProvider.ASSEMBLYAI
    }

    config = TranscriptionConfig(
        provider=provider_map[provider],
        language=language,
        word_timestamps=timestamps,
        speaker_diarization=diarize
    )

    service = TranscriptionService(config)
    result = service.transcribe(audio_file)

    if not result["success"]:
        click.echo(f"Error: {result['error']}", err=True)
        raise SystemExit(1)

    # Format output
    if format == "text":
        output_content = result["text"]
    elif format == "json":
        output_content = json.dumps(result, indent=2)
    elif format == "srt":
        output_content = segments_to_srt(result.get("segments", []))
    elif format == "vtt":
        output_content = segments_to_vtt(result.get("segments", []))

    # Write or print
    if output:
        Path(output).write_text(output_content)
        click.echo(f"Saved to: {output}")
    else:
        click.echo(output_content)


def segments_to_srt(segments: list) -> str:
    """Convert segments to SRT format."""
    lines = []
    for i, seg in enumerate(segments, 1):
        start = format_timestamp(seg["start"], srt=True)
        end = format_timestamp(seg["end"], srt=True)
        lines.append(f"{i}")
        lines.append(f"{start} --> {end}")
        lines.append(seg["text"].strip())
        lines.append("")
    return "\n".join(lines)


def segments_to_vtt(segments: list) -> str:
    """Convert segments to VTT format."""
    lines = ["WEBVTT", ""]
    for seg in segments:
        start = format_timestamp(seg["start"], srt=False)
        end = format_timestamp(seg["end"], srt=False)
        lines.append(f"{start} --> {end}")
        lines.append(seg["text"].strip())
        lines.append("")
    return "\n".join(lines)


def format_timestamp(seconds: float, srt: bool = True) -> str:
    """Format seconds to timestamp."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds % 1) * 1000)

    if srt:
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"


if __name__ == "__main__":
    cli()
```

## Cost Calculator

```python
from dataclasses import dataclass
from typing import Dict


@dataclass
class TranscriptionCost:
    """Calculate and compare transcription costs."""

    # Pricing per minute (USD) - January 2026
    PRICING = {
        "whisper": 0.006,
        "gpt4o_transcribe": 0.006,
        "gpt4o_mini_transcribe": 0.003,
        "assemblyai_standard": 0.002,
        "assemblyai_best": 0.04,
        "deepgram_nova": 0.0043,
        "google_speech": 0.004,
        "azure_speech": 0.016,
    }

    # Self-hosted costs (monthly)
    SELF_HOSTED = {
        "gpu_instance": 276,  # Minimum GPU instance
        "devops_overhead": 100,  # Estimated maintenance
    }

    def calculate_api_cost(
        self,
        minutes: float,
        provider: str = "whisper"
    ) -> float:
        """Calculate API cost for given minutes."""
        rate = self.PRICING.get(provider, 0.006)
        return minutes * rate

    def calculate_monthly_costs(
        self,
        monthly_minutes: float
    ) -> Dict[str, float]:
        """Compare monthly costs across providers."""
        costs = {}

        for provider, rate in self.PRICING.items():
            costs[provider] = monthly_minutes * rate

        # Self-hosted break-even
        self_hosted_fixed = sum(self.SELF_HOSTED.values())
        costs["self_hosted_fixed"] = self_hosted_fixed

        return costs

    def recommend_provider(self, monthly_minutes: float) -> Dict:
        """Recommend optimal provider based on volume."""
        costs = self.calculate_monthly_costs(monthly_minutes)

        # Self-hosted break-even point (~500 hours / 30,000 minutes)
        break_even_minutes = 30000

        if monthly_minutes > break_even_minutes:
            recommendation = "self_hosted"
            reason = "Volume exceeds break-even point"
        elif monthly_minutes < 1000:
            recommendation = "gpt4o_mini_transcribe"
            reason = "Low volume, best accuracy/cost ratio"
        else:
            # Find cheapest API
            api_costs = {k: v for k, v in costs.items() if k != "self_hosted_fixed"}
            recommendation = min(api_costs, key=api_costs.get)
            reason = f"Lowest cost at {monthly_minutes} minutes/month"

        return {
            "recommendation": recommendation,
            "reason": reason,
            "monthly_cost": costs.get(recommendation, costs["self_hosted_fixed"]),
            "all_costs": costs
        }


# Usage example
calculator = TranscriptionCost()
result = calculator.recommend_provider(monthly_minutes=5000)
print(f"Recommended: {result['recommendation']}")
print(f"Monthly cost: ${result['monthly_cost']:.2f}")
```
