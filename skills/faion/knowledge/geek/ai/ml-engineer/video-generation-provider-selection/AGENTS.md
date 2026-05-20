---
slug: video-generation-provider-selection
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Video generation has evolved rapidly with commercial APIs from Runway, Luma, OpenAI Sora, and Google Veo providing production-ready solutions.
content_id: "ba88788149b2cb72"
tags: [video-generation, runway, luma, sora, provider-selection]
---
# AI Video Generation Provider Selection

## Summary

**One-sentence:** Video generation has evolved rapidly with commercial APIs from Runway, Luma, OpenAI Sora, and Google Veo providing production-ready solutions.

**One-paragraph:** Video generation has evolved rapidly with commercial APIs from Runway, Luma, OpenAI Sora, and Google Veo providing production-ready solutions. Select a provider by matching its unique capabilities (lip-sync, native audio, duration, resolution) to task requirements before writing any integration code.

## Applies If (ALL must hold)

- Selecting a provider before starting any video generation integration.
- Evaluating provider capabilities for a new content pipeline (news, social media, marketing).
- Switching providers due to API access changes, cost, or quality regression.
- Building a multi-provider abstraction and deciding which providers to include.

## Skip If (ANY kills it)

- Provider already selected and integration is underway — refer to async-api or production-service methodologies instead.
- Precise character consistency across multiple shots is required — no current provider reliably delivers this; consider human production.
- Video longer than 60 seconds from a single call is needed — all current APIs cap at 5-60s per generation; use concat workflow instead.

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
