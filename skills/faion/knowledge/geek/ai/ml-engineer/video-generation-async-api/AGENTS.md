---
slug: video-generation-async-api
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: All AI video generation providers are async with 60-300s generation latency.
content_id: "ec4082babe7c1e86"
tags: [video-generation, async, polling, runway, api-integration]
---
# AI Video Generation Async API Patterns

## Summary

**One-sentence:** All AI video generation providers are async with 60-300s generation latency.

**One-paragraph:** All AI video generation providers are async with 60-300s generation latency. Agents must never block synchronously — use polling with exponential backoff, timeout guards, and immediate video download after completion since provider URLs expire in 24-72h.

## Applies If (ALL must hold)

- Integrating any video generation provider into an agent or service pipeline.
- Building a polling loop for Runway Gen-3, Luma Dream Machine, or Replicate video models.
- Implementing parallel multi-clip generation with ffmpeg assembly.
- Setting up agentic workflow: provider selection, job submission, poll, download, downstream handoff.

## Skip If (ANY kills it)

- Real-time generation needed (under 30s turnaround) — no current provider supports this; re-evaluate use case.
- Synchronous architecture where the caller cannot tolerate async callbacks or polling — restructure to async first.

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
