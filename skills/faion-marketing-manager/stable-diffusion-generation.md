# Stable Diffusion 3.5 Image Generation

**Complete guide to Stable Diffusion 3.5 (2025-2026)**

---

## Overview

Open-weights model offering maximum control. Best for local deployment and custom workflows.

**Variants:**
- **SD 3.5 Large**: 8B parameters, highest quality
- **SD 3.5 Large Turbo**: 8B, distilled for speed
- **SD 3.5 Medium**: 2.5B parameters, balanced

---

## Local Installation

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

---

## Python with diffusers

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

---

## ControlNet with SD 3.5

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

---

## LoRA Fine-tuning

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

## ComfyUI Workflow Export

```json
{
  "workflow": {
    "nodes": [
      {
        "id": 1,
        "type": "CheckpointLoaderSimple",
        "inputs": {"ckpt_name": "sd3.5_large.safetensors"}
      },
      {
        "id": 2,
        "type": "CLIPTextEncode",
        "inputs": {"text": "beautiful landscape, mountains, sunset"}
      },
      {
        "id": 3,
        "type": "KSampler",
        "inputs": {
          "seed": 42,
          "steps": 28,
          "cfg": 4.5,
          "sampler_name": "euler",
          "scheduler": "normal"
        }
      },
      {
        "id": 4,
        "type": "VAEDecode",
        "inputs": {}
      },
      {
        "id": 5,
        "type": "SaveImage",
        "inputs": {"filename_prefix": "output"}
      }
    ]
  }
}
```

---

## Hardware Requirements

| Model | VRAM Required | Recommended GPU |
|-------|---------------|-----------------|
| SD 3.5 Large | 24GB+ | RTX 4090, A100 |
| SD 3.5 Large (fp8) | 12GB | RTX 4080, RTX 3090 |
| SD 3.5 Medium | 8GB | RTX 4070, RTX 3080 |
| SD 3.5 Large Turbo | 16GB | RTX 4080 |

---

## Model-Specific Tips

**Stable Diffusion:**
- Use LoRAs for consistent styles
- CFG scale 4-7 for SD 3.5
- Negative prompts are important
- ComfyUI for complex workflows

---

## References

- [Stability AI SD 3.5](https://stability.ai/stable-diffusion-3-5)
- [ComfyUI Workflows](https://github.com/comfyanonymous/ComfyUI)
