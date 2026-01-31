---
id: img-gen-basics
name: "Image Generation Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: image-generation
---

# Image Generation Basics

Core patterns for AI image generation using DALL-E 3, Midjourney, and Stable Diffusion.

## DALL-E 3 Implementation

```python
from openai import OpenAI
import requests

client = OpenAI()

def generate_image(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "standard",
    style: str = "vivid"
) -> dict:
    """
    Generate image with DALL-E 3.

    size: "1024x1024", "1792x1024", "1024x1792"
    quality: "standard", "hd"
    style: "vivid", "natural"
    """
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality=quality,
        style=style,
        n=1
    )

    return {
        "url": response.data[0].url,
        "revised_prompt": response.data[0].revised_prompt
    }

def generate_and_save(prompt: str, output_path: str, **kwargs) -> str:
    """Generate image and save to file."""
    result = generate_image(prompt, **kwargs)

    response = requests.get(result["url"])
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
```

### DALL-E 2 Features

```python
def generate_variations(image_path: str, n: int = 3) -> list:
    """Generate variations of an existing image (DALL-E 2 only)."""
    with open(image_path, "rb") as f:
        response = client.images.create_variation(
            image=f,
            n=n,
            size="1024x1024",
            model="dall-e-2"
        )

    return [img.url for img in response.data]

def edit_image(image_path: str, mask_path: str, prompt: str) -> str:
    """Edit image with mask (DALL-E 2 only)."""
    with open(image_path, "rb") as img, open(mask_path, "rb") as mask:
        response = client.images.edit(
            image=img,
            mask=mask,
            prompt=prompt,
            n=1,
            size="1024x1024",
            model="dall-e-2"
        )

    return response.data[0].url
```

## Prompt Engineering

```python
class ImagePromptBuilder:
    """Build effective image generation prompts."""

    def __init__(self):
        self.components = {
            "subject": "",
            "style": "",
            "lighting": "",
            "composition": "",
            "details": [],
            "mood": "",
            "technical": []
        }

    def set_subject(self, subject: str):
        self.components["subject"] = subject
        return self

    def set_style(self, style: str):
        styles = {
            "photorealistic": "photorealistic, highly detailed photograph",
            "digital_art": "digital art, vibrant colors",
            "oil_painting": "oil painting, textured brushstrokes",
            "watercolor": "watercolor painting, soft edges, fluid",
            "anime": "anime style, cel shading",
            "3d_render": "3D render, octane render, highly detailed",
            "sketch": "pencil sketch, hand-drawn",
            "minimalist": "minimalist, clean lines, simple"
        }
        self.components["style"] = styles.get(style, style)
        return self

    def set_lighting(self, lighting: str):
        lighting_options = {
            "golden_hour": "golden hour lighting, warm tones",
            "studio": "professional studio lighting",
            "dramatic": "dramatic lighting, high contrast",
            "soft": "soft diffused lighting",
            "neon": "neon lighting, cyberpunk atmosphere",
            "natural": "natural daylight"
        }
        self.components["lighting"] = lighting_options.get(lighting, lighting)
        return self

    def set_composition(self, composition: str):
        self.components["composition"] = composition
        return self

    def add_detail(self, detail: str):
        self.components["details"].append(detail)
        return self

    def set_mood(self, mood: str):
        self.components["mood"] = mood
        return self

    def add_technical(self, spec: str):
        specs = {
            "4k": "4K resolution, ultra detailed",
            "8k": "8K resolution, extremely detailed",
            "depth_of_field": "shallow depth of field, bokeh",
            "wide_angle": "wide angle lens",
            "macro": "macro photography, extreme detail",
            "cinematic": "cinematic composition, film grain"
        }
        self.components["technical"].append(specs.get(spec, spec))
        return self

    def build(self) -> str:
        """Build the final prompt."""
        parts = []

        if self.components["subject"]:
            parts.append(self.components["subject"])
        if self.components["style"]:
            parts.append(self.components["style"])
        if self.components["lighting"]:
            parts.append(self.components["lighting"])
        if self.components["composition"]:
            parts.append(self.components["composition"])
        if self.components["mood"]:
            parts.append(f"{self.components['mood']} mood")

        parts.extend(self.components["details"])
        parts.extend(self.components["technical"])

        return ", ".join(parts)

# Usage
prompt = (
    ImagePromptBuilder()
    .set_subject("a futuristic city skyline at sunset")
    .set_style("digital_art")
    .set_lighting("golden_hour")
    .set_mood("hopeful")
    .add_detail("flying cars")
    .add_detail("glass buildings")
    .add_technical("8k")
    .add_technical("cinematic")
    .build()
)
```

## Image-to-Image with Vision

```python
import base64

def describe_image(image_path: str) -> str:
    """Describe image using GPT-4 Vision."""
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image in detail for image generation."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content

def reimagine_image(image_path: str, style_modifier: str = "", **kwargs) -> dict:
    """Create new image inspired by existing one."""
    description = describe_image(image_path)
    prompt = f"{description}. {style_modifier}" if style_modifier else description
    return generate_image(prompt, **kwargs)
```

## Batch Generation

```python
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

class BatchImageGenerator:
    """Generate multiple images efficiently."""

    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.client = OpenAI()

    def generate_batch(self, prompts: List[str], **kwargs) -> List[Dict]:
        """Generate images for multiple prompts."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            futures = []

            for prompt in prompts:
                future = executor.submit(self._generate_single, prompt, **kwargs)
                futures.append((prompt, future))

            for prompt, future in futures:
                try:
                    result = future.result()
                    results.append({
                        "prompt": prompt,
                        "success": True,
                        "url": result["url"],
                        "revised_prompt": result["revised_prompt"]
                    })
                except Exception as e:
                    results.append({
                        "prompt": prompt,
                        "success": False,
                        "error": str(e)
                    })

        return results

    def _generate_single(self, prompt: str, **kwargs) -> dict:
        """Generate single image."""
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            **kwargs
        )
        return {
            "url": response.data[0].url,
            "revised_prompt": response.data[0].revised_prompt
        }

    def generate_grid(self, base_prompt: str, variations: List[str], **kwargs) -> List[Dict]:
        """Generate grid of variations."""
        prompts = [f"{base_prompt}, {variation}" for variation in variations]
        return self.generate_batch(prompts, **kwargs)
```

## Best Practices

1. **Prompt Quality** - Be specific with style, lighting, composition, technical specs
2. **Cost Management** - Cache images, use appropriate quality, batch similar requests
3. **Content Safety** - Review policies, implement filtering, handle rejections gracefully
4. **Quality Control** - Review outputs, iterate prompts, use variations for options

## Common Pitfalls

- Vague prompts → unclear results
- Ignoring revised prompts → missing context
- Wrong aspect ratio → poor fit
- Content violations → rejections
- Overcomplication → conflicting details

## Sources

- [DALL-E 3 API Documentation](https://platform.openai.com/docs/guides/images)
- [DALL-E 3 Prompt Guide](https://platform.openai.com/docs/guides/images/prompting)
- [OpenAI Image Generation Best Practices](https://help.openai.com/en/articles/6654000-best-practices-for-dall-e)
- [DALL-E Pricing](https://openai.com/api/pricing/)
