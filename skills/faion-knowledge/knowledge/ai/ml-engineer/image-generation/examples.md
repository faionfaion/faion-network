# Image Generation Code Examples

## DALL-E 3 (OpenAI)

### Basic Generation

```python
from openai import OpenAI
import requests
from pathlib import Path

client = OpenAI()

def generate_image(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "standard",
    style: str = "vivid",
) -> dict:
    """
    Generate image with DALL-E 3.

    Args:
        prompt: Image description
        size: "1024x1024", "1792x1024", "1024x1792"
        quality: "standard" or "hd"
        style: "vivid" or "natural"

    Returns:
        dict with url and revised_prompt
    """
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality=quality,
        style=style,
        n=1
    )

    return {
        "url": response.data[0].url,
        "revised_prompt": response.data[0].revised_prompt
    }


def generate_and_save(
    prompt: str,
    output_path: str,
    **kwargs
) -> str:
    """Generate image and save to file."""
    result = generate_image(prompt, **kwargs)

    response = requests.get(result["url"])
    response.raise_for_status()

    Path(output_path).write_bytes(response.content)
    return output_path
```

### Image Editing (DALL-E 2)

```python
def edit_image(
    image_path: str,
    mask_path: str,
    prompt: str,
    size: str = "1024x1024"
) -> str:
    """
    Edit image with mask (DALL-E 2 only).

    Mask should be RGBA PNG with transparent areas to edit.
    """
    with open(image_path, "rb") as img, open(mask_path, "rb") as mask:
        response = client.images.edit(
            image=img,
            mask=mask,
            prompt=prompt,
            n=1,
            size=size,
            model="dall-e-2"
        )

    return response.data[0].url


def create_variations(
    image_path: str,
    n: int = 3,
    size: str = "1024x1024"
) -> list[str]:
    """Generate variations of existing image (DALL-E 2 only)."""
    with open(image_path, "rb") as f:
        response = client.images.create_variation(
            image=f,
            n=n,
            size=size,
            model="dall-e-2"
        )

    return [img.url for img in response.data]
```

### GPT-4o Vision + Generation

```python
import base64

def describe_and_reimagine(
    image_path: str,
    style_modifier: str = ""
) -> dict:
    """Analyze image and create new version in different style."""
    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode()

    # Describe with GPT-4o
    description_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe this image in detail for image generation. "
                            "Include subject, composition, lighting, colors, mood."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}"
                    }
                }
            ]
        }]
    )

    description = description_response.choices[0].message.content

    # Combine with style modifier
    prompt = f"{description}. {style_modifier}" if style_modifier else description

    # Generate new image
    return generate_image(prompt)
```

---

## Stable Diffusion (Replicate)

### SDXL Basic

```python
import replicate

def generate_sdxl(
    prompt: str,
    negative_prompt: str = "",
    width: int = 1024,
    height: int = 1024,
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5,
    seed: int | None = None
) -> str:
    """
    Generate image with Stable Diffusion XL.

    Args:
        prompt: Image description
        negative_prompt: What to avoid
        width: Image width (max 1024)
        height: Image height (max 1024)
        num_inference_steps: Quality (20-50)
        guidance_scale: Prompt adherence (1-20, default 7.5)
        seed: Random seed for reproducibility

    Returns:
        Image URL
    """
    input_params = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "num_inference_steps": num_inference_steps,
        "guidance_scale": guidance_scale
    }

    if seed is not None:
        input_params["seed"] = seed

    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        input=input_params
    )

    return output[0]


def generate_sdxl_turbo(
    prompt: str,
    num_inference_steps: int = 4
) -> str:
    """Fast generation with SDXL Turbo (1-4 steps)."""
    output = replicate.run(
        "stability-ai/sdxl-turbo",
        input={
            "prompt": prompt,
            "num_inference_steps": num_inference_steps
        }
    )

    return output[0]
```

### Stable Diffusion 3.5

```python
def generate_sd3(
    prompt: str,
    negative_prompt: str = "",
    aspect_ratio: str = "1:1",
    output_format: str = "webp"
) -> str:
    """Generate with Stable Diffusion 3.5."""
    output = replicate.run(
        "stability-ai/stable-diffusion-3.5-large",
        input={
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "aspect_ratio": aspect_ratio,
            "output_format": output_format
        }
    )

    return output[0]
```

