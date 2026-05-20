---
slug: img-gen-basics
tier: geek
group: ai
domain: multimodal-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: DALL-E 3 is the gold standard for photorealistic image generation but has a 5 images/minute rate limit, rewrites prompts silently, and returns URLs that expire in ~1 hour.
content_id: "902b86ac7aa22ef9"
tags: [image-generation, dalle, flux, ai-content-production, visual-assets]
---
# Image Generation Basics: DALL-E, Flux, and SDXL

## Summary

**One-sentence:** DALL-E 3 is the gold standard for photorealistic image generation but has a 5 images/minute rate limit, rewrites prompts silently, and returns URLs that expire in ~1 hour.

**One-paragraph:** DALL-E 3 is the gold standard for photorealistic image generation but has a 5 images/minute rate limit, rewrites prompts silently, and returns URLs that expire in ~1 hour. SDXL and Flux-schnell via Replicate are significantly cheaper (~100x) and work well for social content. The essentials are: (1) structure prompts with ImagePromptBuilder (subject, style, lighting, composition, technical specs), (2) log revised_prompt for audit, (3) download images immediately, (4) respect rate limits, (5) test prompts manually before batch.

## Applies If (ALL must hold)

- Generating article header images, social media visuals, or product mockups from text descriptions.
- Creating image variations for A/B testing content at scale.
- Automating visual asset production in content pipelines.
- Reimagining/restyling an existing image (vision → describe → generate cycle).
- Batch generating illustration sets for structured prompts (e.g., FAQ cards, product categories).

## Skip If (ANY kills it)

- Pixel-perfect brand consistency is required — DALL-E 3 revised prompts silently alter inputs.
- Images will be used without human review in regulated contexts (medical, legal, financial).
- Subject requires real-person likeness — OpenAI policy blocks this.
- High-volume generation where cost is primary constraint — DALL-E 3 at $0.04–$0.12/image adds up fast; use Replicate/Flux for cost.
- Exact text rendering in image is required — all current models struggle with on-image text.

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

- parent skill: `geek/ai/multimodal-ai/`
