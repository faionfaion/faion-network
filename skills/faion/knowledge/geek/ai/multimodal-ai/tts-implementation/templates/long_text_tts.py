"""
LongTextTTS: chunk long text at sentence boundaries and concatenate audio segments.
Fixes: uses tempfile.mkdtemp() to avoid concurrent-agent path collisions.
"""
from __future__ import annotations

import re
import shutil
import tempfile
from pathlib import Path

from openai import OpenAI
from pydub import AudioSegment


class LongTextTTS:
    """Handle text exceeding the 4000-char OpenAI TTS limit."""

    def __init__(self, max_chars: int = 4000):
        self.max_chars = max_chars
        self.client = OpenAI()

    def synthesize(self, text: str, output_path: str, voice: str = "alloy") -> str:
        """Synthesize long text with automatic sentence-boundary chunking."""
        chunks = self._split_text(text)
        if not chunks:
            raise ValueError("Text produced no chunks after splitting")
        tmpdir = tempfile.mkdtemp()  # unique per call — safe for concurrent agents
        try:
            segments = []
            for i, chunk in enumerate(chunks):
                chunk_path = str(Path(tmpdir) / f"chunk_{i}.mp3")
                response = self.client.audio.speech.create(
                    model="tts-1",
                    voice=voice,
                    input=chunk,
                )
                response.stream_to_file(chunk_path)
                segments.append(AudioSegment.from_mp3(chunk_path))
            combined = segments[0]
            for seg in segments[1:]:
                combined += seg
            combined.export(output_path, format="mp3")
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
        return output_path

    def _split_text(self, text: str) -> list[str]:
        """
        Split text at sentence boundaries.
        WARNING: text with no sentence-ending punctuation (code, lists, data)
        produces a single chunk that may exceed max_chars. Pre-process such text.
        """
        chunks: list[str] = []
        current = ""
        for sentence in re.split(r'(?<=[.!?])\s+', text):
            if len(current) + len(sentence) <= self.max_chars:
                current += sentence + " "
            else:
                if current:
                    chunks.append(current.strip())
                current = sentence + " "
        if current:
            chunks.append(current.strip())
        return chunks
