# VR Design Patterns

## Summary

Design patterns for fully-immersive 6DoF VR covering environment anchoring (ground plane, horizon, stable reference objects), locomotion menu (teleport default + smooth opt-in), UI placement (world-locked or body-locked, 1.5-3 m, eye-level, no head-lock), comfort settings (vignette, snap turn, FOV cap, seated mode), and accessibility parity across disability categories. Minimum 14-16 pt text, 90 FPS / 20 ms motion-to-photon, teleport-as-default.

## Why

Head-locked UI causes immediate nausea; smooth locomotion without teleport excludes wheelchair users and motion-sensitive users; no seated mode excludes a large population; text below 14 pt is unreadable even at 4K per eye. These are common mistakes that ship repeatedly because agents and developers default to web/mobile conventions. Teleport-first defaults and world-locked UI solve the most frequent failure modes.

## When To Use

- Designing fully-immersive VR experiences (Quest 2/3/Pro, PSVR2, Valve Index, PICO 4, Vision Pro full-immersion mode).
- Choosing locomotion and UI placement strategy.
- Implementing comfort settings: vignette, snap turn, FOV cap, seated mode, height calibration.
- Auditing an existing VR title for accessibility and motion-sickness risk.

## When NOT To Use

- AR/passthrough/MR — use `ar-design-patterns` and `immersive-design-principles` instead.
- 360-degree video in Cardboard-style viewers — constrained interaction, not 6DoF.
- Mixed-reality productivity with passthrough — use `immersive-design-principles` blended-mode territory.
- WebXR mobile sessions where 90 FPS is unreachable.

## Content

| File | What's inside |
|------|---------------|
| `content/01-environment.xml` | Ground plane, horizon, scale, lighting, boundaries, grounding rules |
| `content/02-locomotion-and-ui.xml` | Locomotion types with comfort ratings, UI placement rules, gaze + confirm, spatial audio |
| `content/03-accessibility.xml` | Vision, hearing, mobility, cognitive disability patterns; interaction alternatives |

## Templates

| File | Purpose |
|------|---------|
| `templates/comfort-defaults.json` | Comfort-defaults JSON schema for VR (locomotion, turn, comfort, UI, accessibility, performance) |
