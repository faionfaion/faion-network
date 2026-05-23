# AR Design Patterns

## Summary

**One-sentence:** Accessible AR (augmented-reality) design patterns: anchor stability, environment-aware contrast, dwell vs gaze input, audio cues, motion budgets.

**One-paragraph:** AR overlays graphics on the real world, so accessibility constraints differ from flat UI: anchor stability against device drift, environment-aware contrast (sun, indoor, dark), dwell + gaze input alternates for hand-tracking, spatial audio cues for blind users, and motion budgets to avoid simulator sickness. This methodology pins five canonical AR patterns and emits an AR-pattern decision record per component.

**Ефективно для:**

- Anchor stability spec prevents 'jittering UI' a11y reports.
- Environment-aware contrast policy works in sun + dark.
- Dwell + gaze alternate avoids fatigue-induced exclusion.
- Motion-budget rule keeps simulator-sickness reports low.

## Applies If (ALL must hold)

- Designing an AR component or HUD.
- Mixed environments (indoor + outdoor) expected.
- Multiple input modalities present.

## Skip If (ANY kills it)

- Pure VR — use `vr-design-patterns`.
- Flat 2D mobile — use standard `accessibility-first-design`.
- Lab-only research demo with no production users.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| AR runtime | ARKit / ARCore / WebXR | platform |
| Component brief | what the AR UI is doing | product |
| Environment scope | indoor / outdoor / mixed | research |
| Input modalities | hand-tracking / gaze / controller / touch | platform |

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
| `templates/ar-pattern-record.json` | JSON skeleton for the AR-pattern record. |
| `templates/ar-anchor-schema.json` | Anchor metadata schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ar-design-patterns.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[vr-design-patterns]]
- [[spatial-accessibility]]
- [[immersive-design-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
