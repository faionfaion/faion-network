# Ideogram 2.0 Image Generation

**Complete guide to Ideogram 2.0 (2025-2026)**

---

## Overview

Specialized for text rendering in images. Excellent for logos, posters, and graphics with text.

**Key Strengths:**
- Best-in-class text rendering
- Good for logos and branding
- Clean, commercial-ready output

---

## API Usage

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

---

## Parameters

| Parameter | Options | Description |
|-----------|---------|-------------|
| `model` | `V_2`, `V_2_TURBO` | Model version |
| `aspect_ratio` | `ASPECT_1_1`, `ASPECT_16_9`, `ASPECT_9_16`, etc. | Output ratio |
| `style_type` | `GENERAL`, `REALISTIC`, `DESIGN`, `RENDER_3D`, `ANIME` | Style preset |
| `magic_prompt_option` | `AUTO`, `ON`, `OFF` | Prompt enhancement |
| `seed` | Integer | Reproducibility |
| `negative_prompt` | String | What to avoid |

---

## Style Types

| Style | Best For |
|-------|----------|
| `GENERAL` | Mixed content |
| `REALISTIC` | Photos, product shots |
| `DESIGN` | Logos, graphics, flat design |
| `RENDER_3D` | 3D renders, product visualization |
| `ANIME` | Anime/manga style |

---

## Pricing

| Plan | Images/Month | Cost |
|------|--------------|------|
| Free | 100 | $0 |
| Basic | 400 | $7/month |
| Plus | 1000 | $16/month |
| Pro | 3000 | $48/month |

API pricing: ~$0.02-0.08 per image depending on model and resolution.

---

## References

- [Ideogram Documentation](https://ideogram.ai/docs)