---

## Flux (Black Forest Labs)

### Flux via Replicate

```python
def generate_flux_schnell(
    prompt: str,
    aspect_ratio: str = "1:1",
    num_outputs: int = 1,
    output_format: str = "webp",
    output_quality: int = 90
) -> list[str]:
    """
    Fast generation with Flux schnell (Apache 2.0 license).

    Args:
        prompt: Image description
        aspect_ratio: "1:1", "16:9", "9:16", "4:3", "3:4"
        num_outputs: Number of images (1-4)
        output_format: "webp", "png", "jpg"
        output_quality: 1-100

    Returns:
        List of image URLs
    """
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "num_outputs": num_outputs,
            "output_format": output_format,
            "output_quality": output_quality
        }
    )

    return list(output)


def generate_flux_dev(
    prompt: str,
    aspect_ratio: str = "1:1",
    num_inference_steps: int = 28,
    guidance_scale: float = 3.5
) -> str:
    """Generate with Flux dev (non-commercial)."""
    output = replicate.run(
        "black-forest-labs/flux-dev",
        input={
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "num_inference_steps": num_inference_steps,
            "guidance": guidance_scale
        }
    )

    return output[0]


def generate_flux_pro(
    prompt: str,
    aspect_ratio: str = "1:1",
    safety_tolerance: int = 2
) -> str:
    """Generate with Flux pro (commercial, highest quality)."""
    output = replicate.run(
        "black-forest-labs/flux-1.1-pro",
        input={
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "safety_tolerance": safety_tolerance
        }
    )

    return output[0]
```

### Flux via BFL API

```python
import httpx

BFL_API_URL = "https://api.bfl.ml"

def generate_flux_bfl(
    prompt: str,
    model: str = "flux-pro-1.1",
    width: int = 1024,
    height: int = 1024,
    api_key: str = None
) -> str:
    """
    Generate with Flux via Black Forest Labs API.

    Models: flux-pro-1.1, flux-dev, flux-schnell
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Request generation
    response = httpx.post(
        f"{BFL_API_URL}/v1/image",
        headers=headers,
        json={
            "model": model,
            "prompt": prompt,
            "width": width,
            "height": height
        }
    )
    response.raise_for_status()

    task_id = response.json()["id"]

    # Poll for result
    while True:
        status_response = httpx.get(
            f"{BFL_API_URL}/v1/get_result",
            headers=headers,
            params={"id": task_id}
        )
        result = status_response.json()

        if result["status"] == "Ready":
            return result["result"]["sample"]
        elif result["status"] == "Failed":
            raise Exception(f"Generation failed: {result.get('error')}")

        import time
        time.sleep(0.5)
```

---

## Batch Generation

```python
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)


class BatchImageGenerator:
    """Generate multiple images efficiently."""

    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.client = OpenAI()

    def generate_batch(
        self,
        prompts: List[str],
        **kwargs
    ) -> List[Dict]:
        """Generate images for multiple prompts."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            futures = [
                (prompt, executor.submit(self._generate_single, prompt, **kwargs))
                for prompt in prompts
            ]

            for prompt, future in futures:
                try:
                    result = future.result()
                    results.append({
                        "prompt": prompt,
                        "success": True,
                        "url": result["url"],
                        "revised_prompt": result["revised_prompt"]
                    })
                except Exception as e:
                    logger.error(f"Failed: {prompt[:50]}... - {e}")
                    results.append({
                        "prompt": prompt,
                        "success": False,
                        "error": str(e)
                    })

        return results

    def _generate_single(self, prompt: str, **kwargs) -> dict:
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            **kwargs
        )
        return {
            "url": response.data[0].url,
            "revised_prompt": response.data[0].revised_prompt
        }

    def generate_variations_grid(
        self,
        base_prompt: str,
        variations: List[str],
        **kwargs
    ) -> List[Dict]:
        """Generate grid of prompt variations."""
        prompts = [f"{base_prompt}, {var}" for var in variations]
        return self.generate_batch(prompts, **kwargs)


# Usage
generator = BatchImageGenerator(max_concurrent=3)

results = generator.generate_variations_grid(
    base_prompt="A modern coffee shop interior",
    variations=[
        "minimalist Scandinavian style",
        "industrial exposed brick",
        "cozy bohemian atmosphere",
        "sleek Japanese aesthetic"
    ],
    size="1024x1024",
    quality="standard"
)
```

