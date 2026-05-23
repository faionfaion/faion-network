---
slug: ai-spatial-computing
tier: geek
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an XR accessibility spec with three-tier input fallback (gaze→voice→controller), on-device latency budget, and W3C XAUR gap analysis for AR/VR/MR products.
content_id: "3f4961426cd216d7"
complexity: deep
produces: spec
est_tokens: 4900
tags: [spatial-computing, ar, vr, xr-accessibility, ai-adaptation, xaur, gaze, on-device-ai]
---
# AI + Spatial Computing Accessibility

## Summary

**One-sentence:** Produces an XR accessibility spec with three-tier input fallback (gaze→voice→controller), on-device latency budget, and W3C XAUR gap analysis for AR/VR/MR products.

**One-paragraph:** Spatial interfaces (visionOS, Quest, HoloLens) generate eye/hand/voice/scene data that 2D UX patterns cannot handle. AI scene understanding reduces interaction steps, but cloud AI breaks the 20 ms comfort budget and LLM-generated XAUR audits frequently hallucinate clauses. This methodology produces an XR accessibility spec covering three-tier input fallback, on-device inference budget (<20 ms p95), opt-in environmental adaptation, biometric retention policy, and a human-on-hardware sign-off gate.

**Ефективно для:** інженера / a11y-спеціаліста, що готує XR продукт до релізу — XAUR-аудит + interaction-fallback-spec + privacy disclosures + human-on-hardware sign-off.

## Applies If (ALL must hold)

- Spec / design.md / PRD references gaze, eye tracking, hand tracking, dwell, spatial audio, scene anchoring, or passthrough.
- Target hardware is visionOS / Vision Pro / Quest 3 / HoloLens 2 / ARKit / ARCore / OpenXR.
- AI inference path is on-device and a p95 budget <20 ms applies to the interactive surface.
- Eye / face / hand / room-mesh capture in scope → privacy review required.

## Skip If (ANY kills it)

- Product targets only 2D web or mobile.
- No access to XR hardware for validation.
- Feature is non-real-time documentation generation only.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Target hardware name + OS version | string | hardware spec |
| Design.md or interaction spec under audit | markdown | product team |
| Sensor inventory (eye/hand/voice/mesh/face) | JSON | engineering |
| Latency budget per modality | JSON | engineering |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-assisted-accessibility]] | Baseline AI-augmented a11y workflow. |
| [[ai-accessibility-automation-2026]] | WCAG automation context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end. | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-spec` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/interaction-fallback-spec.md` | Markdown skeleton: surface + primary modality + tier-2 + tier-3 + dwell + retention + consent. |
| `templates/prompt-xaur-gap-analysis.txt` | Prompt asking agent for clause-by-clause XAUR gap analysis with confidence labels. |
| `templates/_smoke-test.md` | Filled minimum-viable spec for a single gaze→voice→controller surface. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-spatial-computing.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-assisted-accessibility]]
- [[ai-accessibility-automation-2026]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the spec; mis-routing leads to producing the wrong artefact shape.
