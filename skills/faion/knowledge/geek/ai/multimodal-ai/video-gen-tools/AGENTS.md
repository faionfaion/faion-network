---
slug: video-gen-tools
tier: geek
group: ai
domain: multimodal-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: API client implementations for Runway Gen-3, Luma Dream Machine, and Replicate video models (SVD, AnimateDiff, Zeroscope).
content_id: "327017ff03a6f9d1"
tags: [video-generation, runway, luma, replicate, async]
---
# Video Generation Tools

## Summary

**One-sentence:** API client implementations for Runway Gen-3, Luma Dream Machine, and Replicate video models (SVD, AnimateDiff, Zeroscope).

**One-paragraph:** API client implementations for Runway Gen-3, Luma Dream Machine, and Replicate video models (SVD, AnimateDiff, Zeroscope). Includes a production async VideoGenerationService with multi-provider fallback, retry logic, and a stub for image upload that must be implemented per storage backend.

## Applies If (ALL must hold)

- Integrating Runway, Luma, or Replicate into an automated content pipeline
- Building multi-provider fallback logic for resilience
- Extending an existing video by appending new AI-generated segments
- Wrapping async generation in retry/timeout logic for production reliability

## Skip If (ANY kills it)

- Single one-off clip — use the web UI directly; API setup overhead is not justified
- Synchronous request/response architectures — all video APIs are async polling; this pattern will block
- When video quality is untested — validate provider outputs manually before automating at scale
- Latency-sensitive user flows (sub-2s response expected)

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
