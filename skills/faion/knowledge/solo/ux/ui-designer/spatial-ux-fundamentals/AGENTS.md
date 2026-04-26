# Spatial UX Fundamentals

## Summary

Design principles for 3D/XR interfaces: place UI elements in near (0-1m), mid (1-3m), and far (3m+) field zones; specify element sizes in world units (meters) at placement distance; assign interaction modalities per platform constraints; and validate every layout in a physical headset before development begins.

## Why

2D UI patterns — pixel sizing, flat navigation, pointer interaction — do not transfer to 3D space. Placing content outside comfort zones (above eye level, below 0.5m, in peripheral blind spots) causes neck strain, vergence-accommodation conflict, and motion sickness. Text and touch targets must meet minimum visual angle requirements that vary with placement distance, not screen resolution.

## When To Use

- Designing UI for Apple Vision Pro, Meta Quest, or other XR headsets
- Planning spatial layout of panels, menus, and work surfaces in a 3D environment
- Auditing an existing XR app for ergonomic violations
- Specifying spatial interaction patterns for a development team new to XR
- Creating documentation for a spatial design system (scale, reach zones, field-of-view constraints)

## When NOT To Use

- Flat 2D web or mobile interfaces — spatial principles introduce unnecessary complexity
- Early product ideation before target hardware is confirmed — comfort zones vary across headsets
- Accessibility audits without XR-specific assistive technology expertise
- When the development team has no XR SDK experience — specs cannot be implemented without platform capability

## Content

| File | What's inside |
|------|---------------|
| `content/01-spatial-rules.xml` | Near/mid/far field zones, element sizing in world units, comfort zone angular limits, interaction modality assignments per platform, ergonomic risk rules |

## Templates

none

## Scripts

| File | Purpose |
|------|---------|
| `scripts/spatial-comfort.py` | Computes minimum element size and interaction target size at a given placement distance and visual angle |
