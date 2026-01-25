# AI Video Platforms

**Sora 2, Runway Gen-4, Pika Labs, Kling - Platform Comparison and Integration**

---

## Quick Reference

| Platform | Best For | Max Duration | API | Cost Range |
|----------|----------|--------------|-----|------------|
| **Sora 2** | Photorealism, complex motion | 20s (Plus), 60s (Pro) | OpenAI | $20-200/mo subscription |
| **Runway Gen-4** | Professional, consistent | 10s | Yes | $0.05-0.10/second |
| **Pika Labs 2.5** | Speed, effects | 5s (extendable) | Yes | $0.20-0.50/video |
| **Kling 2.0** | Alternative, good value | 10s | Limited | Freemium |
| **Luma Dream Machine** | Fast iteration | 5s | Yes | Credits-based |

---

## Platform Comparison

### Feature Matrix

| Feature | Sora 2 | Runway Gen-4 | Pika 2.5 | Kling 2.0 |
|---------|--------|--------------|----------|-----------|
| Text-to-Video | Yes | Yes | Yes | Yes |
| Image-to-Video | Yes | Yes | Yes | Yes |
| Video-to-Video | Yes | Yes | Partial | No |
| Camera Controls | Advanced | Advanced | Basic | Basic |
| Motion Brush | Yes | Yes | No | No |
| Lip Sync | Yes | No | Yes | Yes |
| Audio Generation | Yes | No | Yes (SFX) | No |
| Storyboard Mode | Yes | Multi-shot | No | No |
| Resolution | 1080p | 4K | 1080p | 1080p |
| API Access | OpenAI | Yes | Yes | Limited |

### When to Use Each

| Use Case | Recommended Platform |
|----------|---------------------|
| Cinematic quality, complex scenes | Sora 2 |
| Professional production, API integration | Runway Gen-4 |
| Quick iterations, social content | Pika Labs 2.5 |
| Budget-conscious, testing | Kling 2.0 |
| Rapid prototyping | Luma Dream Machine |

---

## Sora 2 (OpenAI)

### Overview

OpenAI's flagship video generation model. Best for photorealistic output and complex scene understanding.

**Access:** ChatGPT Plus ($20/mo) or Pro ($200/mo)

### Capabilities

| Feature | Description |
|---------|-------------|
| **Text-to-Video** | Generate from detailed prompts |
| **Image-to-Video** | Animate static images |
| **Video-to-Video** | Remix, edit, extend existing videos |
| **Blend Mode** | Combine two video sources |
| **Re-cut** | Edit and re-render existing videos |
| **Storyboard** | Multi-shot timeline planning |

### Prompt Engineering

**Effective Prompt Structure:**

```
[Scene Description] + [Camera Movement] + [Lighting] + [Style] + [Duration Hint]
```

**Example Prompts:**

```
# Cinematic Scene
A woman with dark skin and wavy hair walks through a neon-lit Tokyo alley
at night. Camera follows from behind, tracking shot. Cyberpunk aesthetic,
moody lighting with pink and blue neon reflections on wet pavement.

# Product Shot
A sleek smartphone rotates slowly on a white marble surface. Camera orbits
around the device. Studio lighting with soft shadows, minimalist aesthetic,
commercial quality.

# Nature Documentary
A monarch butterfly emerging from its chrysalis in extreme close-up.
Time-lapse style, macro photography, natural morning light filtering
through leaves.
```

### Best Practices

1. **Be specific about movement** - Describe camera and subject motion explicitly
2. **Specify lighting** - "Golden hour", "studio lighting", "neon", etc.
3. **Reference styles** - "cinematic", "documentary", "commercial", "music video"
4. **Duration awareness** - Shorter prompts = faster, more coherent output
5. **Iterate** - Use re-cut and blend for refinement

### Limitations

- Max 20 seconds (Plus), 60 seconds (Pro)
- Text rendering still imperfect
- Human hands/fingers can have artifacts
- No direct API (use ChatGPT interface or Sora interface)
- Limited exports per month based on subscription

---

## Runway Gen-3 / Gen-4

### Overview

Industry-standard for professional video production. Best API support and control options.

**Pricing:**
- Standard: $0.05/second generated
- Turbo: $0.02/second (lower quality, faster)
- Unlimited plan: $96/month

### Gen-4 Features

| Feature | Description |
|---------|-------------|
| **Extended Duration** | Up to 40 seconds per generation |
| **Multi-Shot** | Plan and generate connected shots |
| **Camera Controls** | Pan, tilt, zoom, dolly, orbit |
| **Motion Brush** | Paint motion onto specific areas |
| **Structure Reference** | Maintain subject consistency |

### API Integration

