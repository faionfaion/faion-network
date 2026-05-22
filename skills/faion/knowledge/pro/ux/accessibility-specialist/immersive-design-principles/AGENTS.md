---
slug: immersive-design-principles
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A framework for XR/AR/VR/MR experience design covering immersion-level selection (passthrough, blended, fully immersive, portal), motion-comfort mitigations (vignette, snap turn, teleport, grounding), comfort settings completeness, spatial layout rules, and WAI XAUR accessibility coverage.
content_id: "dd6f3c78683d296b"
tags: [xr-design, vr, ar, immersive, accessibility]
---
# Immersive Design Principles

## Summary

**One-sentence:** A framework for XR/AR/VR/MR experience design covering immersion-level selection (passthrough, blended, fully immersive, portal), motion-comfort mitigations (vignette, snap turn, teleport, grounding), comfort settings completeness, spatial layout rules, and WAI XAUR accessibility coverage.

**One-paragraph:** A framework for XR/AR/VR/MR experience design covering immersion-level selection (passthrough, blended, fully immersive, portal), motion-comfort mitigations (vignette, snap turn, teleport, grounding), comfort settings completeness, spatial layout rules, and WAI XAUR accessibility coverage. Default every new experience to highest-comfort settings; let users opt into lower comfort.

## Applies If (ALL must hold)

- Designing or auditing VR/AR/MR/passthrough experiences across Meta Quest, Apple Vision Pro, PSVR2, PICO, HoloLens.
- Choosing the right immersion level for a use case.
- Reviewing comfort settings, locomotion, grounding, and motion-sickness mitigations before user testing.
- Making spatial UIs accessible across vision, hearing, mobility, and cognitive needs.

## Skip If (ANY kills it)

- Pure 2D web/mobile work — use `wcag-22-compliance` and `a11y-basics` instead.
- Hardware/optics tuning (IPD, lens distortion) — those live in the engine/SDK layer.
- Game-feel tuning where intentional motion sickness is a deliberate design choice.
- Conversion-rate optimization for XR storefronts — adjacent topic, not this skill.

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
