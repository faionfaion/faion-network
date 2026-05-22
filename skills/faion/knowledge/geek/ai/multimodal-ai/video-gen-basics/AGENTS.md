---
slug: video-gen-basics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Generating short video clips from text or image input using Runway, Luma, Replicate, or Pika.
content_id: "67df9c2719984296"
tags: [video-generation, ai-video, runway, async-polling, ffmpeg]
---
# Video Generation Basics

## Summary

**One-sentence:** Generating short video clips from text or image input using Runway, Luma, Replicate, or Pika.

**One-paragraph:** Generating short video clips from text or image input using Runway, Luma, Replicate, or Pika. Covers service comparison, VideoPromptBuilder for structured prompt construction, ffmpeg utilities for post-processing, and the async generation polling pattern.

## Applies If (ALL must hold)

- Generating short marketing or social media videos from text descriptions
- Animating static product images into demo clips
- Prototyping visual content before committing to full production
- Creating background loops or b-roll for video pipelines
- Automating video content in content pipelines

## Skip If (ANY kills it)

- Precise temporal control needed (specific actions at specific timestamps) — current models cannot enforce this
- Character consistency across multiple shots is mandatory — models drift between generations
- Videos longer than 10-15 seconds without chaining — extend or concatenate via ffmpeg
- Real-time generation required — generation takes 30-300s per clip; not user-interactive

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
