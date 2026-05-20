---
slug: spatial-ux-fundamentals
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Spatial UX organizes content in three physical zones: near field (0–1 m, primary interactions and controls), mid field (1–3 m, content consumption and work surfaces), far field (3 m+, ambient context and navigation aids).
content_id: "845db2e8bdce2a5f"
tags: [spatial-computing, vr, ux-design, ergonomics, hmd]
---
# Spatial UX Fundamentals

## Summary

**One-sentence:** Spatial UX organizes content in three physical zones: near field (0–1 m, primary interactions and controls), mid field (1–3 m, content consumption and work surfaces), far field (3 m+, ambient context and navigation aids).

**One-paragraph:** Spatial UX organizes content in three physical zones: near field (0–1 m, primary interactions and controls), mid field (1–3 m, content consumption and work surfaces), far field (3 m+, ambient context and navigation aids). Interactive controls must never be placed in the far field. Use 1.5–2.0 m as default content distance. Provide a recenter affordance. Test seated AND standing — comfortable reach shifts ~15°.

## Applies If (ALL must hold)

- Drafting first-pass UX requirements for Apple Vision Pro, Meta Quest, or HoloLens apps.
- Re-mapping a 2D mobile or desktop flow into near/mid/far field zones.
- Reviewing a spatial layout for reach, occlusion, sight-line, and orientation issues.
- Establishing shared spatial vocabulary across PM, engineering, and 3D teams.

## Skip If (ANY kills it)

- Phone AR snap-on features (banner overlays) — world-scale and reach constraints don't apply meaningfully.
- Desktop 3D viewers (CAD, Blender) — different ergonomic constraints than head-mounted spatial.
- 360-degree video lean-back content — viewer is passive; no reach or occlusion design is needed.

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
