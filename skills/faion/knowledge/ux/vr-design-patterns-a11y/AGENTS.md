# VR Design Patterns for Accessibility and Comfort

## Summary

**One-sentence:** Five canonical VR design patterns (snap-turn default, vignette, locomotion choice, hand-presence options, retreat affordance) emitted as a record.

**One-paragraph:** VR design without comfort + accessibility patterns reproduces the same nausea + exclusion every release. This methodology pins five canonical patterns and produces a VR-pattern record per experience validated against the schema.

**Ефективно для:**

- Snap-turn default eliminates the leading nausea cause.
- Vignette cuts simulator-sickness reports.
- Locomotion choice respects user preference.
- Hand-presence options accommodate motor differences.
- Retreat affordance treats exit as a right.

## Applies If (ALL must hold)

- Production VR experience under design.
- Sessions may exceed 5 minutes.
- Multiple interaction modalities present.

## Skip If (ANY kills it)

- Pure AR / MR — use `ar-design-patterns`.
- Single-scene tech demo with no production users.
- Comfort already specced via `immersive-design-principles` for the same experience.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Experience brief | Markdown | product |
| Platform | Quest / Vision / PSVR2 | platform |
| Locomotion plan | modes list | design |
| Interaction model | hand-tracking / controller / both | design |

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
| `templates/vr-pattern-record.json` | JSON skeleton for VR pattern record. |
| `templates/comfort-defaults.json` | Default comfort settings template. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vr-design-patterns.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[immersive-design-principles]]
- [[spatial-accessibility]]
- [[ar-design-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
