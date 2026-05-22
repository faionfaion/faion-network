---
slug: vision-provider-selection
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Modern Vision Language Models (VLMs) enable image understanding — OCR, document analysis, visual QA, classification, moderation, and accessibility.
content_id: "dcfe3035ac3d4733"
tags: [vision, vlm, model-selection, multimodal, provider]
---
# Vision Language Model Provider Selection

## Summary

**One-sentence:** Modern Vision Language Models (VLMs) enable image understanding — OCR, document analysis, visual QA, classification, moderation, and accessibility.

**One-paragraph:** Modern Vision Language Models (VLMs) enable image understanding — OCR, document analysis, visual QA, classification, moderation, and accessibility. Provider selection is the first and most cost-impactful decision: task type, volume, latency, and privacy requirements each favour a different model.

## Applies If (ALL must hold)

- Starting a new vision integration and choosing which VLM API to call first.
- Evaluating cost/quality trade-offs before committing to a provider for a batch pipeline.
- Switching providers because accuracy or cost requirements have changed.
- Selecting a self-hosted model for privacy-sensitive image processing.

## Skip If (ANY kills it)

- Barcode/QR decoding — specialised libraries (zxing, python-qrcode) are faster and cheaper than any VLM.
- Object detection with bounding boxes at scale — fine-tuned YOLO/DETR models beat VLMs on throughput and cost by orders of magnitude.
- Real-time video frame analysis at >5 FPS — VLM API latency (500 ms–2 s) makes this impractical; use local CV models.
- FDA/CE-certified medical imaging inference — off-the-shelf VLM APIs are not cleared devices.

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
