---
slug: immersive-design-principles
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Immersive experiences (AR/VR/MR/XR) balance presence with comfort.
content_id: "dd6f3c78683d296b"
tags: [immersive-design, vr, ar, mr, xr, comfort]
---
# Immersive Design Principles

## Summary

**One-sentence:** Immersive experiences (AR/VR/MR/XR) balance presence with comfort.

**One-paragraph:** Immersive experiences (AR/VR/MR/XR) balance presence with comfort. Four immersion levels exist: passthrough (real + overlays), blended (mixed real/virtual), immersive (full virtual), and portal (windows into virtual). Design with depth, realistic motion physics, environmental awareness, and smooth transitions. Address motion sickness, disorientation, eye strain, and arm fatigue via fixed reference points, grounding, proper depth of field, and rest positions. Test with real headsets and diverse user populations (glasses-wearers, 50+, first-time HMD users) because team tolerance is unrepresentative.

## Applies If (ALL must hold)

- Designing for AR/VR/MR headsets (Vision Pro, Quest 3, Pico 4, HoloLens 2) where immersion level must be deliberate.
- Mixed-reality enterprise tools (training, remote assistance, surgery planning) where over-immersion is a safety risk.
- Spatial gaming and entertainment where immersion-comfort tradeoff drives session length.
- Designing transitions between passthrough and fully-immersive states (the moment most discomfort happens).

## Skip If (ANY kills it)

- 2D mobile / web flows without spatial component.
- Simple AR effects (face filters, product try-on snippets) — overkill for one-shot interactions.
- Marketing-only "VR demo" projects with no real user-research budget; principles are wasted without testing.

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
