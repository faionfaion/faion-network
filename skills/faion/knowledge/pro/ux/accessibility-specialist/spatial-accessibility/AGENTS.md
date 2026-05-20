---
slug: spatial-accessibility
tier: pro
group: ux
domain: accessibility-specialist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Accessibility methodology for spatial/XR interfaces (Apple Vision Pro, Meta Quest, HoloLens, WebXR) addressing motor limitations, visual and hearing impairment, cognitive load, and motion sensitivity.
content_id: "cce0eeb046ffb47f"
tags: [xr, accessibility, spatial, wcag, inclusive-design]
---
# Spatial Accessibility in XR Interfaces

## Summary

**One-sentence:** Accessibility methodology for spatial/XR interfaces (Apple Vision Pro, Meta Quest, HoloLens, WebXR) addressing motor limitations, visual and hearing impairment, cognitive load, and motion sensitivity.

**One-paragraph:** Accessibility methodology for spatial/XR interfaces (Apple Vision Pro, Meta Quest, HoloLens, WebXR) addressing motor limitations, visual and hearing impairment, cognitive load, and motion sensitivity. Core requirements: multiple simultaneous input modalities (gaze + voice + controller + hand), seated mode as the default, 3D captions that face the user, spatial audio navigation for blind users, and alignment with W3C XR Accessibility User Requirements (XAUR).

## Applies If (ALL must hold)

- Designing or shipping for Apple Vision Pro, Meta Quest, HoloLens, Android XR, or WebXR.
- Adding accessibility features to an existing XR application pre-release.
- Auditing an immersive product against W3C XAUR.
- Enterprise XR (training, digital twins, remote assist) where ADA Title II or EAA may apply.
- Adding alternative input modalities to a single-modality XR experience.

## Skip If (ANY kills it)

- 2D web/mobile a11y — use `a11y-testing` and WCAG 2.2 AA.
- Game-only experiences where motion is core gameplay — apply selectively to menus and settings only.
- Internal R&D prototypes never seen by real users.
- Where the platform's built-in a11y settings fully address user needs without custom work.

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
