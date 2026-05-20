---
slug: video-generation-production-service
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production video generation services require a multi-provider abstraction with automatic retry and fallback, an async job API (FastAPI or similar) for caller decoupling, a priority queue for high-volume workloads, and ffmpeg utilities for clip assembly and processing.
content_id: "827f89b9d42fd8d7"
tags: [video-generation, production, fastapi, queue, ffmpeg]
---
# AI Video Generation Production Service

## Summary

**One-sentence:** Production video generation services require a multi-provider abstraction with automatic retry and fallback, an async job API (FastAPI or similar) for caller decoupling, a priority queue for high-volume workloads, and ffmpeg utilities for clip assembly and processing.

**One-paragraph:** Production video generation services require a multi-provider abstraction with automatic retry and fallback, an async job API (FastAPI or similar) for caller decoupling, a priority queue for high-volume workloads, and ffmpeg utilities for clip assembly and processing. All generated video URLs must be downloaded immediately since provider URLs expire in 24-72h.

## Applies If (ALL must hold)

- Building a content pipeline that generates more than a few videos per day.
- Exposing video generation as an internal API endpoint for other services or agents.
- Requiring fallback across multiple providers (Runway, Luma, Replicate) for reliability.
- Processing concurrent video generation requests at volume with priority ordering.
- Assembling multi-clip sequences with audio overlay using ffmpeg.

## Skip If (ANY kills it)

- Single one-off video generation in a script — use the direct API calls from video-generation-async-api instead; this service adds unnecessary overhead.
- Architectures without persistent storage — the service downloads videos locally; ensure storage is provisioned.

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
