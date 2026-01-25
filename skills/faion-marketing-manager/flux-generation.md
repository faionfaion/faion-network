# FLUX Image Generation

**Complete guide to FLUX models (Black Forest Labs) (2025-2026)**

---

## Overview

Open-source photorealistic image generation. Three variants for different use cases.

**Models:**
- **FLUX.1 Pro**: Highest quality, API only
- **FLUX.1 Dev**: Open-source, non-commercial
- **FLUX.1 Schnell**: Fast, 4 steps, Apache 2.0 license

---

## FLUX.1 Pro via Replicate

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

---

## FLUX.1 Dev via Replicate

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

---

## FLUX.1 Schnell - Fast Generation

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

---

## FLUX via fal.ai

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

---

## ControlNet with FLUX

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

## Pricing (API Providers)

| Provider | FLUX Pro | FLUX Dev | FLUX Schnell |
|----------|----------|----------|--------------|
| Replicate | ~$0.03-0.05/image | ~$0.02/image | ~$0.003/image |
| fal.ai | ~$0.03-0.05/image | ~$0.02/image | ~$0.003/image |
| BFL API | ~$0.04/image | - | - |

---

## Model-Specific Tips

**FLUX:**
- More literal prompt following
- Good with technical photography terms
- Supports longer prompts well
- Use `prompt_upsampling` for enhancement

---

## References

- [Black Forest Labs FLUX](https://blackforestlabs.ai)
- [Replicate Model Library](https://replicate.com/models)
