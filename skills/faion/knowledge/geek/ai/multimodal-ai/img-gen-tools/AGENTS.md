---
slug: img-gen-tools
tier: geek
group: ai
domain: multimodal-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production image generation service covering DALL-E 3, Flux, and SDXL with caching, retry, and multi-provider fallback.
content_id: "9f7b82dfb8a26503"
tags: [image-generation, multi-provider, caching, production, dalle3, flux, sdxl]
---
# Image Generation Tools and Production

## Summary

**One-sentence:** Production image generation service covering DALL-E 3, Flux, and SDXL with caching, retry, and multi-provider fallback.

**One-paragraph:** Production image generation service covering DALL-E 3, Flux, and SDXL with caching, retry, and multi-provider fallback. Includes ImagePipeline for variant sets and A/B testing, and PromptTemplates static methods for common use cases.

## Applies If (ALL must hold)

- Running a multi-provider image generation service where one provider may be unavailable
- Batch-generating style/size variant sets (e.g., 3 styles × 4 sizes = 12 images per concept)
- Building A/B test image sets automatically from a concept description
- Caching production image generation to avoid duplicate API costs
- Automating image generation inside a content pipeline (article images, social cards, etc.)

## Skip If (ANY kills it)

- Single image generation — ImageGenerationService adds overhead not justified for one call
- When provider selection logic needs human approval — automated fallback can silently produce lower-quality output
- High-frequency real-time requests (sub-second) — all providers have multi-second latency
- When DALL-E content policy is frequently triggered — automated pipelines will silently skip images

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
