# Image Generation Basics

## Summary

Core patterns for AI image generation using DALL-E 3, SDXL, and Flux: structured prompt construction with ImagePromptBuilder, batch generation with ThreadPoolExecutor, the image-to-image cycle via GPT-4o Vision, and the critical rate-limit and URL-expiry gotchas.

## Why

DALL-E 3 silently rewrites prompts (`revised_prompt` can diverge substantially), has a 5 images/minute rate limit on tier 1, and returns URLs that expire in ~1 hour. Structured prompt building and immediate image download on generation are the two non-negotiable production rules.

## When To Use

- Generating article headers, social media visuals, or product mockups from text
- Creating image variations for A/B testing at scale
- Automating visual asset production in content pipelines
- Reimagining or restyling an existing image (vision → describe → generate cycle)
- Batch generating illustration sets for structured prompts

## When NOT To Use

- Pixel-perfect brand consistency required — DALL-E 3 revised prompts alter the image silently
- Images will be used without human review in regulated contexts (medical, legal, financial)
- Subject requires real-person likeness — OpenAI policy blocks this
- Exact text rendering in the image is required — all current models are unreliable for on-image text
- High volume where cost is primary constraint — use Replicate Flux-schnell instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-generation.xml` | generate_image / generate_and_save; DALL-E 2 variation and edit endpoints; BatchImageGenerator |
| `content/02-prompting.xml` | ImagePromptBuilder with style/lighting/composition/technical fields; image-to-image vision cycle |
| `content/03-rules.xml` | Rate-limit rule, URL expiry rule, revised_prompt logging rule, content policy handling |

## Templates

| File | Purpose |
|------|---------|
| `templates/dalle3.py` | generate_image, generate_and_save, generate_variations, edit_image |
| `templates/prompt-builder.py` | ImagePromptBuilder fluent API |
| `templates/batch-generator.py` | BatchImageGenerator with ThreadPoolExecutor and rate-limit-safe variant |
| `templates/prompt-generate.txt` | Agent task prompt: brief → ImagePromptBuilder call → generate with retry |
