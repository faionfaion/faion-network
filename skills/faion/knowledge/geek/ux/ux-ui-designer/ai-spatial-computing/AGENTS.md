---
slug: ai-spatial-computing
tier: geek
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Spatial interfaces generate complex contextual data that static UI rules cannot handle.
content_id: "3d69e4d4c74ec51f"
tags: [xr, spatial-computing, ar-vr-mr, ai-scene-understanding, gestural-ui]
---
# AI + Spatial Computing

## Summary

**One-sentence:** Spatial interfaces generate complex contextual data that static UI rules cannot handle.

**One-paragraph:** Spatial interfaces generate complex contextual data that static UI rules cannot handle. AI scene classification enables UIs to auto-adapt layouts, pre-position relevant content, and anticipate user intent — reducing interaction friction in environments where traditional 2D patterns fail. Without explicit AI fallback design, failures in scene understanding or gesture prediction degrade UX to zero.

## Applies If (ALL must hold)

- Designing XR (AR/VR/MR) interfaces that must adapt to physical environment context
- Building AI-driven spatial UI that pre-positions content based on scene understanding
- Generating spatial layout specifications for Apple Vision Pro, Meta Quest, or WebXR targets
- Auditing existing spatial UI for contextual awareness gaps
- Prototyping voice + gesture interaction flows for 3D environments

## Skip If (ANY kills it)

- Standard 2D web/mobile UI — spatial computing overhead adds no value
- Early concept validation — spatial UX requires hardware to meaningfully test
- Budget-constrained projects where XR hardware deployment is not planned
- Contexts where latency is unacceptable — AI scene understanding adds 50–200ms

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

- parent skill: `geek/ux/ux-ui-designer/`