```python
# Runway Gen-4 Python SDK
import runwayml

client = runwayml.RunwayML()

# Text-to-Video
text_task = client.text_to_video.create(
    model="gen4",
    prompt="A serene lake at sunrise, mist rising from the water, camera slowly pushes forward",
    duration=10,
    aspect_ratio="16:9",
    resolution="1080p"
)

# Poll for completion
import time
while text_task.status not in ["SUCCEEDED", "FAILED"]:
    text_task = client.tasks.retrieve(text_task.id)
    print(f"Status: {text_task.status}")
    time.sleep(5)

if text_task.status == "SUCCEEDED":
    video_url = text_task.output[0]
    print(f"Video ready: {video_url}")

# Image-to-Video
with open("scene.png", "rb") as f:
    image_data = f.read()

image_task = client.image_to_video.create(
    model="gen4",
    prompt_image=image_data,
    prompt_text="Camera slowly pans right, birds fly across the sky",
    duration=10,
    aspect_ratio="16:9"
)

# With Camera Controls
controlled_task = client.image_to_video.create(
    model="gen4",
    prompt_image=image_data,
    prompt_text="Gentle wind moves the grass",
    camera_motion={
        "horizontal": 0.3,   # Pan right
        "vertical": 0.0,     # No tilt
        "zoom": 0.1,         # Slight zoom in
        "roll": 0.0          # No roll
    },
    duration=10
)
```

### Camera Motion Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `horizontal` | -1.0 to 1.0 | Pan left/right |
| `vertical` | -1.0 to 1.0 | Tilt up/down |
| `zoom` | -1.0 to 1.0 | Zoom out/in |
| `roll` | -1.0 to 1.0 | Rotate camera |

### Motion Brush Workflow

1. Upload source image
2. Paint mask over areas to animate
3. Describe motion for masked areas
4. Generate with motion applied only to selection

---

## Pika Labs 2.5

### Overview

Fast, cost-effective video generation with unique features like lip sync and sound effects.

**Pricing:**
- Free tier: 250 credits/month
- Pro: $8/month - 700 credits
- Unlimited: $28/month

### Key Features

| Feature | Description |
|---------|-------------|
| **Lip Sync** | Sync character lips to audio |
| **Sound Effects** | AI-generated SFX matching video |
| **Modify Region** | Edit specific parts of video |
| **Expand Canvas** | Outpaint video frames |
| **Pikaffects** | Special effects library |

### API Integration

```python
import requests
import time

PIKA_API_KEY = "your-api-key"
PIKA_BASE_URL = "https://api.pika.art/v1"

headers = {
    "Authorization": f"Bearer {PIKA_API_KEY}",
    "Content-Type": "application/json"
}

# Text-to-Video
response = requests.post(
    f"{PIKA_BASE_URL}/generate",
    headers=headers,
    json={
        "prompt": "A cat playing piano in a jazz club, cinematic lighting",
        "aspect_ratio": "16:9",
        "motion_strength": 3,  # 1-5 scale
        "guidance_scale": 12,
        "negative_prompt": "blurry, distorted, low quality"
    }
)

task_id = response.json()["task_id"]

# Poll for result
while True:
    status_response = requests.get(
        f"{PIKA_BASE_URL}/tasks/{task_id}",
        headers=headers
    )
    status = status_response.json()

    if status["status"] == "completed":
        video_url = status["output"]["video_url"]
        break
    elif status["status"] == "failed":
        raise Exception(f"Generation failed: {status['error']}")

    time.sleep(3)

# Image-to-Video with motion
with open("image.png", "rb") as f:
    files = {"image": f}
    data = {
        "prompt": "The character turns and smiles",
        "motion_strength": 2,
        "fps": 24
    }
    response = requests.post(
        f"{PIKA_BASE_URL}/image-to-video",
        headers={"Authorization": f"Bearer {PIKA_API_KEY}"},
        files=files,
        data=data
    )
```

### Pikaffects (Special Effects)

| Effect | Description |
|--------|-------------|
| Melt | Object melts into liquid |
| Explode | Particle explosion |
| Inflate | Object inflates like balloon |
| Crush | Object gets crushed |
| Cake-ify | Transform into cake |
| Squish | Squeeze and release |

---

## Kling 2.0

### Overview

Chinese-developed alternative with competitive quality and pricing. Good for budget-conscious projects.

**Access:** Web interface, limited API

### Features

| Feature | Description |
|---------|-------------|
| **Motion Templates** | Pre-built motion patterns |
| **Style Transfer** | Apply artistic styles |
| **Character Animation** | Consistent character motion |
| **Inpainting** | Edit specific regions |

### Best For

- Testing and prototyping
- Budget-conscious production
- Simple animations
- Social media content

### Limitations

- API access requires application
- Documentation primarily in Chinese
- Some features geo-restricted
- Processing queue can be slow

---

*Part of faion-marketing-manager skill*
*Reference: ai-video-platforms.md*
