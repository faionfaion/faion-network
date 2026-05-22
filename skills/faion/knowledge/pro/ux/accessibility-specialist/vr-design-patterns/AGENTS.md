---
slug: vr-design-patterns
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design patterns for fully-immersive 6DoF VR covering environment anchoring (ground plane, horizon, stable reference objects), locomotion menu (teleport default + smooth opt-in), UI placement (world-locked or body-locked, 1.
content_id: "6543f00fc9abea0c"
tags: [vr, immersive-design, accessibility, design-patterns, comfort]
---
# VR Design Patterns for Accessibility and Comfort

## Summary

**One-sentence:** Design patterns for fully-immersive 6DoF VR covering environment anchoring (ground plane, horizon, stable reference objects), locomotion menu (teleport default + smooth opt-in), UI placement (world-locked or body-locked, 1.

**One-paragraph:** Design patterns for fully-immersive 6DoF VR covering environment anchoring (ground plane, horizon, stable reference objects), locomotion menu (teleport default + smooth opt-in), UI placement (world-locked or body-locked, 1.5-3 m, eye-level, no head-lock), comfort settings (vignette, snap turn, FOV cap, seated mode), and accessibility parity across disability categories. Minimum 14-16 pt text, 90 FPS / 20 ms motion-to-photon, teleport-as-default.

## Applies If (ALL must hold)

- Designing fully-immersive VR experiences (Quest 2/3/Pro, PSVR2, Valve Index, PICO 4, Vision Pro full-immersion mode).
- Choosing locomotion and UI placement strategy.
- Implementing comfort settings: vignette, snap turn, FOV cap, seated mode, height calibration.
- Auditing an existing VR title for accessibility and motion-sickness risk.

## Skip If (ANY kills it)

- AR/passthrough/MR — use `ar-design-patterns` and `immersive-design-principles` instead.
- 360-degree video in Cardboard-style viewers — constrained interaction, not 6DoF.
- Mixed-reality productivity with passthrough — use `immersive-design-principles` blended-mode territory.
- WebXR mobile sessions where 90 FPS is unreachable.

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

- parent skill: `pro/ux/accessibility-specialist/`
