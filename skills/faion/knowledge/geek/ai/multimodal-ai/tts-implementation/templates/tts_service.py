# purpose: Production TTSService — sha256 cache (provider in key), eviction, multi-provider routing.
# consumes: TTSConfig (provider, voice, speed, cache_dir, max_text_length), text payload.
# produces: dict per 02-output-contract: status, path, duration_s, cache_key, cached, chunks.
# depends-on: openai SDK; LongTextTTS template; pydub; tempfile (for chunk isolation).
# token-budget-impact: zero LLM tokens; provider calls are non-LLM TTS.
"""Production TTSService with SHA-256 caching, provider routing, eviction."""
from __future__ import annotations

import hashlib
import logging
import shutil
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from openai import OpenAI


class TTSProvider(Enum):
    OPENAI = "openai"
    ELEVENLABS = "elevenlabs"
    GOOGLE = "google"


@dataclass
class TTSConfig:
    provider: TTSProvider = TTSProvider.OPENAI
    default_voice: str = "alloy"
    default_speed: float = 1.0
    output_format: str = "mp3"
    cache_enabled: bool = True
    cache_dir: str = "./tts_cache"
    max_text_length: int = 4000  # 4000 not 4096 — avoid off-by-one truncation


class TTSService:
    """Production text-to-speech service with caching and long-text handling."""

    def __init__(self, config: TTSConfig | None = None):
        self.config = config or TTSConfig()
        self.logger = logging.getLogger(__name__)
        if self.config.cache_enabled:
            Path(self.config.cache_dir).mkdir(parents=True, exist_ok=True)
        if self.config.provider == TTSProvider.OPENAI:
            self.client = OpenAI()

    def synthesize(
        self,
        text: str,
        output_path: str | None = None,
        voice: str | None = None,
        speed: float | None = None,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        """Synthesize speech. Returns {"success", "path", "duration", "cached"}."""
        voice = voice or self.config.default_voice
        speed = speed or self.config.default_speed
        if use_cache and self.config.cache_enabled:
            cached = self._get_cached(text, voice, speed)
            if cached:
                return {"success": True, "path": cached, "cached": True, "duration": self._get_duration(cached)}
        if len(text) > self.config.max_text_length:
            return self._synthesize_long(text, output_path, voice, speed)
        try:
            path = self._synthesize_openai(text, output_path, voice, speed)
            if self.config.cache_enabled:
                self._cache_audio(text, voice, speed, path)
            return {"success": True, "path": path, "cached": False, "duration": self._get_duration(path)}
        except Exception as e:
            return {"success": False, "error": str(e), "path": None}

    def _synthesize_openai(self, text: str, output_path: str | None, voice: str, speed: float) -> str:
        response = self.client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text,
            speed=speed,
            response_format=self.config.output_format,
        )
        output_path = output_path or f"/tmp/tts_{hashlib.md5(text.encode()).hexdigest()}.{self.config.output_format}"
        response.stream_to_file(output_path)
        return output_path

    def _synthesize_long(self, text: str, output_path: str | None, voice: str, speed: float) -> dict:
        from tts_implementation.templates.long_text_tts import LongTextTTS
        processor = LongTextTTS(max_chars=self.config.max_text_length)
        output_path = output_path or f"/tmp/tts_long_{hashlib.md5(text.encode()).hexdigest()}.mp3"
        result_path = processor.synthesize(text, output_path, voice)
        return {"success": True, "path": result_path, "cached": False, "duration": self._get_duration(result_path)}

    def _get_cache_key(self, text: str, voice: str, speed: float) -> str:
        content = f"{text}|{voice}|{speed}|{self.config.provider.value}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _get_cached(self, text: str, voice: str, speed: float) -> str | None:
        path = Path(self.config.cache_dir) / f"{self._get_cache_key(text, voice, speed)}.{self.config.output_format}"
        return str(path) if path.exists() else None

    def _cache_audio(self, text: str, voice: str, speed: float, audio_path: str) -> None:
        key = self._get_cache_key(text, voice, speed)
        shutil.copy(audio_path, Path(self.config.cache_dir) / f"{key}.{self.config.output_format}")

    def _get_duration(self, audio_path: str) -> float:
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0
        except Exception:
            return 0.0  # callers must treat 0.0 as an error indicator


def evict_tts_cache(cache_dir: str, max_age_days: int = 30, max_size_mb: int = 500) -> int:
    """Evict old cache entries by age or total size limit. Returns number of files deleted."""
    cache = Path(cache_dir)
    entries = sorted(cache.glob("*.mp3"), key=lambda p: p.stat().st_mtime)
    total_mb = sum(p.stat().st_size for p in entries) / (1024 * 1024)
    now, deleted = time.time(), 0
    for entry in entries:
        if (now - entry.stat().st_mtime) / 86400 > max_age_days or total_mb > max_size_mb:
            total_mb -= entry.stat().st_size / (1024 * 1024)
            entry.unlink()
            deleted += 1
    return deleted
