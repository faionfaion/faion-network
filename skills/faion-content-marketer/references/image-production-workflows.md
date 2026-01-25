# Image Production Workflows

**Production pipelines, batch generation, A/B testing (2025-2026)**

---

## Model Comparison

### Quick Reference

| Model | Best For | Text in Images | Control Level | API | Cost |
|-------|----------|----------------|---------------|-----|------|
| **DALL-E 3** | Text rendering, commercial | Excellent | Medium | OpenAI | $0.04-0.12/image |
| **Midjourney v6.1** | Artistic, aesthetic | Good | Medium | Discord/API | $10-60/month |
| **FLUX.1 Pro** | Photorealism | Good | High | Replicate/fal.ai | $0.03-0.05/image |
| **SD 3.5 Large** | Maximum control, local | Moderate | Excellent | Self-hosted | Free (GPU costs) |
| **Ideogram 2.0** | Text in images, logos | Excellent | Medium | API | $0.02-0.08/image |

### When to Use Each

| Use Case | Recommended Model |
|----------|-------------------|
| Text/typography in images | DALL-E 3, Ideogram 2 |
| Photorealistic portraits | FLUX.1 Pro |
| Artistic/stylized images | Midjourney v6.1 |
| Product photography | FLUX.1 Pro, DALL-E 3 |
| Maximum control/customization | Stable Diffusion 3.5 |
| Logo design | Ideogram 2, DALL-E 3 |
| Consistent characters | Midjourney (--cref), SD + LoRA |
| Quick iterations | FLUX.1 Schnell |
| Budget-conscious | SD 3.5 (self-hosted), Ideogram |

---

## Asset Generation Pipeline

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

---

## Batch Generation

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

---

## A/B Testing Images

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

## Cost Comparison

### Per-Image Cost

| Model | Low Quality | Standard | High Quality |
|-------|-------------|----------|--------------|
| **DALL-E 3** | $0.040 | $0.040 | $0.080-0.120 |
| **DALL-E 2** | $0.016 | $0.018 | $0.020 |
| **Midjourney** | ~$0.02* | ~$0.02* | ~$0.02* |
| **FLUX Pro** | - | $0.03-0.05 | - |
| **FLUX Schnell** | $0.003 | - | - |
| **Ideogram** | $0.02 | $0.04 | $0.08 |
| **SD 3.5** | Free** | Free** | Free** |

*Midjourney based on subscription divided by fast hours
**Self-hosted, only GPU/compute costs

### Monthly Cost Scenarios

| Use Case | Volume | Recommended | Est. Monthly Cost |
|----------|--------|-------------|-------------------|
| **Hobbyist** | ~100/month | FLUX Schnell, Free tiers | $0-10 |
| **Content Creator** | ~500/month | Midjourney Standard, FLUX | $30-50 |
| **Agency** | ~2000/month | Mix of services | $100-200 |
| **Enterprise** | ~10000/month | SD self-hosted + APIs | $200-500 |

### Cost Optimization Tips

1. **Prototype with cheap models** - Use FLUX Schnell or Ideogram free tier
2. **Batch similar requests** - Reduce API overhead
3. **Self-host for volume** - SD 3.5 is free (compute only)
4. **Use appropriate quality** - Standard often sufficient
5. **Cache results** - Don't regenerate identical prompts
6. **Choose right model** - Text in images? Use DALL-E/Ideogram, not FLUX

---

## Quality Checklist

Before using generated images:

- [ ] Resolution appropriate for use case
- [ ] No visible artifacts or distortions
- [ ] Text renders correctly (if applicable)
- [ ] Composition matches requirements
- [ ] Style consistent with brand
- [ ] No copyright/trademark issues
- [ ] Suitable for target audience

---

## Ethical Considerations

### Content Guidelines

1. **Consent** - Don't generate images of real people without permission
2. **Deepfakes** - Avoid creating misleading content
3. **Copyright** - Don't replicate copyrighted characters/art
4. **NSFW** - Follow platform content policies
5. **Attribution** - Credit AI generation when required

### Safety Filters

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

| Issue | Cause | Solution |
|-------|-------|----------|
| Blurry output | Low resolution, wrong model | Use HD quality, larger size |
| Wrong subject | Ambiguous prompt | Be more specific, use negative prompts |
| Distorted faces | Model limitation | Use portrait-specific models |
| Wrong text | Model weakness | Use DALL-E 3 or Ideogram |
| Inconsistent style | Prompt drift | Use style references, seed values |
| API timeout | Long generation | Increase timeout, use async |
| Rate limited | Too many requests | Implement backoff, queue requests |


## Sources

- [Creative Production Workflows](https://www.adobe.com/creativecloud/business.html)
- [Design Systems Guide](https://www.designsystems.com/)
- [Brand Asset Management](https://brandfolder.com/resources/)
- [Creative Operations Blog](https://www.workfront.com/blog)
- [Figma Best Practices](https://www.figma.com/best-practices/)