---

## Production Service

```python
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum
import hashlib
import json
import os
from pathlib import Path


class ImageModel(Enum):
    DALLE3 = "dall-e-3"
    DALLE2 = "dall-e-2"
    SDXL = "stable-diffusion-xl"
    FLUX_SCHNELL = "flux-schnell"
    FLUX_PRO = "flux-pro"


@dataclass
class ImageConfig:
    model: ImageModel = ImageModel.DALLE3
    default_size: str = "1024x1024"
    default_quality: str = "standard"
    max_retries: int = 3
    cache_enabled: bool = True
    cache_dir: str = "./image_cache"


class ImageService:
    """Production image generation with caching and retry."""

    def __init__(self, config: Optional[ImageConfig] = None):
        self.config = config or ImageConfig()
        self.client = OpenAI()

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
                return {**cached, "cached": True}

        # Generate with retry
        last_error = None
        for attempt in range(self.config.max_retries):
            try:
                result = self._generate(prompt, size, quality, style)

                if self.config.cache_enabled:
                    self._cache_result(prompt, size, quality, style, result)

                return {**result, "cached": False}

            except Exception as e:
                last_error = e
                if attempt < self.config.max_retries - 1:
                    import time
                    time.sleep(2 ** attempt)  # Exponential backoff

        raise last_error

    def _generate(
        self,
        prompt: str,
        size: str,
        quality: str,
        style: str
    ) -> Dict:
        if self.config.model == ImageModel.DALLE3:
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

        elif self.config.model == ImageModel.FLUX_SCHNELL:
            import replicate
            output = replicate.run(
                "black-forest-labs/flux-schnell",
                input={"prompt": prompt}
            )
            return {
                "url": output[0],
                "model": "flux-schnell"
            }

        raise ValueError(f"Unsupported model: {self.config.model}")

    def _cache_key(self, prompt: str, size: str, quality: str, style: str) -> str:
        content = f"{self.config.model.value}|{prompt}|{size}|{quality}|{style}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _get_cached(self, prompt: str, size: str, quality: str, style: str) -> Optional[Dict]:
        key = self._cache_key(prompt, size, quality, style)
        cache_file = Path(self.config.cache_dir) / f"{key}.json"

        if cache_file.exists():
            return json.loads(cache_file.read_text())
        return None

    def _cache_result(self, prompt: str, size: str, quality: str, style: str, result: Dict):
        key = self._cache_key(prompt, size, quality, style)
        cache_file = Path(self.config.cache_dir) / f"{key}.json"
        cache_file.write_text(json.dumps(result))
```

---

## Async Generation

```python
import asyncio
import httpx
from openai import AsyncOpenAI


async def generate_async(
    prompt: str,
    size: str = "1024x1024"
) -> dict:
    """Async image generation with DALL-E 3."""
    client = AsyncOpenAI()

    response = await client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        n=1
    )

    return {
        "url": response.data[0].url,
        "revised_prompt": response.data[0].revised_prompt
    }


async def generate_multiple_async(
    prompts: list[str],
    **kwargs
) -> list[dict]:
    """Generate multiple images concurrently."""
    tasks = [generate_async(prompt, **kwargs) for prompt in prompts]
    return await asyncio.gather(*tasks, return_exceptions=True)


# Usage
async def main():
    prompts = [
        "A serene mountain landscape at dawn",
        "A bustling Tokyo street at night",
        "A cozy library with warm lighting"
    ]

    results = await generate_multiple_async(prompts)

    for prompt, result in zip(prompts, results):
        if isinstance(result, Exception):
            print(f"Failed: {prompt[:30]}... - {result}")
        else:
            print(f"Success: {result['url']}")

# asyncio.run(main())
```
