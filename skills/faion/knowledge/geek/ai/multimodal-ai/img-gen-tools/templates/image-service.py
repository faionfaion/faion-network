"""
purpose: ImageService abstraction with SHA-keyed cache + provider registry + audit.
consumes: prompt + use_case + tenant_id + provider params
produces: storage_uri + revised_prompt + cost_usd
depends-on: content/01-core-rules.xml r1, r2, r6
token-budget-impact: per-call (provider cost); cache returns free after first generation
"""
import hashlib
import json
import logging
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from openai import OpenAI


class ImageModel(Enum):
    DALLE3 = "dall-e-3"
    SDXL = "stable-diffusion-xl"
    FLUX = "flux"


@dataclass
class ImageGenerationConfig:
    model: ImageModel = ImageModel.DALLE3
    default_size: str = "1024x1024"
    default_quality: str = "standard"
    max_retries: int = 3
    cache_enabled: bool = True
    cache_dir: str = "./image_cache"


class ImageGenerationService:
    """Production image generation with caching and retry."""

    def __init__(self, config: Optional[ImageGenerationConfig] = None):
        self.config = config or ImageGenerationConfig()
        self.client = OpenAI()
        self.logger = logging.getLogger(__name__)
        if self.config.cache_enabled:
            os.makedirs(self.config.cache_dir, exist_ok=True)

    def generate(self, prompt: str, size: Optional[str] = None,
                 quality: Optional[str] = None, style: str = "vivid",
                 use_cache: bool = True) -> dict[str, Any]:
        size = size or self.config.default_size
        quality = quality or self.config.default_quality
        # Normalize before hashing — strip+lower prevents cache misses for near-identical prompts
        norm_prompt = prompt.strip().lower()

        if use_cache and self.config.cache_enabled:
            cached = self._get_cached(norm_prompt, size, quality, style)
            if cached:
                self.logger.info("Cache hit")
                return cached

        for attempt in range(self.config.max_retries):
            try:
                if self.config.model == ImageModel.DALLE3:
                    result = self._generate_dalle3(prompt, size, quality, style)
                elif self.config.model == ImageModel.SDXL:
                    result = self._generate_sdxl(prompt, size)
                else:
                    result = self._generate_flux(prompt)

                if self.config.cache_enabled:
                    self._cache_result(norm_prompt, size, quality, style, result)
                return result
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1}: {e}")
                if attempt == self.config.max_retries - 1:
                    raise
        return {"error": "max retries exceeded"}

    def _generate_dalle3(self, prompt: str, size: str,
                         quality: str, style: str) -> dict:
        response = self.client.images.generate(
            model="dall-e-3", prompt=prompt,
            size=size, quality=quality, style=style, n=1
        )
        return {"url": response.data[0].url,
                "revised_prompt": response.data[0].revised_prompt,
                "provider": "dalle3"}

    def _generate_sdxl(self, prompt: str, size: str) -> dict:
        import replicate
        width, height = map(int, size.split("x"))
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={"prompt": prompt, "width": width, "height": height}
        )
        return {"url": output[0], "provider": "sdxl"}

    def _generate_flux(self, prompt: str) -> dict:
        import replicate
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={"prompt": prompt, "aspect_ratio": "1:1", "output_format": "webp"}
        )
        url = next(iter(output))  # flux-schnell returns iterator, not list
        return {"url": str(url), "provider": "flux"}

    def _cache_key(self, prompt: str, size: str, quality: str, style: str) -> str:
        return hashlib.sha256(f"{prompt}|{size}|{quality}|{style}".encode()).hexdigest()

    def _get_cached(self, prompt: str, size: str,
                    quality: str, style: str) -> Optional[dict]:
        key = self._cache_key(prompt, size, quality, style)
        cache_file = Path(self.config.cache_dir) / f"{key}.json"
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)
        return None

    def _cache_result(self, prompt: str, size: str,
                      quality: str, style: str, result: dict) -> None:
        key = self._cache_key(prompt, size, quality, style)
        cache_file = Path(self.config.cache_dir) / f"{key}.json"
        with open(cache_file, "w") as f:
            json.dump(result, f)
