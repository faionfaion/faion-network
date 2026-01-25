# DALL-E Image Generation

**Complete guide to DALL-E 3 and DALL-E 2 image generation (2025-2026)**

---

## Overview

OpenAI's flagship image generation model. Best-in-class for text rendering and commercial-safe content.

**Key Strengths:**
- Excellent text rendering in images
- Strong prompt following
- Built-in safety filters
- Automatic prompt enhancement (revised_prompt)

---

## DALL-E 3

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

---

## DALL-E 2

### Image Editing (Inpainting)

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
```

### Variations

```python
# Variations - create similar images
response = client.images.create_variation(
    model="dall-e-2",
    image=open("source.png", "rb"),
    size="1024x1024",
    n=3
)
```

---

## Pricing (2025-2026)

| Model | Quality | Size | Price per Image |
|-------|---------|------|-----------------|
| **DALL-E 3** | HD | 1024x1024 | $0.080 |
| **DALL-E 3** | HD | 1792x1024, 1024x1792 | $0.120 |
| **DALL-E 3** | Standard | 1024x1024 | $0.040 |
| **DALL-E 3** | Standard | 1792x1024, 1024x1792 | $0.080 |
| **DALL-E 2** | - | 1024x1024 | $0.020 |
| **DALL-E 2** | - | 512x512 | $0.018 |
| **DALL-E 2** | - | 256x256 | $0.016 |

---

## Best Practices

1. **Be specific** - More detail = better results
2. **Use revised_prompt** - Check what DALL-E actually generated
3. **Natural style for realism** - Use `style: "natural"` for photos
4. **HD for detail** - Worth the extra cost for final assets
5. **Download immediately** - URLs expire in 1 hour

---

## Model-Specific Tips

**DALL-E 3:**
- Natural language works best
- System adds detail automatically
- Check `revised_prompt` to understand changes
- Use "natural" style for realism

**DALL-E 2:**
- Good for editing and variations
- Lower cost for iterations
- Supports multiple images per request (n=1-10)

---

## References

- [OpenAI DALL-E Documentation](https://platform.openai.com/docs/guides/images)


## Sources

- [OpenAI DALL-E Documentation](https://platform.openai.com/docs/guides/images)
- [DALL-E Prompt Engineering](https://dallery.gallery/dall-e-ai-guide-faq/)
- [OpenAI Research Blog](https://openai.com/research/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [AI Art Weekly Newsletter](https://aiartweekly.com/)
