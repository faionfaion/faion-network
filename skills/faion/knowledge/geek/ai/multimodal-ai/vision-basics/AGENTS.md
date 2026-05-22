---
slug: vision-basics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Analyze images with VLM APIs (GPT-4o, Claude Sonnet, Gemini Flash): single-image analysis, multi-image comparison, structured JSON extraction via Pydantic, and stateful visual Q&A.
content_id: "8b214b9c67435fbf"
tags: [vision, vlm, structured-extraction, pydantic, image-analysis]
---
# Vision Basics

## Summary

**One-sentence:** Analyze images with VLM APIs (GPT-4o, Claude Sonnet, Gemini Flash): single-image analysis, multi-image comparison, structured JSON extraction via Pydantic, and stateful visual Q&A.

**One-paragraph:** Analyze images with VLM APIs (GPT-4o, Claude Sonnet, Gemini Flash): single-image analysis, multi-image comparison, structured JSON extraction via Pydantic, and stateful visual Q&A. Covers input methods (URL vs. base64), detail settings, token cost control, and the failure modes that make VLMs unsuitable for precision tasks.

## Applies If (ALL must hold)

- Agents need to read content from screenshots, diagrams, or scanned forms.
- Pipeline receives images as intermediate outputs (web scraping returns screenshot; agent reads the page).
- Generating alt-text or captions for images at scale.
- Classifying images (safe/unsafe, relevant/irrelevant) as a routing step.
- Extracting text from images when dedicated OCR is unavailable or layout is complex.

## Skip If (ANY kills it)

- Real-time video analysis at >2 FPS — VLM API latency (500ms-2s) is too high; use YOLOv11 or GroundingDINO locally.
- High-volume barcode/QR decoding — use zxing or python-qrcode; 100x cheaper and deterministic.
- Pixel-level measurement — VLM outputs are statistical estimates, not precise values.
- Privacy-sensitive images that must not leave the local environment — use Qwen2.5-VL or LLaVA via Ollama.
- Tasks reducible to image metadata (EXIF, creation date) — VLMs cannot see metadata; use Pillow or ExifTool.
- Medical, legal, or forensic images where model content policies may silently reject inputs.

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
