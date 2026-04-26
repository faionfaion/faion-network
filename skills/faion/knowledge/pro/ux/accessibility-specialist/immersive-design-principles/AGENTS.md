# Immersive Design Principles

## Summary

A framework for XR/AR/VR/MR experience design covering immersion-level selection (passthrough, blended, fully immersive, portal), motion-comfort mitigations (vignette, snap turn, teleport, grounding), comfort settings completeness, spatial layout rules, and WAI XAUR accessibility coverage. Default every new experience to highest-comfort settings; let users opt into lower comfort.

## Why

Poor immersive design causes motion sickness, disorientation, fatigue, and safety issues that drive users to abandon a session and not return. Visual-vestibular mismatch is the primary failure mode — it is caused by smooth locomotion without a stable reference frame, frame rates below 90 FPS, or latency above 20 ms. Accessibility omissions (no seated mode, no captions, no voice commands) exclude large user populations and violate WAI XAUR.

## When To Use

- Designing or auditing VR/AR/MR/passthrough experiences across Meta Quest, Apple Vision Pro, PSVR2, PICO, HoloLens.
- Choosing the right immersion level for a use case.
- Reviewing comfort settings, locomotion, grounding, and motion-sickness mitigations before user testing.
- Making spatial UIs accessible across vision, hearing, mobility, and cognitive needs.

## When NOT To Use

- Pure 2D web/mobile work — use `wcag-22-compliance` and `a11y-basics` instead.
- Hardware/optics tuning (IPD, lens distortion) — those live in the engine/SDK layer.
- Game-feel tuning where intentional motion sickness is a deliberate design choice.
- Conversion-rate optimization for XR storefronts — adjacent topic, not this skill.

## Content

| File | What's inside |
|------|---------------|
| `content/01-immersion-levels.xml` | Four immersion levels, depth/layering, motion physics, smooth transitions |
| `content/02-comfort-and-safety.xml` | Motion comfort, visual/audio/interaction settings, grounding, scale, performance floors |
| `content/03-accessibility.xml` | Vision, hearing, mobility, cognitive accessibility in XR; WAI XAUR compliance |

## Templates

| File | Purpose |
|------|---------|
| `templates/comfort-settings.json` | Default comfort-settings schema for XR experiences (locomotion, visual, audio, interaction) |
