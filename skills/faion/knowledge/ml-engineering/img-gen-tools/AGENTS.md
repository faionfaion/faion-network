# Image Generation Tools

## Summary

**One-sentence:** Produces a multi-provider image-generation service — DALL-E + Replicate (Flux/SDXL) + Stability adapter, S3 cache, prompt-template library, idempotent fallback.

**One-paragraph:** Above the single-provider basics, production pipelines need a stable abstraction across providers (so cost or capacity migrations are config-only), an S3 cache keyed by `sha1(prompt+provider+params)` (so retries don't double-bill), a prompt-template library mapping use cases (article-header, social-card, product-mockup) to structured prompts, and an idempotent fallback chain (`dalle3 → flux-schnell → sdxl`) triggered on provider failure or budget exhaustion. Output: a typed ImageService class + provider adapters + per-call audit log.

**Ефективно для:** content engineer / media pipeline, що генерує images у production з multi-tenant budget + provider rotation + cache-on-prompt + audit trail.

## Applies If (ALL must hold)

- Multiple use cases share the generation pipeline (article-header + social-card + product-mockup).
- A multi-provider strategy is desired (cost/capacity/quality routing).
- An S3-compatible cache is available.
- Pipeline tolerates the fallback provider's quality when primary fails.

## Skip If (ANY kills it)

- Single use case + single provider — `[[img-gen-basics]]` is sufficient.
- Pixel-perfect brand on one provider — fallback chain undermines consistency.
- No cache available — re-generating the same prompt is wasteful.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Provider API keys (OpenAI + Replicate + Stability) | secret | secrets manager |
| Prompt-template library keyed by use case | YAML | content repo |
| S3-compatible cache bucket | URI | infra |
| Per-tenant cost band | YAML | finops |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/multimodal-ai/img-gen-basics` | Single-provider baseline. |
| `geek/ai/llm-integration/ai-cost-attribution-schema` | Per-tenant attribution discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: provider abstraction, sha1-key cache, prompt template library, idempotent fallback, per-tenant attribution, audit log. | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for ImageService config + per-call audit log entry. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: cache key without params, no fallback, hardcoded provider, missing attribution, log without input hash. | ~700 |
| `content/04-procedure.xml` | medium | Steps: define template library → wire providers → cache layer → fallback chain → attribution → audit. | ~700 |
| `content/06-decision-tree.xml` | essential | Routes use case + cost band to a provider sequence. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft-template-library` | sonnet | YAML authoring. |
| `pick-fallback-chain` | opus | Cost vs quality reasoning. |
| `lint-cache-keys` | haiku | Pattern check on hash inputs. |

## Templates

| File | Purpose |
|---|---|
| `templates/image-service.py` | ImageService class with provider registry + cache + fallback. |
| `templates/multi-provider.py` | Provider adapters (DALL-E, Replicate, Stability). |
| `templates/cache-to-s3.py` | S3 cache layer keyed on sha1(prompt+provider+params). |
| `templates/prompt-templates.py` | Use-case → structured prompt template library. |
| `templates/prompt-generate.txt` | LLM-assisted prompt construction template. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-img-gen-tools.py` | Validate ImageService config: provider list, fallback chain, cache_uri, attribution enabled. | Pre-commit + CI. |

## Related

- [[img-gen-basics]]
- [[ai-cost-attribution-schema]]

## Decision tree

The tree at `content/06-decision-tree.xml` routes the use case (header/card/mockup) and the per-tenant cost band to a provider sequence (primary + fallbacks). Walk it before extending the use-case library so new use cases stay consistent with the cost discipline.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/image-service.py`

```python
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
```

### `templates/multi-provider.py`

```python
"""
import logging
from openai import OpenAI


class MultiProviderImageService:
    """Image generation with provider fallback. Result always includes provider field."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate(self, prompt: str,
                 providers: list[str] | None = None, **kwargs) -> dict:
        """
        Try providers in order; return first success.
        providers: ["dalle3", "flux", "sdxl"]
        Always include provider in result — silent fallback must be visible.
        """
        providers = providers or ["dalle3", "flux"]
        errors = {}
        for provider in providers:
            try:
                self.logger.info(f"Trying {provider}")
                result = self._dispatch(provider, prompt, **kwargs)
                result["provider"] = provider  # always expose which provider was used
                return result
            except Exception as e:
                self.logger.warning(f"{provider} failed: {e}")
                errors[provider] = str(e)
        raise RuntimeError(f"All providers failed: {errors}")

    def _dispatch(self, provider: str, prompt: str, **kwargs) -> dict:
        if provider == "dalle3":
            return self._dalle3(prompt, **kwargs)
        elif provider == "sdxl":
            return self._sdxl(prompt, **kwargs)
        elif provider == "flux":
            return self._flux(prompt, **kwargs)
        raise ValueError(f"Unknown provider: {provider}")

    def _dalle3(self, prompt: str, size: str = "1024x1024",
                quality: str = "standard", style: str = "vivid") -> dict:
        client = OpenAI()
        response = client.images.generate(
            model="dall-e-3", prompt=prompt, size=size, quality=quality,
            style=style, n=1
        )
        return {"url": response.data[0].url,
                "revised_prompt": response.data[0].revised_prompt}

    def _sdxl(self, prompt: str, size: str = "1024x1024", **_) -> dict:
        import replicate
        width, height = map(int, size.split("x"))
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={"prompt": prompt, "width": width, "height": height}
        )
        return {"url": output[0]}

    def _flux(self, prompt: str, **_) -> dict:
        import replicate
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={"prompt": prompt, "output_format": "webp"}
        )
        return {"url": str(next(iter(output)))}
```

### `templates/cache-to-s3.py`

```python
"""
import boto3
import hashlib
import requests


def cache_to_s3(url: str, prompt: str, bucket: str,
                prefix: str = "img-gen") -> str:
    """
    Download generated image and upload to S3. Returns permanent S3 URL.
    Resolves DALL-E/Flux pre-signed URL expiry (~1 hour).
    Idempotent: checks S3 before downloading.
    """
    key = hashlib.sha256(prompt.strip().lower().encode()).hexdigest()[:16]
    ext = "webp" if "webp" in url else "png"
    s3_key = f"{prefix}/{key}.{ext}"
    s3 = boto3.client("s3")

    # Check if already uploaded — avoid re-downloading
    try:
        s3.head_object(Bucket=bucket, Key=s3_key)
        return f"https://{bucket}.s3.amazonaws.com/{s3_key}"
    except s3.exceptions.ClientError:
        pass

    data = requests.get(url, timeout=30).content
    s3.put_object(Bucket=bucket, Key=s3_key, Body=data,
                  ContentType=f"image/{ext}")
    return f"https://{bucket}.s3.amazonaws.com/{s3_key}"
```

### `templates/prompt-templates.py`

```python
"""


class PromptTemplates:
    """Reusable prompt templates. Use as single source of truth — avoid ad-hoc strings."""

    @staticmethod
    def product_photo(product: str,
                      background: str = "white studio background",
                      lighting: str = "professional studio lighting") -> str:
        return (f"{product}, {background}, {lighting}, "
                "product photography, high quality, commercial, 4K")

    @staticmethod
    def logo(concept: str, style: str = "minimalist",
             colors: str = "modern color palette") -> str:
        return (f"{style} logo design, {concept}, {colors}, "
                "vector art, clean, professional")

    @staticmethod
    def social_media(content: str, platform: str = "instagram",
                     mood: str = "vibrant") -> str:
        return (f"{content}, {mood} mood, social media post, "
                f"eye-catching, {platform} style")

    @staticmethod
    def ui_mockup(screen: str, style: str = "modern",
                  platform: str = "web") -> str:
        return (f"{style} {platform} interface, {screen}, "
                "clean design, professional UI/UX, Figma style")


def select_provider(use_case: str) -> str:
    """Provider selection heuristic by use case."""
    return {
        "product_photo": "dalle3",   # best photorealism
        "logo": "dalle3",            # clean vector-like output
        "social_media": "flux",      # fast and cheap for volume
        "mockup": "sdxl",            # controllable composition
    }.get(use_case, "dalle3")
```

### `templates/prompt-generate.txt`

```text
-->
<task>
Generate production image for:
<brief>{BRIEF}</brief>

Provider: {PROVIDER}  (dalle3|sdxl|flux)
Template: {TEMPLATE}  (product_photo|logo|social_media|ui_mockup)
Size: {SIZE}
Cache: enabled

Return: {"url": "...", "provider": "...", "revised_prompt": "...", "cached": true|false}
On error: {"error": "...", "provider": "..."}

Rules:
- Use PromptTemplates.{TEMPLATE}() to build the prompt — not ad-hoc strings
- Log revised_prompt alongside original for DALL-E 3
- Download and cache to S3 immediately — provider URLs expire in ~1 hour
- On content policy rejection: return error, do NOT retry same prompt
</task>
```
