# M-GEN-001: Image Prompting

## Overview

Image prompting is the art of crafting effective prompts for text-to-image models like DALL-E, Midjourney, Stable Diffusion, and FLUX. Good prompts consistently produce high-quality, relevant images while bad prompts yield unpredictable results.

**When to use:** Generating images for products, marketing, documentation, or creative projects.

## Core Concepts

### 1. Model Comparison (2025)

| Model | Strengths | Weaknesses | Best For |
|-------|-----------|------------|----------|
| **DALL-E 3** | Text rendering, coherence | Less artistic | Product, marketing |
| **Midjourney v6** | Artistic quality, aesthetics | No API (Discord only) | Creative, artistic |
| **FLUX.1 Pro** | Photorealism, fast | Newer model | Photorealistic |
| **Stable Diffusion 3** | Customizable, open | Requires setup | Custom workflows |
| **Ideogram 2.0** | Text rendering | Limited styles | Text-heavy images |

### 2. Prompt Anatomy

```
[Subject] + [Style] + [Medium] + [Lighting] + [Composition] + [Details] + [Quality modifiers]
```

**Example:**
```
A professional headshot of a friendly business woman,
corporate photography style, soft studio lighting,
centered composition, wearing a navy blue blazer,
neutral gray background, high resolution, 8K
```

### 3. Key Prompt Components

| Component | Purpose | Examples |
|-----------|---------|----------|
| **Subject** | What to generate | "a golden retriever", "a modern office" |
| **Style** | Artistic approach | "watercolor", "photorealistic", "flat design" |
| **Medium** | Artistic medium | "oil painting", "3D render", "photograph" |
| **Lighting** | Light quality | "soft lighting", "dramatic shadows", "golden hour" |
| **Composition** | Layout | "centered", "rule of thirds", "wide angle" |
| **Quality** | Output quality | "high detail", "8K", "professional" |

## Best Practices

### 1. Be Specific and Descriptive

```markdown
# Bad - Vague
"A dog"

# Good - Specific
"A golden retriever puppy sitting in a sunlit meadow,
looking at the camera with tongue out, soft focus background
with wildflowers, warm afternoon lighting, professional pet photography"
```

### 2. Use Style References

```markdown
# Photography styles
"35mm film photography", "macro photography", "long exposure"
"portrait photography", "product photography"

# Art styles
"in the style of Studio Ghibli", "impressionist oil painting"
"minimalist vector illustration", "Art Deco poster design"

# Design styles
"flat design icon", "isometric illustration", "material design"
"brutalist architecture", "mid-century modern"
```

### 3. Control Composition

```markdown
# Framing
"close-up shot", "medium shot", "wide establishing shot"
"overhead view", "worm's eye view", "straight-on angle"

# Layout
"centered composition", "rule of thirds", "symmetrical"
"negative space on left", "subject on right side"

# Depth
"shallow depth of field", "bokeh background"
"deep focus", "tilt-shift effect"
```

## Common Patterns

### Pattern 1: Product Photography

```python
def product_image_prompt(
    product: str,
    background: str = "clean white",
    angle: str = "hero angle",
    lighting: str = "soft studio"
) -> str:
    return f"""
    Professional product photography of {product},
    {angle} view, {background} background,
    {lighting} lighting, high-end commercial photography,
    sharp focus, no shadows, minimalist aesthetic,
    8K resolution, professional catalog style
    """

# Example
prompt = product_image_prompt(
    product="a sleek wireless headphone in matte black",
    background="gradient gray to white",
    angle="three-quarter"
)
```

### Pattern 2: Social Media Graphics

```python
def social_media_prompt(
    concept: str,
    platform: str = "instagram",
    style: str = "modern minimal"
) -> str:
    aspect_ratios = {
        "instagram": "square composition 1:1",
        "twitter": "16:9 landscape",
        "pinterest": "2:3 vertical",
        "linkedin": "1.91:1 landscape"
    }

    return f"""
    {concept}, {style} graphic design,
    {aspect_ratios.get(platform, 'square')},
    vibrant colors, clean typography space,
    social media ready, eye-catching,
    professional graphic design, trending on Dribbble
    """
```

### Pattern 3: Consistent Character Design

