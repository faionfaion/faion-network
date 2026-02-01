# Image Generation

AI image generation from text descriptions using DALL-E 3, Stable Diffusion, Flux, and other models.

## Overview

| Service | Quality | Best For | API | Pricing (2025) |
|---------|---------|----------|-----|----------------|
| DALL-E 3 | High | General purpose, text in images | OpenAI | $0.04-0.12/image |
| GPT-4o | Very High | Multimodal, precise prompts | OpenAI | Usage-based |
| Stable Diffusion XL | High | Customization, local | Replicate/Self-hosted | Free/Variable |
| Stable Diffusion 3.5 | Very High | Professional, enterprise | Stability AI/AWS Bedrock | Enterprise |
| Flux.1/2 | Very High | Photorealistic, fast | Black Forest Labs | $0.014+/image |
| Midjourney | Excellent | Artistic, creative | Discord/API | $10-60/month |

## When to Use

- Marketing and advertising content
- Product visualization
- UI/UX design prototyping
- Social media graphics
- Custom illustrations
- Creative exploration
- Brand asset generation

## Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre-generation checklist, quality gates |
| [examples.md](examples.md) | Code examples for all providers |
| [templates.md](templates.md) | Reusable prompt templates |
| [llm-prompts.md](llm-prompts.md) | Meta-prompts for generating image prompts |

## Quick Reference

### DALL-E 3 Sizes

| Size | Aspect | Use Case |
|------|--------|----------|
| 1024x1024 | 1:1 | Social media, avatars |
| 1792x1024 | 16:9 | Hero images, banners |
| 1024x1792 | 9:16 | Stories, mobile |

### DALL-E 3 Styles

| Style | Effect |
|-------|--------|
| vivid | Hyper-realistic, dramatic (default) |
| natural | Softer, more organic |

### DALL-E 3 Quality

| Quality | Effect | Cost |
|---------|--------|------|
| standard | Fast, lower detail | $0.04-0.08 |
| hd | Slower, higher detail | $0.08-0.12 |

### Stable Diffusion Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| guidance_scale | 1-20 | Prompt adherence (7.5 default) |
| num_inference_steps | 20-50 | Quality vs speed |
| negative_prompt | text | What to avoid |

### Flux Models

| Model | Speed | License | Use Case |
|-------|-------|---------|----------|
| Flux.1 schnell | 1-4 steps | Apache 2.0 | Fast prototyping |
| Flux.1 dev | 20-50 steps | Non-commercial | Development |
| Flux.1/2 pro | 25+ steps | Commercial | Production |
| Flux.2 klein | Sub-second | Apache 2.0 | Real-time |

## Prompt Structure Formula

```
[Subject] + [Style] + [Lighting] + [Composition] + [Details] + [Technical]
```

**Example:**
```
A futuristic city skyline at sunset,
digital art style with vibrant colors,
golden hour lighting with warm tones,
wide angle composition,
flying cars and glass buildings,
8K resolution, cinematic film grain
```

## Model Selection Guide

| Requirement | Recommended Model |
|-------------|-------------------|
| Best prompt adherence | DALL-E 3, GPT-4o |
| Fastest generation | Flux.2 klein, SDXL Turbo |
| Most artistic | Midjourney |
| Best for customization | Stable Diffusion + LoRA |
| Best text rendering | DALL-E 3, GPT-4o |
| Best anatomy | Flux.1/2, GPT-4o |
| Free/self-hosted | Stable Diffusion, Flux schnell |
| Enterprise/scale | Stable Diffusion 3.5 (AWS Bedrock) |

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Vague prompts | Use structured formula with 6+ keywords |
| Wrong aspect ratio | Match to use case (social, banner, mobile) |
| No caching | Implement result caching to avoid regeneration |
| Ignoring revised prompts | Check DALL-E's revised_prompt for actual generation |
| Text rendering issues | Use GPT-4o or keep text under 25 chars |
| Inconsistent characters | Use seeds (SD) or reference images (Flux Kontext) |
| Content policy violations | Pre-filter prompts, handle rejections gracefully |

## Resources

- [DALL-E 3 Documentation](https://platform.openai.com/docs/guides/images)
- [Stability AI Models](https://stability.ai/stable-image)
- [Black Forest Labs (Flux)](https://bfl.ai/)
- [Replicate API](https://replicate.com/docs)
- [HuggingFace SDXL](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Prompt crafting | sonnet | Prompt engineering |
| Model selection | haiku | Tool selection |
| Image quality optimization | sonnet | Quality tuning |
