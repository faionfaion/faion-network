# Image Generation

## Summary

AI image generation from text prompts using DALL-E 3, Flux (Black Forest Labs), Stable Diffusion, and related APIs. Covers model selection, prompt engineering formula ([Subject] + [Style] + [Lighting] + [Composition] + [Details] + [Technical]), API integration patterns, and pipeline automation for content at scale.

## Why

Each model has a distinct strength profile: DALL-E 3 and GPT-4o lead on text rendering and prompt adherence; Flux leads on photorealism and anatomy; Stable Diffusion + LoRA is the only option for brand-specific fine-tuned assets; Flux schnell (Apache 2.0) is the cost-effective choice for high-volume batch generation. Selecting the wrong model wastes cost or produces unusable output.

## When To Use

- Marketing visuals, social media graphics, product mockups in automated content pipelines
- Custom illustrations for articles/newsletters where stock photography is inadequate
- Rapid UI/UX prototyping: visualizing interface concepts before implementation
- Generating A/B test creative variants at scale for advertising campaigns
- Brand asset generation with consistent style via fine-tuned models or style references

## When NOT To Use

- Legal/medical/financial documents where image hallucinations create liability
- Photorealistic images of real named people — content policy violations and likeness rights risk
- Logo design requiring precise vector output — generative models produce raster only
- High-volume generation where per-image API cost matters at scale — self-host Flux schnell (Apache 2.0)
- Consistent character generation across many images without Flux Kontext or LoRA
- Anything requiring exact pixel-level control: infographics with precise data, technical diagrams

## Content

| File | What's inside |
|------|---------------|
| `content/01-model-selection.xml` | Model comparison table, selection rules by use case, cost model, prompt formula |
| `content/02-pipeline.xml` | Agentic pipeline: prompt-engineer → image-generator → quality-checker; API gotchas; best practices |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-engineer.txt` | Prompt to transform a content brief into a structured generation prompt |
| `templates/generate-with-retry.py` | DALL-E 3 batch generation with content-policy retry and URL expiry handling |
