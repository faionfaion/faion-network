---
slug: vision-classification-moderation
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Image classification labels an image into one of N predefined categories; content moderation is a specialised classification that detects unsafe categories (violence, adult content, hate symbols) with severity levels.
content_id: "070af311b4a48c97"
tags: [vision, classification, content-moderation, vlm, safety]
---
# Vision Image Classification and Content Moderation

## Summary

**One-sentence:** Image classification labels an image into one of N predefined categories; content moderation is a specialised classification that detects unsafe categories (violence, adult content, hate symbols) with severity levels.

**One-paragraph:** Image classification labels an image into one of N predefined categories; content moderation is a specialised classification that detects unsafe categories (violence, adult content, hate symbols) with severity levels. Both tasks follow the same pattern: structured-output prompt → confidence score → routing to auto-approve/queue/reject. GPT-4o is the default model for both tasks.

## Applies If (ALL must hold)

- Content moderation pipeline where images are submitted by end users.
- Routing user-uploaded images to category-specific downstream processors.
- Automated labelling of product images, marketing assets, or media libraries.
- Quality assessment of uploaded images before publishing.
- Brand safety checks on programmatic advertising creatives.

## Skip If (ANY kills it)

- Object detection with bounding boxes at scale — fine-tuned YOLO/DETR models beat VLMs on throughput and cost by 10-100x.
- Real-time video moderation at >5 FPS — VLM API latency makes this impractical; use dedicated video moderation APIs (AWS Rekognition Video, Google Video Intelligence).
- Binary safe/unsafe moderation with very high throughput (>1000 images/s) — purpose-built moderation APIs (OpenAI Moderation, Perspective API) are faster and cheaper.
- Pixel-precise segmentation tasks — use DETR, SAM, or SegFormer instead.

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
