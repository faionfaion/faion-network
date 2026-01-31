# AI Image Generation Workflows

**Production workflows for image generation, editing, and asset management**

---

## Image-to-Image

### Style Transfer

Transform existing images while preserving structure.

```python
# FLUX Redux for style transfer
import fal_client

result = fal_client.subscribe(
    "fal-ai/flux-pro/v1.1/redux",
    arguments={
        "image_url": "https://example.com/photo.jpg",
        "prompt": "Same scene in impressionist painting style, vibrant colors",
        "strength": 0.6  # 0.3-0.8 typical range
    }
)

# Stable Diffusion img2img
from diffusers import StableDiffusion3Img2ImgPipeline
from diffusers.utils import load_image

pipe = StableDiffusion3Img2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large",
    torch_dtype=torch.float16
)
pipe.to("cuda")

init_image = load_image("photo.png").resize((1024, 1024))

image = pipe(
    prompt="oil painting style, impressionist brush strokes",
    image=init_image,
    strength=0.7,  # How much to change (0-1)
    num_inference_steps=28
).images[0]
```

### Strength Parameter

| Strength | Effect |
|----------|--------|
| 0.3-0.4 | Subtle changes, preserve most details |
| 0.5-0.6 | Moderate transformation |
| 0.7-0.8 | Significant changes, keep composition |
| 0.9+ | Almost complete regeneration |

### Upscaling

```python
# Using Real-ESRGAN via Replicate
import replicate

output = replicate.run(
    "nightmareai/real-esrgan:350d32041630ffbe63c8352783a26d94126809164e54085352f8571e3d4edd3b",
    input={
        "image": open("low_res.png", "rb"),
        "scale": 4,  # 2x or 4x
        "face_enhance": True
    }
)

# Using FLUX for creative upscaling
output = replicate.run(
    "black-forest-labs/flux-1.1-pro-ultra",
    input={
        "image": open("source.png", "rb"),
        "prompt": "enhance details, sharp focus, 4K resolution",
        "aspect_ratio": "1:1",
        "output_quality": 100
    }
)
```

### Background Removal

```python
# Using remove.bg API
import requests

response = requests.post(
    "https://api.remove.bg/v1.0/removebg",
    files={"image_file": open("photo.png", "rb")},
    data={"size": "auto"},
    headers={"X-Api-Key": "YOUR_API_KEY"}
)

with open("no_bg.png", "wb") as f:
    f.write(response.content)

# Using Replicate
output = replicate.run(
    "lucataco/remove-bg:95fcc2a26d3899cd6c2691c900465aaeff466285a65c14638cc5f36f34befaf1",
    input={"image": open("photo.png", "rb")}
)
```

---

## Inpainting and Outpainting

### Inpainting (Edit Regions)

Edit specific parts of an image while keeping the rest.

```python
# DALL-E 2 Inpainting
from openai import OpenAI
client = OpenAI()

response = client.images.edit(
    model="dall-e-2",
    image=open("scene.png", "rb"),
    mask=open("mask.png", "rb"),  # White = keep, Transparent = edit
    prompt="A golden retriever sitting on the grass",
    size="1024x1024"
)

# Stable Diffusion Inpainting
from diffusers import StableDiffusionInpaintPipeline
from diffusers.utils import load_image

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-inpainting",
    torch_dtype=torch.float16
)
pipe.to("cuda")

init_image = load_image("scene.png").resize((512, 512))
mask_image = load_image("mask.png").resize((512, 512))

image = pipe(
    prompt="a beautiful flower garden",
    image=init_image,
    mask_image=mask_image,
    num_inference_steps=50
).images[0]
```

### Creating Masks

```python
# Automatic mask with Segment Anything
from segment_anything import SamPredictor, sam_model_registry
import numpy as np
from PIL import Image

sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h.pth")
predictor = SamPredictor(sam)

image = np.array(Image.open("photo.png"))
predictor.set_image(image)

# Point-based segmentation
masks, scores, _ = predictor.predict(
    point_coords=np.array([[500, 300]]),  # Click point
    point_labels=np.array([1]),  # 1 = foreground
    multimask_output=True
)

# Save best mask
best_mask = masks[np.argmax(scores)]
mask_image = Image.fromarray((best_mask * 255).astype(np.uint8))
mask_image.save("mask.png")
```

### Outpainting (Expand Canvas)

```python
# DALL-E 2 Outpainting
from PIL import Image
import numpy as np

# Create expanded canvas with transparent edges
original = Image.open("original.png")
expanded = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))

# Center original in expanded canvas
x_offset = (1024 - original.width) // 2
y_offset = (1024 - original.height) // 2
expanded.paste(original, (x_offset, y_offset))

# Create mask (white = keep, transparent = generate)
mask = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
mask.paste(Image.new("RGB", original.size, (255, 255, 255)), (x_offset, y_offset))

# Save for API
expanded.save("expanded.png")
mask.save("outpaint_mask.png")

# Use with DALL-E 2 edit endpoint
response = client.images.edit(
    model="dall-e-2",
    image=open("expanded.png", "rb"),
    mask=open("outpaint_mask.png", "rb"),
    prompt="continuation of the landscape scene, same style",
    size="1024x1024"
)
```

---

## Production Workflows

### Asset Generation Pipeline

