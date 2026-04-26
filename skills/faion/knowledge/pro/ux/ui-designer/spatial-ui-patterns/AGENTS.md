# Spatial UI Patterns

## Summary

Panel anchoring, window management, and interaction rules for 3D/XR interfaces (visionOS, Meta Horizon OS, HoloLens, Android XR). Four anchor types — world-locked, head-locked, body-locked, hand-attached — each with distinct use cases, ergonomic constraints, and platform-specific APIs.

## Why

Traditional 2D components break in 3D space: wrong anchor choice causes arm fatigue, FOV violations, or interaction conflicts. Explicit anchor rules and comfort checks (distance 0.5-2 m, eccentricity ≤30°, touch target ≥4 cm) prevent the most common failures before prototyping.

## When To Use

- Designing UI for visionOS, Meta Quest/Horizon OS, HoloLens, Magic Leap 2, or Android XR.
- Porting 2D apps to spatial environments and choosing panel anchoring strategy.
- Defining window-management rules (snap, group, dock, spatial recall).
- Reviewing existing XR UIs for fatigue, near-field clutter, or FOV violations.

## When NOT To Use

- 2D mobile/desktop UIs — patterns assume 3D positioning and head/hand tracking.
- Handheld AR (ARKit on iPhone) — different interaction model; anchoring rules diverge.
- VR-only games with bespoke diegetic UI — system patterns may conflict with game fiction.

## Content

| File | What's inside |
|------|---------------|
| `content/01-anchor-types.xml` | Four anchor types with rules, ergonomic constraints, and platform notes. |
| `content/02-window-management.xml` | Snap, group, dock, spatial-memory rules and antipatterns. |
| `content/03-comfort-and-gotchas.xml` | Comfort envelope rules, AI-agent gotchas, accessibility gaps. |

## Templates

| File | Purpose |
|------|---------|
| `templates/comfort-check.ts` | TypeScript function that flags panels outside the ergonomic envelope. |
| `templates/panel-classifier-prompt.txt` | Prompt for a panel-classifier subagent (world/head/body/hand). |
