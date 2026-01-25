# AI Image Generation Models - Part 1: DALL-E, Midjourney, FLUX

**DALL-E 3, Midjourney, FLUX API usage and parameters (2025-2026)**

---

## Quick Reference

| Model | Best For | Text in Images | Control Level | API | Cost |
|-------|----------|----------------|---------------|-----|------|
| **DALL-E 3** | Text rendering, commercial | Excellent | Medium | OpenAI | $0.04-0.12/image |
| **Midjourney v6.1** | Artistic, aesthetic | Good | Medium | Discord/API | $10-60/month |
| **FLUX.1 Pro** | Photorealism | Good | High | Replicate/fal.ai | $0.03-0.05/image |

For Stable Diffusion 3.5 and Ideogram 2.0, see [image-generation-sd-ideogram.md](image-generation-sd-ideogram.md)

---

## DALL-E 3 (OpenAI)

### Overview

OpenAI's flagship image generation model. Best-in-class for text rendering and commercial-safe content.

**Key Strengths:**
- Excellent text rendering in images
- Strong prompt following
- Built-in safety filters
- Automatic prompt enhancement (revised_prompt)

### API Usage

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var

# Basic generation
response = client.images.generate(
    model="dall-e-3",
    prompt="A minimalist logo for 'Faion Network' featuring an abstract neural network pattern in deep blue and silver, white background, vector style",
    size="1024x1024",      # "1024x1024" | "1792x1024" | "1024x1792"
    quality="hd",          # "standard" | "hd"
    style="vivid",         # "vivid" | "natural"
    n=1                    # DALL-E 3 supports only n=1
)

image_url = response.data[0].url
revised_prompt = response.data[0].revised_prompt  # What DALL-E actually used
```

### Parameters

| Parameter | Options | Description |
|-----------|---------|-------------|
| `model` | `dall-e-3`, `dall-e-2` | Model version |
| `size` | 1024x1024, 1792x1024, 1024x1792 | Output resolution |
| `quality` | `standard`, `hd` | Image quality (hd = more detail) |
| `style` | `vivid`, `natural` | Vivid = dramatic, Natural = realistic |
| `response_format` | `url`, `b64_json` | URL expires in 1 hour |
| `n` | 1 (DALL-E 3), 1-10 (DALL-E 2) | Number of images |

### Response Formats

```python
# URL response (default) - expires in 1 hour
response = client.images.generate(
    model="dall-e-3",
    prompt="...",
    response_format="url"
)
url = response.data[0].url

# Base64 response - for immediate use/storage
response = client.images.generate(
    model="dall-e-3",
    prompt="...",
    response_format="b64_json"
)
import base64
image_bytes = base64.b64decode(response.data[0].b64_json)
with open("image.png", "wb") as f:
    f.write(image_bytes)
```

### Image Editing (DALL-E 2 only)

```python
# Inpainting - edit specific regions
response = client.images.edit(
    model="dall-e-2",
    image=open("original.png", "rb"),
    mask=open("mask.png", "rb"),  # Transparent areas will be regenerated
    prompt="Add a red sports car in the parking lot",
    size="1024x1024",
    n=1
)

# Variations - create similar images
response = client.images.create_variation(
    model="dall-e-2",
    image=open("source.png", "rb"),
    size="1024x1024",
    n=3
)
```

### curl Example

```bash
source ~/.secrets/openai

curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A futuristic AI network visualization, dark blue background with glowing neural connections",
    "n": 1,
    "size": "1024x1024",
    "quality": "hd",
    "style": "vivid"
  }'
```

### Best Practices

1. **Be specific** - More detail = better results
2. **Use revised_prompt** - Check what DALL-E actually generated
3. **Natural style for realism** - Use `style: "natural"` for photos
4. **HD for detail** - Worth the extra cost for final assets
5. **Download immediately** - URLs expire in 1 hour

---

## Midjourney

### Overview

Industry-leading aesthetic quality. Best for artistic, stylized images. Recently launched official API.

**Key Strengths:**
- Exceptional aesthetic quality
- Strong community and style ecosystem
- Character reference (--cref) for consistency
- Style reference (--sref) for consistent aesthetics

### API Access

Midjourney now offers an official API (beta). Previously Discord-only.

```python
import requests
import time

MIDJOURNEY_API_KEY = "your-api-key"
BASE_URL = "https://api.midjourney.com/v1"

headers = {
    "Authorization": f"Bearer {MIDJOURNEY_API_KEY}",
    "Content-Type": "application/json"
}

# Submit generation request
response = requests.post(
    f"{BASE_URL}/imagine",
    headers=headers,
    json={
        "prompt": "portrait of a cyberpunk hacker, neon lights, cinematic --ar 16:9 --style raw --v 6.1",
        "webhook_url": "https://your-webhook.com/callback"  # Optional
    }
)

task_id = response.json()["task_id"]

# Poll for completion
while True:
    status = requests.get(
        f"{BASE_URL}/tasks/{task_id}",
        headers=headers
    ).json()

    if status["status"] == "completed":
        image_urls = status["images"]
        break
    elif status["status"] == "failed":
        raise Exception(f"Generation failed: {status['error']}")

    time.sleep(5)

# Upscale a specific image (U1, U2, U3, U4)
upscale_response = requests.post(
    f"{BASE_URL}/upscale",
    headers=headers,
    json={
        "task_id": task_id,
        "index": 1  # U1
    }
)
```

### Discord Bot Usage

For those without API access:

```
/imagine prompt: portrait of a scientist, dramatic lighting, oil painting style --ar 3:4 --v 6.1

