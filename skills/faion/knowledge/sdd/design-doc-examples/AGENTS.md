# Design Doc Examples

## Summary

**One-sentence:** Provide reusable worked design-doc examples (single-service, cross-service, migration, hot-path) that a writer copies and adapts rather than starts from a blank page.

**One-paragraph:** Most design-doc quality issues stem from blank-page paralysis. This methodology ships four canonical worked examples — single-service feature, cross-service refactor, data migration, hot-path performance work — each fully filled in with realistic content. Writers pick the closest match, copy the file, and edit; reviewers compare against the example. The examples are versioned so updates to the underlying design-doc-structure flow into all four at once.

**Ефективно для:**

- Engineer writing their first design doc on a new team — needs a worked example to anchor scope and depth.
- Reviewer who wants a baseline to compare against during async review.
- Solo agent generating a draft doc from spec + design-doc-structure — examples ground tone and detail level.
- Migration projects where the example saves an hour of structuring.

## Applies If (ALL must hold)

- Design-doc-structure methodology is in use as the canonical layout.
- The current design problem fits one of the four example archetypes.
- Writer can copy + adapt rather than build from scratch.
- Examples are versioned alongside the structure spec.

## Skip If (ANY kills it)

- Design problem is unique enough that no example archetype fits.
- Writer prefers blank-page authoring for style reasons.
- Doc is for an external audience (vendor RFP) where examples are too internal.
- Pre-discovery — no design problem yet to instantiate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| design-doc-structure spec | markdown | design-doc-structure output |
| Four worked examples | markdown | templates/ directory |
| Archetype selector | decision tree | This methodology |
| Spec.md + ADRs | markdown | Spec + ADR methodology outputs |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/design-doc-structure` | Layout the examples instantiate. |
| `solo/sdd/sdd-planning/design-doc-writing-process` | Writing flow the examples illustrate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-archetype` | haiku | Match input description to one of four archetypes. |
| `adapt-example` | sonnet | Substitute names, schemas, and metrics from the real spec. |
| `compare-and-feedback` | sonnet | Reviewer task — compare draft against example. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-doc-examples.json` | JSON skeleton conforming to the output contract schema. |
| `templates/design-doc-examples.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-doc-examples.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[design-doc-structure]]
- [[design-doc-writing-process]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
