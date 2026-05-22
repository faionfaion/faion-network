---
slug: video-generation-prompt-engineering
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Effective video generation prompts follow the formula: Subject + Action + Setting + Style + Camera + Lighting.
content_id: "3ecba486ab73383b"
tags: [video-generation, prompt-engineering, runway, luma, veo]
---
# AI Video Generation Prompt Engineering

## Summary

**One-sentence:** Effective video generation prompts follow the formula: Subject + Action + Setting + Style + Camera + Lighting.

**One-paragraph:** Effective video generation prompts follow the formula: Subject + Action + Setting + Style + Camera + Lighting. Each provider processes prompts differently — Runway prefers cinematic camera directions while Luma prefers descriptive scene prose. Provider-specific prompt patterns yield significantly better results than generic descriptions.

## Applies If (ALL must hold)

- Writing prompts for any video generation provider (Runway, Luma, Sora 2, Veo 3, Replicate).
- Creating prompt templates for automated content pipelines (news B-roll, social media, product videos).
- Optimizing existing prompts that produce inconsistent or low-quality output.
- Building a prompt library for reuse across agent workflows.

## Skip If (ANY kills it)

- Prompting for precise multi-shot character consistency — current models drift across clips regardless of prompt quality; use image seeding as a supplement.
- Controlling native audio content in Sora 2 or Veo 3 — audio is non-deterministic and cannot be controlled via prompt.

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
