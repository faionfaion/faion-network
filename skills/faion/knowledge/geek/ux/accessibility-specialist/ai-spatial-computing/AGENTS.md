---
slug: ai-spatial-computing
tier: geek
group: ux
domain: accessibility-specialist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AI enables spatial interfaces (AR/VR/MR) to adapt contextually — recognizing environments, predicting gestures, routing voice commands, and powering gaze-based accessibility.
content_id: "3d69e4d4c74ec51f"
tags: [spatial-computing, ar, vr, xr-accessibility, ai-adaptation, xaur, gaze, on-device-ai]
---
# AI + Spatial Computing

## Summary

**One-sentence:** AI enables spatial interfaces (AR/VR/MR) to adapt contextually — recognizing environments, predicting gestures, routing voice commands, and powering gaze-based accessibility.

**One-paragraph:** AI enables spatial interfaces (AR/VR/MR) to adapt contextually — recognizing environments, predicting gestures, routing voice commands, and powering gaze-based accessibility. This methodology covers AI-driven contextual UI adaptation, W3C XAUR accessibility gap analysis for XR apps, and privacy architecture for biometric/spatial data collection. It gives the agent concrete WHEN triggers, a step-by-step audit checklist, ready-to-paste LLM prompts, an interaction-spec template, CLI commands for measuring on-device inference latency, and a verification procedure that ends with a human-on-hardware sign-off gate.

## Applies If (ALL must hold)

- Trigger: user input mentions visionOS, Vision Pro, Quest, Quest 3, HoloLens, ARCore, ARKit, RealityKit, OpenXR, Unity Sentis, or "XR/AR/VR/MR accessibility"
- Trigger: a spec, design.md, or PRD references gaze, eye tracking, hand tracking, dwell selection, spatial audio, scene anchoring, or passthrough
- Trigger: a ticket asks for an XAUR audit, accessibility gap analysis, or accessibility-conformance report on a spatial product
- Trigger: code under review includes
- Trigger: AI-driven contextual UI adaptation (environment-aware UX) is being added to a spatial application
- Trigger: privacy review or DPIA for a product that captures eye, face, hand, room scan, or biometric data
- Trigger: ML latency target is being defined for an interactive XR feature (must be

## Skip If (ANY kills it)

- Product targets only 2D web or mobile — spatial patterns add unnecessary complexity
- No access to XR hardware for validation — AI-generated spatial UX without device testing is unreliable
- Real-time AI inference cannot meet the <20ms threshold — on-device AI is mandatory here
- Budget and timeline do not support specialized XR accessibility testing
- Feature is non-real-time documentation generation only (e.g. VPAT drafting) — use the generic accessibility-audit methodology instead

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

- parent skill: `geek/ux/accessibility-specialist/`
