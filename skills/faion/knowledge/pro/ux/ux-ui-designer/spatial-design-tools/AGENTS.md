---
slug: spatial-design-tools
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A phase-gated tool selection methodology for spatial (AR/VR/MR) product workflows: concept in Figma + ShapesXR, prototype in Unity or Unreal, production in engine.
content_id: "160b0bc9bb1734dd"
tags: [spatial-computing, ar-vr-mr, tool-selection, design-workflow, asset-pipeline]
---
# Spatial Design Tools

## Summary

**One-sentence:** A phase-gated tool selection methodology for spatial (AR/VR/MR) product workflows: concept in Figma + ShapesXR, prototype in Unity or Unreal, production in engine.

**One-paragraph:** A phase-gated tool selection methodology for spatial (AR/VR/MR) product workflows: concept in Figma + ShapesXR, prototype in Unity or Unreal, production in engine. Standardize on USD/USDZ for visionOS, glTF for Web/Quest handoff. Asset-budget constraints (polygon count, file size) must be set at concept stage, not after artist work is done.

## Applies If (ALL must hold)

- Choosing or reviewing a tool stack for a new AR/VR/MR project.
- Setting up designer-to-developer handoff path (Figma 2D wireframes → ShapesXR → Unity/Unreal).
- Evaluating a solopreneur stack for visionOS, Quest, or WebXR delivery.
- Onboarding designers from 2D backgrounds onto a spatial workflow.

## Skip If (ANY kills it)

- 2D-only projects — spatial tool overhead yields no benefit.
- Teams already locked into a vendor mid-project — switching costs exceed gains.
- Marketing-only AR effects — Spark AR / Lens Studio handle that niche; the full landscape is overkill.

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
