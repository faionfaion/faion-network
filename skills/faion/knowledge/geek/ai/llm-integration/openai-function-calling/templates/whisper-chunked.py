"""
purpose: Chunked Whisper transcription for audio files exceeding the 25MB API limit.
consumes: OpenAI client, audio file path, optional proper-noun prompt.
produces: full transcript string joined from chunk transcriptions.
depends-on: ffmpeg system binary, openai>=1.0.
token-budget-impact: pricing per audio minute; chunking does not increase cost.
"""
import subprocess
import tempfile
import os
from pathlib import Path
from openai import OpenAI


def transcribe_large(
    client: OpenAI,
    audio_path: str,
    chunk_minutes: int = 10,
    prompt: str = "",
) -> str:
    """Transcribe large audio file by splitting into chunks.

    Args:
        audio_path: Path to audio file (any ffmpeg-supported format).
        chunk_minutes: Duration of each chunk in minutes.
        prompt: Proper noun hints repeated on every chunk for consistency.
    Returns:
        Full transcript as a single joined string.
    """
    chunks_dir = tempfile.mkdtemp()
    chunk_pattern = os.path.join(chunks_dir, "chunk_%03d.mp3")

    subprocess.run([
        "ffmpeg", "-i", audio_path,
        "-f", "segment", "-segment_time", str(chunk_minutes * 60),
        "-c", "copy", chunk_pattern,
    ], check=True, capture_output=True)

    parts = []
    for chunk in sorted(Path(chunks_dir).glob("chunk_*.mp3")):
        with open(chunk, "rb") as f:
            kwargs = {"model": "whisper-1", "file": f}
            if prompt:
                kwargs["prompt"] = prompt  # repeat hint on every chunk
            parts.append(client.audio.transcriptions.create(**kwargs).text)

    return " ".join(parts)
