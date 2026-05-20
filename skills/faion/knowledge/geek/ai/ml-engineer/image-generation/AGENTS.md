---
slug: image-generation
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AI image generation from text prompts using DALL-E 3, Flux (Black Forest Labs), Stable Diffusion, and related APIs.
content_id: "80dd113ad849d676"
tags: [image-generation, dall-e, flux, stable-diffusion, multimodal]
---
# AI Image Generation: Model Selection and Pipeline Automation

## Summary

**One-sentence:** AI image generation from text prompts using DALL-E 3, Flux (Black Forest Labs), Stable Diffusion, and related APIs.

**One-paragraph:** AI image generation from text prompts using DALL-E 3, Flux (Black Forest Labs), Stable Diffusion, and related APIs. Covers model selection, prompt engineering formula ([Subject] + [Style] + [Lighting] + [Composition] + [Details] + [Technical]), API integration patterns, and pipeline automation for content at scale.

## Applies If (ALL must hold)

- Generating marketing visuals, social media graphics, or product mockups as part of an automated content pipeline
- Producing custom illustrations for articles, blog posts, or newsletters where stock photography is inadequate
- Rapid UI/UX prototyping: visualizing interface concepts before implementation
- Generating variation sets (A/B test creatives) at scale for advertising campaigns
- Brand asset generation with consistent style through fine-tuned models or style references
- AI news pipelines where each article requires a unique header image generated from the article summary

## Skip If (ANY kills it)

- Legal/medical/financial documents where image hallucinations create liability
- Photorealistic images of real named people — content policy violations plus legal risk (likeness rights)
- Logo design requiring precise vector output — generative models produce raster; use a designer or vector tools
- High-volume generation where per-image cost matters at scale — self-host Flux schnell (Apache 2.0) instead of paying per API call
- Consistent character generation across many images without Flux Kontext or LoRA — models don't preserve identity by default
- Anything requiring exact pixel-level control (infographics with precise data, technical diagrams)

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ml-engineer/`
