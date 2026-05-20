---
slug: spatial-accessibility
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for designing AR/VR/MR interfaces that work across motor, visual, cognitive, and motion-sensitivity differences.
content_id: "cce0eeb046ffb47f"
tags: [spatial-computing, accessibility, xr, aria, input-modalities]
---
# Spatial Accessibility

## Summary

**One-sentence:** A methodology for designing AR/VR/MR interfaces that work across motor, visual, cognitive, and motion-sensitivity differences.

**One-paragraph:** A methodology for designing AR/VR/MR interfaces that work across motor, visual, cognitive, and motion-sensitivity differences. Every spatial interaction must support at least two input modalities and have a non-spatial fallback. Seated-mode parity is mandatory — if an interaction requires standing or arm-raising, a seated alternative must be documented.

## Applies If (ALL must hold)

- Designing AR/VR/MR experiences on Vision Pro, Quest, PS VR2, HoloLens, or WebXR.
- Adapting an existing flat UI for a spatial platform — need seated mode, gaze fallback, motion-comfort settings.
- Submitting an app to App Store or Meta Horizon Store.
- Designing enterprise XR (industrial training, medical) where injury risk is non-zero.

## Skip If (ANY kills it)

- 2D mobile/desktop apps — use standard WCAG 2.2 / mobile a11y; spatial tradeoffs do not apply.
- Pure passthrough video apps with no UI overlay — accessibility reduces to standard video a11y (captions, contrast).
- Throwaway VR demos for a single internal user — full spatial-a11y program is overkill before validation.

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