Buttons:
U1-U4: Upscale individual images
V1-V4: Create variations
Re-roll: Generate new images
```

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--ar` | Aspect ratio | `--ar 16:9`, `--ar 3:4` |
| `--v` | Model version | `--v 6.1` |
| `--style` | Style preset | `--style raw` (less stylized) |
| `--chaos` | Variation (0-100) | `--chaos 50` |
| `--stylize` | Artistic influence (0-1000) | `--stylize 750` |
| `--no` | Negative prompt | `--no blur, watermark` |
| `--cref` | Character reference | `--cref [image_url]` |
| `--sref` | Style reference | `--sref [image_url]` |
| `--cw` | Character weight (0-100) | `--cw 50` |
| `--sw` | Style weight (0-1000) | `--sw 500` |
| `--tile` | Seamless patterns | `--tile` |
| `--seed` | Reproducibility | `--seed 12345` |
| `--q` | Quality (0.25, 0.5, 1) | `--q 1` |
| `--repeat` | Multiple generations | `--repeat 4` |

### Character Consistency (--cref)

```
/imagine portrait of a woman with red hair, business attire --cref https://example.com/character.jpg --cw 100

--cw values:
0: Only face
50: Face + some style
100: Full character reference
```

### Style Reference (--sref)

```
/imagine mountain landscape at sunset --sref https://example.com/style.jpg --sw 500

--sw values:
0-100: Subtle influence
100-500: Moderate influence
500-1000: Strong influence
```

---

## FLUX (Black Forest Labs)

### Overview

Open-source photorealistic image generation. Three variants for different use cases.

**Models:**
- **FLUX.1 Pro**: Highest quality, API only
- **FLUX.1 Dev**: Open-source, non-commercial
- **FLUX.1 Schnell**: Fast, 4 steps, Apache 2.0 license

### FLUX.1 Pro via Replicate

```python
import replicate

# FLUX.1 Pro - best quality
output = replicate.run(
    "black-forest-labs/flux-1.1-pro",
    input={
        "prompt": "Professional headshot of a CEO, studio lighting, neutral background, sharp focus",
        "aspect_ratio": "1:1",
        "output_format": "webp",
        "output_quality": 90,
        "safety_tolerance": 2,
        "prompt_upsampling": True
    }
)

image_url = output
print(f"Generated: {image_url}")
```

### FLUX.1 Dev via Replicate

```python
# FLUX.1 Dev - open weights, good quality
output = replicate.run(
    "black-forest-labs/flux-dev",
    input={
        "prompt": "Serene Japanese garden with cherry blossoms, koi pond, photorealistic",
        "guidance": 3.5,
        "num_inference_steps": 50,
        "aspect_ratio": "16:9",
        "output_format": "png"
    }
)
```

### FLUX.1 Schnell - Fast Generation

```python
# FLUX.1 Schnell - 4 steps, fastest
output = replicate.run(
    "black-forest-labs/flux-schnell",
    input={
        "prompt": "A golden retriever playing in autumn leaves",
        "num_inference_steps": 4,
        "aspect_ratio": "1:1"
    }
)
```

### FLUX via fal.ai

```python
import fal_client

# Text-to-Image
result = fal_client.subscribe(
    "fal-ai/flux-pro/v1.1",
    arguments={
        "prompt": "Minimalist product shot of wireless earbuds on marble surface",
        "image_size": "landscape_16_9",
        "num_images": 1,
        "enable_safety_checker": True
    }
)

image_url = result["images"][0]["url"]

# Image-to-Image with FLUX
result = fal_client.subscribe(
    "fal-ai/flux-pro/v1.1/redux",
    arguments={
        "image_url": "https://example.com/source.jpg",
        "prompt": "Same scene but at sunset with warm golden lighting",
        "strength": 0.7
    }
)
```

### ControlNet with FLUX

```python
# FLUX with Canny edge control
result = fal_client.subscribe(
    "fal-ai/flux-pro/v1.1/canny",
    arguments={
        "image_url": "https://example.com/pose_reference.jpg",
        "prompt": "Fashion model in designer outfit, studio photography",
        "control_strength": 0.8
    }
)

# FLUX with Depth control
result = fal_client.subscribe(
    "fal-ai/flux-pro/v1.1/depth",
    arguments={
        "image_url": "https://example.com/scene.jpg",
        "prompt": "Same composition but in watercolor painting style",
        "control_strength": 0.7
    }
)
```

---

## See Also

- **Part 2:** [image-generation-sd-ideogram.md](image-generation-sd-ideogram.md) - Stable Diffusion 3.5, Ideogram 2.0
- [OpenAI DALL-E Documentation](https://platform.openai.com/docs/guides/images)
- [Midjourney Documentation](https://docs.midjourney.com)
- [Black Forest Labs FLUX](https://blackforestlabs.ai)

---

*Part of Faion Network Marketing Manager Skill*
*Last Updated: 2026-01-23*


## Sources

- [DALL-E Platform](https://openai.com/dall-e-3)
- [Midjourney Showcase](https://www.midjourney.com/showcase)
- [Flux by Black Forest Labs](https://blackforestlabs.ai/)
- [AI Art Comparison Study](https://www.aiimagecomparison.com/)
- [Generative AI Tools Review](https://www.theverge.com/ai-artificial-intelligence)
