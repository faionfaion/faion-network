---
slug: spatial-interaction-patterns
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Input modalities and interaction patterns for spatial (AR/VR/MR) computing: hand tracking, controllers, gaze, voice, and gesture.
content_id: "aba67744189197d0"
tags: [spatial-interaction, input-modalities, xr-design, accessibility, gesture-design]
---
# Spatial Interaction Patterns

## Summary

**One-sentence:** Input modalities and interaction patterns for spatial (AR/VR/MR) computing: hand tracking, controllers, gaze, voice, and gesture.

**One-paragraph:** Input modalities and interaction patterns for spatial (AR/VR/MR) computing: hand tracking, controllers, gaze, voice, and gesture. Design interaction state machines for direct manipulation, ray-cast selection, or gaze+dwell with primary + fallback modalities.

## Applies If (ALL must hold)

- Choosing input modality (hands / controllers / gaze / voice / gesture) per task in an XR app.
- Designing interaction state machines for direct manipulation, ray-cast selection, or gaze+dwell.
- Drafting accessibility-friendly multi-modal alternatives (voice or gaze fallback for fine motor).
- Specifying gesture vocabulary and conflict resolution in mixed-input apps.

## Skip If (ANY kills it)

- 2D mobile/desktop interactions — wrong vocabulary entirely.
- Pure 360° lean-back content where the user does not interact.
- Pre-strategy phases — pair with spatial-ux-fundamentals first to set field/scale before pattern choice.

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

- parent skill: `pro/ux/ux-ui-designer/`
