# Adobe Firefly Integration

## Summary

Workflow for integrating Adobe Firefly generative AI into Creative Cloud pipelines — structured image brief generation (positive prompt, negative prompt, style preset, aspect ratio), batch generation via Firefly Services API (enterprise), and brand-compliance auditing of generated assets. Agents operate in brief-generation and post-processing layers; direct API automation requires enterprise Firefly Services access.

## Why

Firefly's commercial-safe training (Adobe Stock) eliminates stock licensing risk for generated imagery. Without structured prompts and negative prompts, outputs trend toward generic stock aesthetics and may not match brand guidelines. AI amplifies prompt quality — a vague brief produces unusable output at scale; a structured brief produces consistent, reviewable variants.

## When To Use

- Generating commercial-safe imagery for marketing, product pages, or editorial content
- Creating on-brand variations of existing images at scale (background removal, generative fill for product shots)
- Producing vector assets from text descriptions for icon sets or illustration libraries
- Text effects and typography treatments for campaign assets
- Batch asset generation within an established Creative Cloud workflow

## When NOT To Use

- UI/UX prototyping — use Figma; Firefly does not produce interactive components
- Developer handoff assets — Firefly generates raster/vector art, not production-ready SVG component assets
- When generative credits are exhausted and content deadline is imminent — have a stock fallback
- Brand-critical assets requiring exact color accuracy — AI introduces color variation; validate against brand palette
- When style guide strictly requires human-created imagery (certain editorial, legal, or medical contexts)

## Content

| File | What's inside |
|------|---------------|
| `content/01-workflow-and-rules.xml` | Firefly capability map, prompt structure rules, API access requirements |
| `content/02-tools-and-gotchas.xml` | CLI tools, services, agent workflow, limitations, AI gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/batch-prompt-generator.py` | Generate structured Firefly Services batch API payload from content brief + brand guide |
| `templates/prompt-image-brief.txt` | Agent prompt: generate structured Firefly prompts from content brief and brand guide |
| `templates/prompt-asset-audit.txt` | Agent prompt: audit generated images against brand standards |
