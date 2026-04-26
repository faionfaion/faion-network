# Image Generation Tools and Production

## Summary

Production-grade image generation service covering Stable Diffusion XL, Flux, and DALL-E 3 via a unified ImageGenerationService with caching, retry, and multi-provider fallback. Includes ImagePipeline for variant sets and A/B testing, and PromptTemplates static methods for common use cases.

## Why

Provider URLs expire (~1 hour for DALL-E), rate limits vary per tier, and different providers suit different use cases (DALL-E 3 for photorealism, Flux-schnell for volume, SDXL for controllable composition). A service layer with content-hash caching and provider selection heuristics prevents duplicate costs and silent fallback to lower-quality output.

## When To Use

- Running a multi-provider image service where one provider may be unavailable
- Batch-generating style/size variant sets for campaigns
- Building A/B test image sets automatically from a concept brief
- Caching production image generation to avoid duplicate API costs
- Automating image generation inside a content pipeline

## When NOT To Use

- Single image generation — the service layer adds overhead not justified for one call
- When provider selection needs human approval — automated fallback can silently produce lower-quality output
- High-frequency real-time requests (sub-second) — all providers have multi-second latency
- When DALL-E content policy is frequently triggered — automated pipelines will silently skip images

## Content

| File | What's inside |
|------|---------------|
| `content/01-service.xml` | ImageGenerationService with cache and retry; MultiProviderImageService fallback; known bugs |
| `content/02-pipeline.xml` | ImagePipeline variant sets and A/B generation; PromptTemplates for product/logo/social/UI |

## Templates

| File | Purpose |
|------|---------|
| `templates/image-service.py` | ImageGenerationService with SHA-256 caching and DALL-E 3 / SDXL backends |
| `templates/multi-provider.py` | MultiProviderImageService with ordered fallback |
| `templates/prompt-templates.py` | PromptTemplates static methods: product_photo, logo, social_media, ui_mockup |
| `templates/cache-to-s3.py` | Download generated image and upload to S3 to resolve URL expiry |
| `templates/prompt-generate.txt` | Agent task prompt for single image generation with provider and template selection |
