---
slug: ar-design-patterns
tier: pro
group: ux
domain: accessibility-specialist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design patterns for augmented reality experiences on iOS (ARKit/RealityKit), Android (ARCore), WebAR (8th Wall, model-viewer), and social AR (Snap Lens Studio).
content_id: "f87d0aa0ebdaf898"
tags: [ar, augmented-reality, xr, arkit, arcore]
---
# AR Design Patterns

## Summary

**One-sentence:** Design patterns for augmented reality experiences on iOS (ARKit/RealityKit), Android (ARCore), WebAR (8th Wall, model-viewer), and social AR (Snap Lens Studio).

**One-paragraph:** Design patterns for augmented reality experiences on iOS (ARKit/RealityKit), Android (ARCore), WebAR (8th Wall, model-viewer), and social AR (Snap Lens Studio). Covers surface and object anchoring strategies, interaction patterns (touch, gaze, voice, controller), real/virtual distinction, safety considerations, comfort and performance constraints, and accessibility requirements per W3C XAUR.

## Applies If (ALL must hold)

- Designing AR experiences with spatial anchoring for iOS, Android, WebAR, or social AR platforms.
- Selecting an anchoring strategy (horizontal surface, vertical surface, image tracking, object recognition, geo).
- Auditing AR UX for safety, occlusion quality, accessibility, and performance.
- Building retail try-on, maintenance overlay, museum, navigation, or training AR flows.

## Skip If (ANY kills it)

- Fully-immersive VR with occluded headset — use vr-design-patterns.
- Mixed-reality productivity (passthrough Quest / Vision Pro) — use immersive-design-principles.
- Pure 2D mobile UI that only overlays a camera feed without spatial anchoring — standard mobile UX applies.
- Low-power smart glasses with no spatial tracking — different constraints (voice-first display-only).

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
