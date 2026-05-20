---
slug: spatial-ux-fundamentals
tier: solo
group: ux
domain: ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design principles for 3D/XR interfaces: place UI elements in near (0-1m), mid (1-3m), and far (3m+) field zones; specify element sizes in world units (meters) at placement distance; assign interaction modalities per platform constraints; and validate every layout in a physical headset before development begins.
content_id: "845db2e8bdce2a5f"
tags: [xr, spatial-design, ergonomics, 3d-ui, vision-pro]
---
# Spatial UX Fundamentals

## Summary

**One-sentence:** Design principles for 3D/XR interfaces: place UI elements in near (0-1m), mid (1-3m), and far (3m+) field zones; specify element sizes in world units (meters) at placement distance; assign interaction modalities per platform constraints; and validate every layout in a physical headset before development begins.

**One-paragraph:** Design principles for 3D/XR interfaces: place UI elements in near (0-1m), mid (1-3m), and far (3m+) field zones; specify element sizes in world units (meters) at placement distance; assign interaction modalities per platform constraints; and validate every layout in a physical headset before development begins.

## Applies If (ALL must hold)

- Designing UI for Apple Vision Pro, Meta Quest, or other XR headsets
- Planning spatial layout of panels, menus, and work surfaces in a 3D environment
- Auditing an existing XR app for ergonomic violations
- Specifying spatial interaction patterns for a development team new to XR
- Creating documentation for a spatial design system (scale, reach zones, field-of-view constraints)

## Skip If (ANY kills it)

- Flat 2D web or mobile interfaces — spatial principles introduce unnecessary complexity
- Early product ideation before target hardware is confirmed — comfort zones vary across headsets
- Accessibility audits without XR-specific assistive technology expertise
- When the development team has no XR SDK experience — specs cannot be implemented without platform capability

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

- parent skill: `solo/ux/ui-designer/`
