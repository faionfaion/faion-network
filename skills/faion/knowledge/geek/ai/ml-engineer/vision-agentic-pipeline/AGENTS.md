---
slug: vision-agentic-pipeline
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production vision pipelines use a three-subagent chain: image-router (classifies image type, selects VLM + prompt), vision-extractor (calls VLM, enforces structured output, returns Pydantic model), validation-agent (cross-checks extracted fields against business rules).
content_id: "22dffbb575dbdd5e"
tags: [vision, agentic, pipeline, vlm, production]
---
# Vision Agentic Pipeline: Production Architecture

## Summary

**One-sentence:** Production vision pipelines use a three-subagent chain: image-router (classifies image type, selects VLM + prompt), vision-extractor (calls VLM, enforces structured output, returns Pydantic model), validation-agent (cross-checks extracted fields against business rules).

**One-paragraph:** Production vision pipelines use a three-subagent chain: image-router (classifies image type, selects VLM + prompt), vision-extractor (calls VLM, enforces structured output, returns Pydantic model), validation-agent (cross-checks extracted fields against business rules). Low-confidence extractions (<0.85) route to a human-review queue. The VisionService class wraps this with retry logic, multi-provider fallback, and async batch processing.

## Applies If (ALL must hold)

- Agent-driven document processing workflows where images arrive as tool results from other agents.
- Visual Q&A over a corpus of images (product catalogs, medical scans, satellite imagery).
- Multi-provider resilience requirements where single-provider downtime must not block the pipeline.
- High-volume batch document processing that must scale beyond single-threaded VLM calls.
- Pipelines where business-rule validation on extracted data is required before downstream writes.

## Skip If (ANY kills it)

- Simple one-off image descriptions — a single VLM call is sufficient; the router-extractor-validator overhead is not justified.
- Real-time video frame analysis at >5 FPS — VLM API latency (500 ms–2 s) makes this impractical; use local CV models.
- Privacy-sensitive images where sending to third-party APIs violates data agreements — use self-hosted Qwen3-VL or GLM-4.5V and run the pipeline locally.

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
