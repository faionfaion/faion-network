# Spatial UX Fundamentals

## Summary

Spatial UX organizes content in three physical zones: near field (0–1 m, primary interactions and controls), mid field (1–3 m, content consumption and work surfaces), far field (3 m+, ambient context and navigation aids). Interactive controls must never be placed in the far field. Use 1.5–2.0 m as default content distance. Provide a recenter affordance. Test seated AND standing — comfortable reach shifts ~15°.

## Why

2D UI patterns do not translate to 3D spatial interfaces: a button at screen-bottom works on a phone but falls in the chin-fatigue zone on a headset. Field zones enforce ergonomic constraints derived from human-factors research on head-mounted displays. Skipping them produces layouts that users cannot comfortably reach or sustain, causing abandonment after minutes of use.

## When To Use

- Drafting first-pass UX requirements for Apple Vision Pro, Meta Quest, or HoloLens apps.
- Re-mapping a 2D mobile or desktop flow into near/mid/far field zones.
- Reviewing a spatial layout for reach, occlusion, sight-line, and orientation issues.
- Establishing shared spatial vocabulary across PM, engineering, and 3D teams.

## When NOT To Use

- Phone AR snap-on features (banner overlays) — world-scale and reach constraints don't apply meaningfully.
- Desktop 3D viewers (CAD, Blender) — different ergonomic constraints than head-mounted spatial.
- 360-degree video lean-back content — viewer is passive; no reach or occlusion design is needed.

## Content

| File | What's inside |
|------|---------------|
| `content/01-field-zones.xml` | Near/mid/far zone definitions, anchoring types, occlusion rules, sight-line rules. |
| `content/02-antipatterns-and-workflow.xml` | Common spatial antipatterns, agentic workflow, lint spec, agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spatial-spec-linter.py` | Validate JSON spatial spec: flag elements outside correct distance bands or interactive controls in far field. |
