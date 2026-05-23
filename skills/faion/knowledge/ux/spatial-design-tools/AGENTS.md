# Spatial Design Tools

## Summary

**One-sentence:** Produces a phase-gated tool-selection config for spatial (AR/VR/MR) workflows: concept in Figma + ShapesXR, prototype in Unity or Unreal, production in engine; with asset-pipeline standards (USD/USDZ for visionOS, glTF for Quest/Web) and polygon + file-size budgets set at concept stage.

**One-paragraph:** Spatial product teams routinely pick the wrong tool for the wrong phase: hi-fi 3D in Figma before validation, screenshot-driven design after engine onboarding. This methodology declares a phase-gated tool stack per project type. Concept = Figma + ShapesXR (cheap iteration). Prototype = Unity or Unreal (in-engine playable). Production = same engine plus USD/USDZ for visionOS or glTF for Quest / WebXR. Asset-budget constraints (polygon count, file size, draw calls) are set during concept stage, not after artist work is done. Output is a config artefact consumed by engineering for project bootstrap.

**Ефективно для:**

- Pre-prototype tool selection: Figma + ShapesXR vs Unity/Unreal vs USD authoring.
- Standardizing asset format (USD/USDZ for visionOS, glTF for Quest/WebXR).
- Setting polygon + file-size + draw-call budgets at concept stage, not after artist work.
- Cross-team tool-stack alignment між design + engineering + 3D artists.

## Applies If (ALL must hold)

- New spatial product is being scoped or restarted at the prototype stage.
- Multi-platform target requires consistent asset pipeline (visionOS + Quest + WebXR).
- 3D artists and engineers need a shared tool contract before content production starts.

## Skip If (ANY kills it)

- Single-engine team with established pipeline — overhead exceeds payoff.
- Pure passthrough video apps without 3D content.
- Internal hackweek experiments where tool churn is acceptable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Project type | enum: concept|prototype|production | PM |
| Target platforms | list | PM |
| 3D artist roster + tools | list | art director |
| Asset budget targets | JSON | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[spatial-computing-overview]] | platform decision precedes tool selection |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: phase-gated-tools, asset-format-by-platform, budget-at-concept, engine-choice-explicit, in-engine-prototype | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-phase` | haiku | Mechanical enum pick. |
| `pick-tool-stack` | sonnet | Light judgment on team skill + target match. |
| `set-budgets` | sonnet | Reasoning over platform docs. |
| `validate` | haiku | Mechanical schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-stack-config.json` | Skeleton config artefact |
| `templates/spatial-budget.sh` | Asset-budget enforcement script for CI |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spatial-design-tools.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[spatial-computing-overview]]
- [[spatial-ux-fundamentals]]
- [[spatial-ui-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on project phase first; in prototype/production it splits on whether visionOS is in the platform list (forcing USDZ alongside glTF). Budgets-set check fires on any leaf. Each leaf cites a rule from `01-core-rules.xml`.
