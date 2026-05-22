---
slug: adobe-firefly-integration
tier: geek
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use Adobe Firefly Services REST API to batch-generate commercial-safe images, apply Generative Fill to placeholder regions, and produce vector assets from text prompts.
content_id: "8ae553d58f3928d8"
tags: [firefly, generative-ai, asset-generation, api-integration, automation]
---
# Adobe Firefly Integration

## Summary

**One-sentence:** Use Adobe Firefly Services REST API to batch-generate commercial-safe images, apply Generative Fill to placeholder regions, and produce vector assets from text prompts.

**One-paragraph:** Use Adobe Firefly Services REST API to batch-generate commercial-safe images, apply Generative Fill to placeholder regions, and produce vector assets from text prompts. Firefly is trained on licensed content with clear generative-credit accounting — it is the correct tool when commercial IP safety is required. All generated assets require a human brand-alignment review before production promotion.

## Applies If (ALL must hold)

- Generating commercial-safe image assets for UI mockups, marketing banners, or product visuals
- Creating vector assets in Illustrator via text-to-vector prompts for icon sets
- Removing or replacing image backgrounds in Photoshop for product shots or hero images
- Producing asset variations (color, style, format) from a single source for A/B testing
- Applying AI-generated text effects and typography variations at scale

## Skip If (ANY kills it)

- Design requires a coherent custom illustration style — Firefly outputs generic aesthetics
- Iterating on UI layout or component design — Figma is the correct tool
- Team has no Adobe CC enterprise licenses — generative credits are consumed per generation and the API requires enterprise plan
- Output must strictly match an established illustration system — Firefly cannot learn custom styles
- Speed is critical and assets must integrate directly into Figma without round-trips

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

- parent skill: `geek/ux/ui-designer/`
