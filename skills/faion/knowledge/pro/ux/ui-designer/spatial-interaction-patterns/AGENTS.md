---
slug: spatial-interaction-patterns
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reference for the five input modalities in spatial/XR interfaces (hand tracking, controllers, gaze, voice, gesture) and the three primary interaction patterns (direct manipulation, ray-casting, gaze+dwell) with their respective use cases, strengths, and accessibility implications.
content_id: "aba67744189197d0"
tags: [spatial-interaction, xr, input-modality, accessibility, gesture]
---
# Spatial Interaction Patterns

## Summary

**One-sentence:** Reference for the five input modalities in spatial/XR interfaces (hand tracking, controllers, gaze, voice, gesture) and the three primary interaction patterns (direct manipulation, ray-casting, gaze+dwell) with their respective use cases, strengths, and accessibility implications.

**One-paragraph:** Reference for the five input modalities in spatial/XR interfaces (hand tracking, controllers, gaze, voice, gesture) and the three primary interaction patterns (direct manipulation, ray-casting, gaze+dwell) with their respective use cases, strengths, and accessibility implications.

## Applies If (ALL must hold)

- Designing interaction flows for an XR application
- Selecting primary and fallback input modalities for a spatial feature
- Evaluating an existing XR interaction for accessibility (gaze+dwell as motor-impairment fallback)
- Writing interaction specifications for XR developers

## Skip If (ANY kills it)

- 2D touch or mouse-based interfaces — different interaction model
- Voice-only VUI design — use error-handling-in-vui or vui-accessibility-inclusivity instead
- Platform selection decisions — use spatial-computing-overview instead

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

- parent skill: `pro/ux/ui-designer/`
