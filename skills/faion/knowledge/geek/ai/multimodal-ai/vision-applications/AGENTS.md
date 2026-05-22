---
slug: vision-applications
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production patterns for vision LLM tasks: OCR, document extraction, image classification, and content moderation using GPT-4o, Claude, or Gemini Vision.
content_id: "c81d8dc8021b63cb"
tags: [vision, ocr, document-extraction, image-classification, content-moderation]
---
# Vision Applications

## Summary

**One-sentence:** Production patterns for vision LLM tasks: OCR, document extraction, image classification, and content moderation using GPT-4o, Claude, or Gemini Vision.

**One-paragraph:** Production patterns for vision LLM tasks: OCR, document extraction, image classification, and content moderation using GPT-4o, Claude, or Gemini Vision. Each task sends an image plus a structured prompt and receives JSON-formatted output.

## Applies If (ALL must hold)

- Document digitization: invoices, receipts, forms, passports, business cards
- Content moderation: classify user-uploaded images before storage or display
- E-commerce: auto-tag product images, generate descriptions, classify categories
- Accessibility: generate alt-text for images at upload time
- Visual QA: answer questions about screenshots, diagrams, charts

## Skip If (ANY kills it)

- High-volume bulk processing (>10k images/day) — per-image token cost accumulates; CLIP/YOLO/Tesseract are 100-1000x cheaper for classification/detection
- Pixel-level precision tasks (medical imaging, satellite analysis) — vision LLMs reason semantically, not at pixel level
- Real-time video analysis — frame-by-frame API calls add 1-3s latency per frame
- Standardized forms with fixed layout — dedicated OCR tools are faster and cheaper

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
