---
id: img-gen-tools
name: "Image Generation Tools & Production"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: image-generation
---

# Image Generation Tools & Production

Production-ready implementations for Stable Diffusion, Flux, and multi-provider image generation services.

## Stable Diffusion via Replicate

```python
import replicate

def generate_with_stable_diffusion(
    prompt: str,
    negative_prompt: str = "",
    width: int = 1024,
    height: int = 1024,
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5
) -> str:
    """Generate image with Stable Diffusion XL."""
    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        input={
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale
        }
    )
    return output[0]

def generate_with_flux(prompt: str, aspect_ratio: str = "1:1", num_outputs: int = 1) -> list:
    """Generate image with Flux (high quality)."""
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "num_outputs": num_outputs,
            "output_format": "webp",
            "output_quality": 90
        }
    )
    return output
```

## Production Image Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
import logging
import hashlib
import os
from openai import OpenAI

class ImageModel(Enum):
    DALLE3 = "dall-e-3"
    DALLE2 = "dall-e-2"
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
    """Production image generation service."""

    def __init__(self, config: Optional[ImageGenerationConfig] = None):
        self.config = config or ImageGenerationConfig()
        self.client = OpenAI()
        self.logger = logging.getLogger(__name__)

        if self.config.cache_enabled:
            os.makedirs(self.config.cache_dir, exist_ok=True)

    def generate(
        self,
        prompt: str,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        style: str = "vivid",
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Generate image with caching and retry."""
        size = size or self.config.default_size
        quality = quality or self.config.default_quality

        # Check cache
        if use_cache and self.config.cache_enabled:
            cached = self._get_cached(prompt, size, quality, style)
            if cached:
                self.logger.info("Cache hit")
                return cached

        # Generate with retry
        for attempt in range(self.config.max_retries):
            try:
                if self.config.model == ImageModel.DALLE3:
                    result = self._generate_dalle3(prompt, size, quality, style)
                elif self.config.model == ImageModel.SDXL:
                    result = self._generate_sdxl(prompt, size)
                else:
                    result = self._generate_dalle3(prompt, size, quality, style)

                # Cache result
                if self.config.cache_enabled:
                    self._cache_result(prompt, size, quality, style, result)

                return result

            except Exception as e:
                self.logger.error(f"Generation failed (attempt {attempt + 1}): {e}")
                if attempt == self.config.max_retries - 1:
                    raise

        return {"error": "Max retries exceeded"}

    def _generate_dalle3(self, prompt: str, size: str, quality: str, style: str) -> Dict:
        """Generate with DALL-E 3."""
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            style=style,
            n=1
        )

        return {
            "url": response.data[0].url,
            "revised_prompt": response.data[0].revised_prompt,
            "model": "dall-e-3"
        }

    def _generate_sdxl(self, prompt: str, size: str) -> Dict:
        """Generate with Stable Diffusion XL."""
        import replicate

        width, height = map(int, size.split("x"))
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={"prompt": prompt, "width": width, "height": height}
        )

        return {"url": output[0], "model": "sdxl"}

    def _get_cache_key(self, prompt: str, size: str, quality: str, style: str) -> str:
        content = f"{prompt}|{size}|{quality}|{style}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _get_cached(self, prompt: str, size: str, quality: str, style: str) -> Optional[Dict]:
        from pathlib import Path
        import json

        key = self._get_cache_key(prompt, size, quality, style)
        cache_file = Path(self.config.cache_dir) / f"{key}.json"

        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)
        return None

    def _cache_result(self, prompt: str, size: str, quality: str, style: str, result: Dict):
        from pathlib import Path
        import json

        key = self._get_cache_key(prompt, size, quality, style)
        cache_file = Path(self.config.cache_dir) / f"{key}.json"

        with open(cache_file, "w") as f:
            json.dump(result, f)

# Usage
service = ImageGenerationService(
    ImageGenerationConfig(cache_enabled=True, default_quality="hd")
)

result = service.generate("a minimalist logo for a tech startup", size="1024x1024")
```

## Multi-Provider Fallback

```python
class MultiProviderImageService:
    """Image service with provider fallback."""

    def __init__(self):
        self.providers = {
            "dalle3": self._generate_dalle3,
            "sdxl": self._generate_sdxl,
            "flux": self._generate_flux
        }
        self.logger = logging.getLogger(__name__)

    def generate(self, prompt: str, providers: List[str] = ["dalle3", "sdxl"], **kwargs) -> Dict:
        """Generate with fallback."""
        errors = {}

        for provider in providers:
            try:
                self.logger.info(f"Trying {provider}")
                return self.providers[provider](prompt, **kwargs)
            except Exception as e:
                self.logger.warning(f"{provider} failed: {e}")
                errors[provider] = str(e)

        raise Exception(f"All providers failed: {errors}")

    def _generate_dalle3(self, prompt: str, **kwargs) -> Dict:
        client = OpenAI()
        response = client.images.generate(model="dall-e-3", prompt=prompt, **kwargs)
        return {"url": response.data[0].url, "provider": "dalle3"}

    def _generate_sdxl(self, prompt: str, **kwargs) -> Dict:
        import replicate
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={"prompt": prompt, **kwargs}
        )
        return {"url": output[0], "provider": "sdxl"}

    def _generate_flux(self, prompt: str, **kwargs) -> Dict:
        import replicate
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={"prompt": prompt, **kwargs}
        )
        return {"url": output[0], "provider": "flux"}
```

## Prompt Templates

```python
class PromptTemplates:
    """Reusable prompt templates."""

    @staticmethod
    def product_photo(product: str, background: str = "white studio background", lighting: str = "professional studio lighting") -> str:
        return f"{product}, {background}, {lighting}, product photography, high quality, commercial, 4K"

    @staticmethod
    def logo(concept: str, style: str = "minimalist", colors: str = "modern color palette") -> str:
        return f"{style} logo design, {concept}, {colors}, vector art, clean, professional"

    @staticmethod
    def social_media(content: str, platform: str = "instagram", mood: str = "vibrant") -> str:
        return f"{content}, {mood} mood, social media post, eye-catching, {platform} style"

    @staticmethod
    def ui_mockup(screen: str, style: str = "modern", platform: str = "web") -> str:
        return f"{style} {platform} interface, {screen}, clean design, professional UI/UX, Figma style"

# Usage
templates = PromptTemplates()
prompt = templates.product_photo(
    product="wireless earbuds",
    background="gradient blue background",
    lighting="dramatic side lighting"
)
```

## Automated Image Pipeline

```python
class ImagePipeline:
    """Automated image generation pipeline."""

    def __init__(self, service: ImageGenerationService):
        self.service = service

    def generate_variant_set(self, base_prompt: str, styles: List[str], sizes: List[str]) -> Dict[str, List[Dict]]:
        """Generate multiple style and size variants."""
        results = {}

        for style in styles:
            style_results = []
            prompt = f"{base_prompt}, {style}"

            for size in sizes:
                result = self.service.generate(prompt=prompt, size=size)
                style_results.append({"size": size, "url": result["url"]})

            results[style] = style_results

        return results

    def a_b_test_images(self, concept: str, variations: List[str], size: str = "1024x1024") -> List[Dict]:
        """Generate A/B test image variants."""
        results = []

        for i, variation in enumerate(variations):
            prompt = f"{concept}, {variation}"
            result = self.service.generate(prompt=prompt, size=size)
            results.append({
                "variant": chr(65 + i),  # A, B, C...
                "variation": variation,
                "url": result["url"]
            })

        return results
```

## Best Practices

1. **Workflow Integration** - Automate common use cases, build templates, version control prompts
2. **Production Considerations** - Implement caching, add retry logic, handle fallbacks, monitor costs
3. **Quality Assurance** - Review generated images, A/B test variations, collect feedback

## Common Pitfalls

- No caching → regenerating same images
- Single provider → no fallback when API fails
- Hardcoded prompts → difficult to maintain
- No error handling → service failures break pipeline

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Generate images from prompts | haiku | API calls and parameter tuning |
| Create batch image variations | haiku | Mechanical image generation workflow |
| Design image generation pipeline | sonnet | Architecture and error handling |

## Sources

- [Replicate API Documentation](https://replicate.com/docs)
- [Stable Diffusion XL on Replicate](https://replicate.com/stability-ai/sdxl)
- [Flux Model Documentation](https://replicate.com/black-forest-labs/flux-schnell)
- [Midjourney API (Community)](https://docs.midjourney.com/)
