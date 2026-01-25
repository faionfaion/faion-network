# Image Editing Workflows

**Image-to-image, inpainting, outpainting, upscaling (2025-2026)**

---

## Image-to-Image (Style Transfer)

Transform existing images while preserving structure.

### FLUX Redux

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/flux-pro/v1.1/redux",
    arguments={
        "image_url": "https://example.com/photo.jpg",
        "prompt": "Same scene in impressionist painting style, vibrant colors",
        "strength": 0.6  # 0.3-0.8 typical range
    }
)
```

### Stable Diffusion img2img

```python
from diffusers import StableDiffusion3Img2ImgPipeline
from diffusers.utils import load_image
import torch

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

---

## Inpainting (Edit Regions)

Edit specific parts of an image while keeping the rest.

### DALL-E 2 Inpainting

```python
from openai import OpenAI
client = OpenAI()

response = client.images.edit(
    model="dall-e-2",
    image=open("scene.png", "rb"),
    mask=open("mask.png", "rb"),  # White = keep, Transparent = edit
    prompt="A golden retriever sitting on the grass",
    size="1024x1024"
)
```

### Stable Diffusion Inpainting

```python
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

### Creating Masks with Segment Anything

```python
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

---

## Outpainting (Expand Canvas)

```python
from PIL import Image
from openai import OpenAI

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
client = OpenAI()
response = client.images.edit(
    model="dall-e-2",
    image=open("expanded.png", "rb"),
    mask=open("outpaint_mask.png", "rb"),
    prompt="continuation of the landscape scene, same style",
    size="1024x1024"
)
```

---

## Upscaling

### Real-ESRGAN

```python
import replicate

output = replicate.run(
    "nightmareai/real-esrgan:350d32041630ffbe63c8352783a26d94126809164e54085352f8571e3d4edd3b",
    input={
        "image": open("low_res.png", "rb"),
        "scale": 4,  # 2x or 4x
        "face_enhance": True
    }
)
```

### FLUX Creative Upscaling

```python
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

---

## Background Removal

### remove.bg API

```python
import requests

response = requests.post(
    "https://api.remove.bg/v1.0/removebg",
    files={"image_file": open("photo.png", "rb")},
    data={"size": "auto"},
    headers={"X-Api-Key": "YOUR_API_KEY"}
)

with open("no_bg.png", "wb") as f:
    f.write(response.content)
```

### Replicate

```python
output = replicate.run(
    "lucataco/remove-bg:95fcc2a26d3899cd6c2691c900465aaeff466285a65c14638cc5f36f34befaf1",
    input={"image": open("photo.png", "rb")}
)
```
