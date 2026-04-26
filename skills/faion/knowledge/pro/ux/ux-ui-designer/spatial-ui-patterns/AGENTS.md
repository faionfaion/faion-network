# Spatial UI Patterns

## Summary

A pattern taxonomy for 3D user interfaces in AR/VR/MR: four panel types (world-locked, head-locked, body-locked, hand-attached), window management conventions, and ergonomic constraints (comfort distance ≥ 1 m, FoV occupancy ≤ 40°, touch targets ≥ 60×60 pt at 1 m). Default to world-locked for reference content and body-locked for primary UI. Head-locked UI is forbidden in visionOS and discouraged on Quest.

## Why

2D UI metaphors (fixed pixel position, z-index stacking, cursor pointer) do not translate to 3D space. Each panel type has different ergonomic, accessibility, and persistence tradeoffs. Choosing the wrong type causes discomfort (arm fatigue, vergence-accommodation conflict), failed platform review (Apple HIG, Meta VRC.PC.UX), and poor UX. The taxonomy provides a decision framework that maps to each platform's native scene model.

## When To Use

- Designing a visionOS, Quest, HoloLens, or Magic Leap app where 2D windowed metaphors are insufficient.
- Porting an existing 2D app to spatial computing — needs panel-type decisions and window-management rules.
- Authoring spatial design guidelines for a brand entering XR.
- Reviewing a third-party XR design for ergonomic, accessibility, and FoV risks.
- Building HUDs in games or industrial XR (training, telepresence, surgical planning).

## When NOT To Use

- Pure phone or desktop products — spatial constructs add cognitive overhead.
- Simple 2D content shown inside a headset's flat-window mode (a Safari tab in visionOS) — standard responsive design rules apply.
- Prototyping at the storyboard stage where the platform is undecided.
- Static signage or passive AR overlays without interaction.

## Content

| File | What's inside |
|------|---------------|
| `content/01-panel-types.xml` | Four panel types, ergonomic rules, window management, DO/DON'T constraints |
| `content/02-agent-patterns.xml` | Agent scene-scaffold workflow, subagent roles, prompt patterns, platform gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/SpatialApp.swift` | Minimal visionOS scene scaffold with WindowGroup, Volume, and ImmersiveSpace |

## Scripts

none