```python
def character_prompt(
    character_desc: str,
    action: str,
    setting: str,
    style: str = "Pixar 3D animation"
) -> str:
    return f"""
    {character_desc}, {action}, in {setting},
    {style} style, expressive face, dynamic pose,
    consistent character design, appealing proportions,
    warm color palette, soft ambient lighting,
    high quality 3D render, 8K
    """

# Use same character description for consistency
character = "a young fox with orange fur and big green eyes wearing a blue scarf"
prompt1 = character_prompt(character, "running through", "an autumn forest")
prompt2 = character_prompt(character, "reading a book in", "a cozy library")
```

### Pattern 4: DALL-E 3 with OpenAI API

```python
from openai import OpenAI

client = OpenAI()

def generate_image(prompt: str, size: str = "1024x1024", quality: str = "hd") -> str:
    """Generate image with DALL-E 3."""

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,  # "1024x1024", "1792x1024", "1024x1792"
        quality=quality,  # "standard" or "hd"
        n=1
    )

    return response.data[0].url

# Usage
prompt = """
    A modern home office with a standing desk,
    large window with natural light, plants,
    minimalist Scandinavian design, warm wood tones,
    architectural photography, soft afternoon light,
    clean and organized, 8K resolution
"""

image_url = generate_image(prompt, size="1792x1024", quality="hd")
```

### Pattern 5: Negative Prompts (Stable Diffusion)

```python
def generate_with_negative(
    positive_prompt: str,
    negative_prompt: str = None,
    model: str = "stable-diffusion-xl"
) -> str:
    """Generate with both positive and negative prompts."""

    default_negative = """
    blurry, low quality, distorted, deformed,
    ugly, bad anatomy, extra limbs, watermark,
    text, logo, signature, cropped, out of frame
    """

    negative = negative_prompt or default_negative

    # API call depends on provider
    response = sd_client.generate(
        prompt=positive_prompt,
        negative_prompt=negative,
        model=model,
        steps=30,
        cfg_scale=7
    )

    return response.image_url

# Example
prompt = "Professional headshot of a business executive"
negative = "cartoon, anime, illustration, distorted face, multiple people"
```

## Style Reference Guide

### Photography Styles
| Style | Keywords | Use Case |
|-------|----------|----------|
| Portrait | "85mm lens, shallow DOF, studio" | Headshots |
| Product | "white background, soft shadows" | E-commerce |
| Landscape | "wide angle, golden hour" | Nature, travel |
| Street | "candid, natural light, 35mm" | Lifestyle |
| Food | "overhead, props, rustic" | Restaurant, recipe |

### Illustration Styles
| Style | Keywords | Use Case |
|-------|----------|----------|
| Flat Design | "flat illustration, vector, minimal" | UI, icons |
| Isometric | "isometric view, 3D illustration" | Infographics |
| Watercolor | "watercolor painting, soft edges" | Artistic |
| Line Art | "line drawing, sketch, ink" | Technical |
| Cartoon | "cartoon style, vibrant colors" | Children, fun |

### 3D Render Styles
| Style | Keywords | Use Case |
|-------|----------|----------|
| Realistic | "photorealistic 3D render, Octane" | Products |
| Stylized | "Pixar style, Cinema 4D" | Animation |
| Architectural | "architectural visualization" | Real estate |
| Abstract | "3D abstract shapes, gradients" | Creative |

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Too vague | Random results | Add specific details |
| Contradictory | Confused output | Keep style consistent |
| Too long | Model ignores parts | Prioritize key elements |
| No style mention | Generic look | Specify artistic style |
| Requesting text | Often illegible | Use Ideogram or DALL-E 3 |

## Tools & References

### Related Skills
- faion-image-gen-skill
- faion-openai-api-skill

### Related Agents
- faion-image-generator-agent
- faion-image-editor-agent

### External Resources
- [DALL-E 3 Prompting](https://platform.openai.com/docs/guides/images)
- [Midjourney Documentation](https://docs.midjourney.com/)
- [Stable Diffusion Prompt Guide](https://stability.ai/blog/stable-diffusion-prompt-guide)
- [Lexica.art](https://lexica.art/) - Prompt inspiration

## Checklist

- [ ] Identified target style/aesthetic
- [ ] Included subject description
- [ ] Specified artistic style/medium
- [ ] Added lighting description
- [ ] Described composition
- [ ] Included quality modifiers
- [ ] Added negative prompts (if supported)
- [ ] Selected appropriate model
- [ ] Tested with variations
- [ ] Documented successful prompts

---

*Methodology: M-GEN-001 | Category: Multimodal/Generation*
*Related: faion-image-generator-agent, faion-image-gen-skill*
