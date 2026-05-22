---
slug: spatial-computing-overview
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Spatial computing blends digital content with physical space through AR, VR, and MR.
content_id: "010b8c61801ce015"
tags: [spatial-computing, ar, vr, mr, xr, visionos, android-xr, quest, platform-selection]
---
# Spatial Computing Overview: Platform Landscape and Selection Workflow (2026)

## Summary

**One-sentence:** Spatial computing blends digital content with physical space through AR, VR, and MR.

**One-paragraph:** Spatial computing blends digital content with physical space through AR, VR, and MR. This methodology gives an autonomous agent a concrete, paste-ready workflow to evaluate the 2026 platform landscape and produce a defensible platform-selection recommendation in a single pass.

## Applies If (ALL must hold)

- User asks: "Which XR/AR/VR/spatial platform should we build on?"
- User asks for a "spatial app", "Vision Pro app", "Quest app", "AR app", "MR app", or "headset app" without naming the platform.
- Task involves designing or scoping a new application targeting head-mounted displays (HMDs) in 2025/2026.
- Evaluating market opportunity, install base, or ecosystem before committing to an SDK.
- Planning a multiplatform XR strategy (e.g. WebXR + native + Unity).
- Translating a 2D mobile/web product to a spatial modality.

## Skip If (ANY kills it)

- Optimizing existing 2D mobile/desktop applications — use standard mobile or desktop UX methodologies.
- Projects with no XR/AR/VR component or vision — this overview is not applicable.
- Pre-2024 legacy VR knowledge tasks — platforms and guidelines (visionOS, Horizon OS, Android XR) have changed; consult vendor docs directly.
- Internal hack-week prototypes with no commercial intent — the platform-selection overhead exceeds the value.
- Hardware engineering questions (optics, SLAM, compute) — out of scope; consult hardware specs.

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