```python
import os
import json
import hashlib
from datetime import datetime

class ImageGenerationPipeline:
    def __init__(self, output_dir: str = "generated_assets"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.manifest = []

    def generate_dall_e(self, prompt: str, **kwargs) -> dict:
        from openai import OpenAI
        client = OpenAI()

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=kwargs.get("size", "1024x1024"),
            quality=kwargs.get("quality", "hd"),
            style=kwargs.get("style", "vivid"),
            response_format="b64_json"
        )

        # Save image
        import base64
        image_data = base64.b64decode(response.data[0].b64_json)
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        filename = f"dalle3_{prompt_hash}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(image_data)

        # Record metadata
        metadata = {
            "model": "dall-e-3",
            "prompt": prompt,
            "revised_prompt": response.data[0].revised_prompt,
            "filepath": filepath,
            "timestamp": datetime.now().isoformat(),
            "params": kwargs
        }
        self.manifest.append(metadata)

        return metadata

    def generate_flux(self, prompt: str, **kwargs) -> dict:
        import replicate

        model = kwargs.get("model", "black-forest-labs/flux-1.1-pro")
        output = replicate.run(
            model,
            input={
                "prompt": prompt,
                "aspect_ratio": kwargs.get("aspect_ratio", "1:1"),
                "output_format": kwargs.get("format", "png")
            }
        )

        # Download image
        import requests
        response = requests.get(output)
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        filename = f"flux_{prompt_hash}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        metadata = {
            "model": model,
            "prompt": prompt,
            "filepath": filepath,
            "timestamp": datetime.now().isoformat(),
            "params": kwargs
        }
        self.manifest.append(metadata)

        return metadata

    def save_manifest(self):
        manifest_path = os.path.join(self.output_dir, "manifest.json")
        with open(manifest_path, "w") as f:
            json.dump(self.manifest, f, indent=2)

# Usage
pipeline = ImageGenerationPipeline("project_assets")

# Generate hero images
for style in ["professional", "creative", "minimalist"]:
    pipeline.generate_dall_e(
        f"Hero image for tech startup, {style} style, abstract neural network pattern",
        quality="hd",
        size="1792x1024"
    )

pipeline.save_manifest()
```

### Batch Generation

```python
import asyncio
from typing import List, Dict

async def batch_generate(prompts: List[str], model: str = "flux") -> List[Dict]:
    """Generate multiple images concurrently."""
    import aiohttp
    import replicate

    async def generate_one(prompt: str) -> Dict:
        output = await asyncio.to_thread(
            replicate.run,
            "black-forest-labs/flux-1.1-pro",
            input={"prompt": prompt, "aspect_ratio": "1:1"}
        )
        return {"prompt": prompt, "url": output}

    tasks = [generate_one(p) for p in prompts]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return [r for r in results if not isinstance(r, Exception)]

# Usage
prompts = [
    "Product shot of wireless earbuds on marble",
    "Product shot of smartwatch on wooden desk",
    "Product shot of laptop in modern office",
]

results = asyncio.run(batch_generate(prompts))
```

### A/B Testing Images

```python
def generate_variants(base_prompt: str, variations: List[str], model: str = "dall-e-3") -> List[Dict]:
    """Generate prompt variations for A/B testing."""
    from openai import OpenAI
    client = OpenAI()

    results = []
    for variation in variations:
        full_prompt = f"{base_prompt}, {variation}"
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size="1024x1024",
            quality="standard"
        )
        results.append({
            "variation": variation,
            "prompt": full_prompt,
            "revised_prompt": response.data[0].revised_prompt,
            "url": response.data[0].url
        })

    return results

# Test different styles
variants = generate_variants(
    base_prompt="Landing page hero image for AI productivity app",
    variations=[
        "minimalist design, blue gradient",
        "vibrant colors, abstract shapes",
        "dark theme, neon accents",
        "natural lighting, workspace setting"
    ]
)
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

## Ethical Considerations

### Content Guidelines

1. **Consent** - Don't generate images of real people without permission
2. **Deepfakes** - Avoid creating misleading content
3. **Copyright** - Don't replicate copyrighted characters/art
4. **NSFW** - Follow platform content policies
5. **Attribution** - Credit AI generation when required

### Safety Filters

All major platforms have content safety filters:

| Platform | Safety Level |
|----------|--------------|
| DALL-E 3 | Strict, built-in |
| Midjourney | Strict, terms enforced |
| FLUX Pro | Configurable (1-6) |
| SD 3.5 | Local = user responsibility |

### Licensing

| Model | Commercial Use |
|-------|----------------|
| DALL-E 3 | Yes |
| Midjourney | Yes (paid plans) |
| FLUX Pro | Yes |
| FLUX Dev | Non-commercial only |
| FLUX Schnell | Yes (Apache 2.0) |
| SD 3.5 | Check specific license |

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Blurry output | Low resolution, wrong model | Use HD quality, larger size |
| Wrong subject | Ambiguous prompt | Be more specific, use negative prompts |
| Distorted faces | Model limitation | Use portrait-specific models |
| Wrong text | Model weakness | Use DALL-E 3 or Ideogram |
| Inconsistent style | Prompt drift | Use style references, seed values |
| API timeout | Long generation | Increase timeout, use async |
| Rate limited | Too many requests | Implement backoff, queue requests |

### Quality Checklist

Before using generated images:

- [ ] Resolution appropriate for use case
- [ ] No visible artifacts or distortions
- [ ] Text renders correctly (if applicable)
- [ ] Composition matches requirements
- [ ] Style consistent with brand
- [ ] No copyright/trademark issues
- [ ] Suitable for target audience

---

*Part of Faion Network Marketing Manager Skill*
*Last Updated: 2026-01-23*


## Sources

- [AI Workflow Automation](https://www.zapier.com/blog/ai-automation/)
- [ComfyUI Workflows](https://github.com/comfyanonymous/ComfyUI)
- [Photoshop Generative Fill](https://www.adobe.com/products/photoshop/generative-fill.html)
- [Bannerbear Automation](https://www.bannerbear.com/blog/)
- [Design Automation Best Practices](https://www.canva.com/design/)
