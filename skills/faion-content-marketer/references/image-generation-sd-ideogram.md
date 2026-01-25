# AI Image Generation Models - Part 2: Stable Diffusion, Ideogram

**Stable Diffusion 3.5, Ideogram 2.0 API usage and parameters (2025-2026)**

---

## Quick Reference

| Model | Best For | Text in Images | Control Level | API | Cost |
|-------|----------|----------------|---------------|-----|------|
| **SD 3.5 Large** | Maximum control, local | Moderate | Excellent | Self-hosted | Free (GPU costs) |
| **Ideogram 2.0** | Text in images, logos | Excellent | Medium | API | $0.02-0.08/image |

For DALL-E 3, Midjourney, and FLUX, see [image-generation-dalle-midjourney-flux.md](image-generation-dalle-midjourney-flux.md)

---

## Stable Diffusion 3.5

### Overview

Open-weights model offering maximum control. Best for local deployment and custom workflows.

**Variants:**
- **SD 3.5 Large**: 8B parameters, highest quality
- **SD 3.5 Large Turbo**: 8B, distilled for speed
- **SD 3.5 Medium**: 2.5B parameters, balanced

### Local Installation

```bash
# Using ComfyUI (recommended)
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt

# Download SD 3.5 Large model
# Place in ComfyUI/models/checkpoints/
# Get from huggingface.co/stabilityai/stable-diffusion-3.5-large

# Run ComfyUI
python main.py
```

### Python with diffusers

```python
from diffusers import StableDiffusion3Pipeline
import torch

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large",
    torch_dtype=torch.float16
)
pipe.to("cuda")

# Basic generation
image = pipe(
    prompt="A majestic lion in the savanna at golden hour, photorealistic, 8K",
    negative_prompt="blurry, low quality, distorted",
    num_inference_steps=28,
    guidance_scale=4.5,
    height=1024,
    width=1024
).images[0]

image.save("lion.png")
```

### ControlNet with SD 3.5

```python
from diffusers import StableDiffusion3ControlNetPipeline, SD3ControlNetModel
from diffusers.utils import load_image
import torch

# Load ControlNet model
controlnet = SD3ControlNetModel.from_pretrained(
    "stabilityai/stable-diffusion-3.5-controlnet-canny",
    torch_dtype=torch.float16
)

pipe = StableDiffusion3ControlNetPipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large",
    controlnet=controlnet,
    torch_dtype=torch.float16
)
pipe.to("cuda")

# Load control image
control_image = load_image("https://example.com/canny_edges.png")

# Generate with control
image = pipe(
    prompt="Modern architecture building, glass and steel, sunny day",
    control_image=control_image,
    controlnet_conditioning_scale=0.8,
    num_inference_steps=28
).images[0]
```

### LoRA Fine-tuning

```python
# Load base model with LoRA
from diffusers import StableDiffusion3Pipeline
import torch

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large",
    torch_dtype=torch.float16
)

# Load custom LoRA
pipe.load_lora_weights("path/to/custom_style.safetensors")
pipe.to("cuda")

# Generate with LoRA style
image = pipe(
    prompt="portrait of a person in custom_style",
    num_inference_steps=28
).images[0]
```

---

## Ideogram 2.0

### Overview

Specialized for text rendering in images. Excellent for logos, posters, and graphics with text.

**Key Strengths:**
- Best-in-class text rendering
- Good for logos and branding
- Clean, commercial-ready output

### API Usage

```python
import requests

IDEOGRAM_API_KEY = "your-api-key"

response = requests.post(
    "https://api.ideogram.ai/generate",
    headers={
        "Api-Key": IDEOGRAM_API_KEY,
        "Content-Type": "application/json"
    },
    json={
        "image_request": {
            "prompt": "A modern tech startup logo with the text 'FAION' in bold geometric font, blue and silver gradient, white background, vector style",
            "aspect_ratio": "ASPECT_1_1",
            "model": "V_2",
            "magic_prompt_option": "AUTO",
            "style_type": "DESIGN"
        }
    }
)

result = response.json()
image_url = result["data"][0]["url"]
```

### Parameters

| Parameter | Options | Description |
|-----------|---------|-------------|
| `model` | `V_2`, `V_2_TURBO` | Model version |
| `aspect_ratio` | `ASPECT_1_1`, `ASPECT_16_9`, `ASPECT_9_16`, etc. | Output ratio |
| `style_type` | `GENERAL`, `REALISTIC`, `DESIGN`, `RENDER_3D`, `ANIME` | Style preset |
| `magic_prompt_option` | `AUTO`, `ON`, `OFF` | Prompt enhancement |
| `seed` | Integer | Reproducibility |
| `negative_prompt` | String | What to avoid |

### Style Types

| Style | Best For |
|-------|----------|
| `GENERAL` | Mixed content |
| `REALISTIC` | Photos, product shots |
| `DESIGN` | Logos, graphics, flat design |
| `RENDER_3D` | 3D renders, product visualization |
| `ANIME` | Anime/manga style |

---

## References

- [Stability AI SD 3.5](https://stability.ai/stable-diffusion-3-5)
- [Ideogram Documentation](https://ideogram.ai/docs)
- [Replicate Model Library](https://replicate.com/models)
- [ComfyUI Workflows](https://github.com/comfyanonymous/ComfyUI)

---

## See Also

- **Part 1:** [image-generation-dalle-midjourney-flux.md](image-generation-dalle-midjourney-flux.md) - DALL-E 3, Midjourney, FLUX

---

*Part of Faion Network Marketing Manager Skill*
*Last Updated: 2026-01-23*


## Sources

- [Stable Diffusion Web](https://stablediffusionweb.com/)
- [Ideogram Platform](https://ideogram.ai/)
- [Civitai Models](https://civitai.com/)
- [Hugging Face Diffusion Models](https://huggingface.co/models?pipeline_tag=text-to-image)
- [AI Image Generation Research](https://arxiv.org/list/cs.CV/recent)
