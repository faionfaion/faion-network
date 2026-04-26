"""VideoGenerationService: async multi-provider routing with retry and download."""
import asyncio
import logging
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import httpx


class VideoProvider(Enum):
    RUNWAY = "runway"
    LUMA = "luma"
    REPLICATE = "replicate"


@dataclass
class VideoGenerationConfig:
    provider: VideoProvider = VideoProvider.REPLICATE
    default_duration: int = 5
    default_aspect_ratio: str = "16:9"
    max_retries: int = 3
    timeout: int = 600
    output_dir: str = "./generated_videos"


class VideoGenerationService:
    """Production async video generation service."""

    def __init__(self, config: Optional[VideoGenerationConfig] = None):
        self.config = config or VideoGenerationConfig()
        self.logger = logging.getLogger(__name__)
        Path(self.config.output_dir).mkdir(exist_ok=True)

    async def generate(self, prompt: str,
                       provider: Optional[VideoProvider] = None,
                       **kwargs) -> dict[str, Any]:
        provider = provider or self.config.provider
        for attempt in range(self.config.max_retries):
            try:
                result = await self._dispatch(provider, prompt, **kwargs)
                if result["status"] == "success":
                    output_path = await self._download_video(
                        result["video_url"], prompt[:50])
                    if not Path(output_path).exists() or Path(output_path).stat().st_size == 0:
                        return {"status": "failed", "error": "empty output file"}
                    result["local_path"] = output_path
                return result
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.config.max_retries - 1:
                    return {"status": "failed", "error": str(e)}
        return {"status": "failed", "error": "max retries exceeded"}

    async def _dispatch(self, provider: VideoProvider, prompt: str, **kwargs) -> dict:
        from video_gen_tools.templates.runway_generator import RunwayVideoGenerator
        from video_gen_tools.templates.luma_generator import LumaVideoGenerator
        from video_gen_tools.templates.replicate_generator import ReplicateVideoGenerator
        import os

        if provider == VideoProvider.RUNWAY:
            gen = RunwayVideoGenerator()
            return gen.generate_from_text(
                prompt,
                duration=kwargs.get("duration", self.config.default_duration),
                aspect_ratio=kwargs.get("aspect_ratio", self.config.default_aspect_ratio))
        elif provider == VideoProvider.LUMA:
            gen = LumaVideoGenerator(os.environ["LUMA_API_KEY"])
            return gen.generate(prompt,
                                aspect_ratio=kwargs.get("aspect_ratio",
                                                        self.config.default_aspect_ratio))
        else:
            gen = ReplicateVideoGenerator()
            url = gen.generate_with_zeroscope(prompt)
            return {"status": "success", "video_url": url}

    async def _download_video(self, url: str, name: str) -> str:
        """Stream download to avoid OOM on large files."""
        clean_name = re.sub(r"[^\w\s-]", "", name).strip()[:50]
        output_path = Path(self.config.output_dir) / f"{clean_name}.mp4"
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", url) as response:
                with open(output_path, "wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)
        return str(output_path)
