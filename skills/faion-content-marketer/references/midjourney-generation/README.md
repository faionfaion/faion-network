# Midjourney Image Generation

**Complete guide to Midjourney v6.1 image generation (2025-2026)**

---

## Overview

Industry-leading aesthetic quality. Best for artistic, stylized images. Recently launched official API.

**Key Strengths:**
- Exceptional aesthetic quality
- Strong community and style ecosystem
- Character reference (--cref) for consistency
- Style reference (--sref) for consistent aesthetics

---

## API Access

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

---

## Discord Bot Usage

For those without API access:

```
/imagine prompt: portrait of a scientist, dramatic lighting, oil painting style --ar 3:4 --v 6.1

Buttons:
U1-U4: Upscale individual images
V1-V4: Create variations
Re-roll: Generate new images
```

---

## Parameters

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

---

## Character Consistency (--cref)

```
/imagine portrait of a woman with red hair, business attire --cref https://example.com/character.jpg --cw 100

--cw values:
0: Only face
50: Face + some style
100: Full character reference
```

---

## Style Reference (--sref)

```
/imagine mountain landscape at sunset --sref https://example.com/style.jpg --sw 500

--sw values:
0-100: Subtle influence
100-500: Moderate influence
500-1000: Strong influence
```

---

## Pricing

| Plan | Monthly Cost | Fast Hours | Relax Mode |
|------|-------------|------------|------------|
| Basic | $10 | 3.3 hours | No |
| Standard | $30 | 15 hours | Yes |
| Pro | $60 | 30 hours | Yes |
| Mega | $120 | 60 hours | Yes |

---

## Model-Specific Tips

**Midjourney:**
- Use `--style raw` for less stylization
- Stack style references with `--sref`
- Lower `--stylize` for more prompt adherence
- Separate concepts with `::`

---

## References

- [Midjourney Documentation](https://docs.midjourney.com)


## Sources

- [Midjourney Documentation](https://docs.midjourney.com/)
- [Midjourney Prompt Guide](https://docs.midjourney.com/docs/prompts)
- [Midjourney Community](https://www.midjourney.com/showcase)
- [Prompt Hero Midjourney](https://prompthero.com/midjourney-prompts)
- [Midjourney Styles Reference](https://github.com/willwulfken/MidJourney-Styles-and-Keywords-Reference)
