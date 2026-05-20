---
slug: vr-design-patterns
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: User-centered VR design starts with comfort: place a visible ground plane and stable horizon, choose teleportation-first locomotion for novices, anchor UI to the world (not the head), and provide accessibility fallbacks including seated modes, subtitles, and one-handed control.
content_id: "6543f00fc9abea0c"
tags: [vr, immersive, ux-design, interaction-design, comfort]
---
# VR Design Patterns

## Summary

**One-sentence:** User-centered VR design starts with comfort: place a visible ground plane and stable horizon, choose teleportation-first locomotion for novices, anchor UI to the world (not the head), and provide accessibility fallbacks including seated modes, subtitles, and one-handed control.

**One-paragraph:** User-centered VR design starts with comfort: place a visible ground plane and stable horizon, choose teleportation-first locomotion for novices, anchor UI to the world (not the head), and provide accessibility fallbacks including seated modes, subtitles, and one-handed control.

## Applies If (ALL must hold)

- Fully-immersive Quest, Vision Pro, Pico, Index, Vive deployments.
- Designing locomotion, in-VR menus, hand-tracking interactions, or seated/room-scale modes.
- Migrating a 2D enterprise tool (training, collaboration, design review) to a VR-native experience.
- Specifying comfort defaults and accessibility fallbacks for a VR build.

## Skip If (ANY kills it)

- AR / passthrough / MR-first apps — use ar-design-patterns and immersive-design-principles instead.
- 360° video viewers without interaction — patterns over-engineer the experience.
- Web-based WebXR demos with less than 2 minutes target session — most patterns assume sustained presence.

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
