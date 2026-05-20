---
slug: spatial-ui-patterns
tier: pro
group: ux
domain: ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Panel anchoring, window management, and interaction rules for 3D/XR interfaces (visionOS, Meta Horizon OS, HoloLens, Android XR).
content_id: "74a68d691e50df2e"
tags: [spatial-ui, xr, panel-anchoring, window-management, visionos]
---
# Spatial UI Patterns

## Summary

**One-sentence:** Panel anchoring, window management, and interaction rules for 3D/XR interfaces (visionOS, Meta Horizon OS, HoloLens, Android XR).

**One-paragraph:** Panel anchoring, window management, and interaction rules for 3D/XR interfaces (visionOS, Meta Horizon OS, HoloLens, Android XR). Four anchor types — world-locked, head-locked, body-locked, hand-attached — each with distinct use cases, ergonomic constraints, and platform-specific APIs.

## Applies If (ALL must hold)

- Designing UI for visionOS, Meta Quest/Horizon OS, HoloLens, Magic Leap 2, or Android XR.
- Porting 2D apps to spatial environments and choosing panel anchoring strategy.
- Defining window-management rules (snap, group, dock, spatial recall).
- Reviewing existing XR UIs for fatigue, near-field clutter, or FOV violations.

## Skip If (ANY kills it)

- 2D mobile/desktop UIs — patterns assume 3D positioning and head/hand tracking.
- Handheld AR (ARKit on iPhone) — different interaction model; anchoring rules diverge.
- VR-only games with bespoke diegetic UI — system patterns may conflict with game fiction.

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
