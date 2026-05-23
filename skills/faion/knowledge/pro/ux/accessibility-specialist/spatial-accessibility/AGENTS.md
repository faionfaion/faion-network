---
slug: spatial-accessibility
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Accessibility rules for XR (VR/AR/MR) spatial UI: reach zones, height variability, occlusion, spatial audio, seated alternates.
content_id: "8d374cd2f443bf36"
complexity: medium
produces: report
est_tokens: 4100
tags: [spatial, xr, vr, ar, a11y]
---
# Spatial Accessibility in XR Interfaces

## Summary

**One-sentence:** Accessibility rules for XR (VR/AR/MR) spatial UI: reach zones, height variability, occlusion, spatial audio, seated alternates.

**One-paragraph:** Spatial UI introduces new exclusion vectors: out-of-reach controls, height assumptions, occluding panels, missing spatial-audio cues, standing-only flows. This methodology pins five spatial-accessibility rules and emits a per-experience spatial-a11y record.

**Ефективно для:**

- Reach zones documented so panels work for short / tall / seated users.
- Occlusion budget keeps critical info visible.
- Spatial audio doubles as a directional cue for blind users.
- Seated alternates remove standing-only exclusion.

## Applies If (ALL must hold)

- XR experience with persistent spatial UI panels.
- Seated + standing users in scope.
- Multiple user heights expected.

## Skip If (ANY kills it)

- Pure flat-screen — use `accessibility-first-design`.
- Single-pose tech demo with no production users.
- AR-only with no persistent panels — use `ar-design-patterns`.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Experience brief | Markdown | product |
| Reach zone matrix | near/mid/far layout | design |
| Locomotion + seating model | string | design |
| Audio plan | channel + spatial schema | audio |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| a11y-basics | Provides WCAG POUR / conformance vocabulary used across the accessibility-specialist domain. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with sourced rationale + skip-this-methodology + run-the-checklist | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure (input / action / output / decision-gate) | 800 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs (preconditions, severity, modality) to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `triage-inputs` | haiku | Mechanical scrape from inputs. |
| `apply-rules` | sonnet | Per-rule judgement on inputs. |
| `synthesise-artefact` | sonnet | Aggregates rule outcomes into the final artefact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spatial-accessibility-record.json` | JSON skeleton matching the schema. |
| `templates/xr-scene-audit.py` | Stdlib helper to scan a scene JSON for reach-zone + occlusion violations. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spatial-accessibility.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[vr-design-patterns]]
- [[ar-design-patterns]]
- [[immersive-design-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
