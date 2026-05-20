---
slug: spatial-ui-patterns
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A pattern taxonomy for 3D user interfaces in AR/VR/MR: four panel types (world-locked, head-locked, body-locked, hand-attached), window management conventions, and ergonomic constraints (comfort distance ≥ 1 m, FoV occupancy ≤ 40°, touch targets ≥ 60×60 pt at 1 m).
content_id: "74a68d691e50df2e"
tags: [spatial-ui, ar-vr-mr, panel-types, window-management, ergonomics]
---
# Spatial UI Patterns

## Summary

**One-sentence:** A pattern taxonomy for 3D user interfaces in AR/VR/MR: four panel types (world-locked, head-locked, body-locked, hand-attached), window management conventions, and ergonomic constraints (comfort distance ≥ 1 m, FoV occupancy ≤ 40°, touch targets ≥ 60×60 pt at 1 m).

**One-paragraph:** A pattern taxonomy for 3D user interfaces in AR/VR/MR: four panel types (world-locked, head-locked, body-locked, hand-attached), window management conventions, and ergonomic constraints (comfort distance ≥ 1 m, FoV occupancy ≤ 40°, touch targets ≥ 60×60 pt at 1 m). Default to world-locked for reference content and body-locked for primary UI. Head-locked UI is forbidden in visionOS and discouraged on Quest.

## Applies If (ALL must hold)

- Designing a visionOS, Quest, HoloLens, or Magic Leap app where 2D windowed metaphors are insufficient.
- Porting an existing 2D app to spatial computing — needs panel-type decisions and window-management rules.
- Authoring spatial design guidelines for a brand entering XR.
- Reviewing a third-party XR design for ergonomic, accessibility, and FoV risks.
- Building HUDs in games or industrial XR (training, telepresence, surgical planning).

## Skip If (ANY kills it)

- Pure phone or desktop products — spatial constructs add cognitive overhead.
- Simple 2D content shown inside a headset's flat-window mode (a Safari tab in visionOS) — standard responsive design rules apply.
- Prototyping at the storyboard stage where the platform is undecided.
- Static signage or passive AR overlays without interaction.

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
