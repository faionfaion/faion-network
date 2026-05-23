---
slug: impl-plan-examples
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Ship reusable worked impl-plan examples (greenfield feature, multi-file refactor, data migration, infra change) so authors copy a realistic plan rather than building from scratch.
content_id: "933bb6d90e736131"
complexity: light
produces: report
est_tokens: 3500
tags: ["impl-plan", "examples", "templates", "worked-examples", "starter"]
---
# Impl Plan Examples

## Summary

**One-sentence:** Ship reusable worked impl-plan examples (greenfield feature, multi-file refactor, data migration, infra change) so authors copy a realistic plan rather than building from scratch.

**One-paragraph:** Impl-plan quality stalls when each author invents their own scope and depth. This methodology ships four worked impl-plan examples covering the most common archetypes: greenfield feature, multi-file refactor, data migration, infra change. Each example carries a full TASK list, token estimates, dependency graph, and acceptance criteria. Authors pick the closest archetype, copy, and adapt; reviewers compare against the example baseline.

**Ефективно для:**

- Engineer writing their first impl-plan; needs a worked example to calibrate scope.
- Reviewer comparing draft impl-plan against a known-good baseline.
- Agent generating impl-plan from spec.md + design.md; example anchors structure.
- Migration projects where the example saves an hour of TASK structuring.

## Applies If (ALL must hold)

- Writing-implementation-plans methodology is in use.
- The current change fits one of the four example archetypes.
- Author can copy + adapt rather than build from scratch.
- Examples are versioned alongside the impl-plan structure.

## Skip If (ANY kills it)

- Change is unique enough that no example archetype fits.
- Author prefers blank-page authoring.
- Pre-design — impl-plan would invent design that does not exist.
- Single-task work — no plan to structure.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| writing-implementation-plans output | markdown | Writing-impl-plan methodology |
| Four worked impl-plan examples | markdown | templates/ |
| Archetype selector | decision tree | This methodology |
| spec.md + design.md | markdown | Spec + Design methodology outputs |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/writing-implementation-plans` | Envelope these examples instantiate. |
| `solo/sdd/sdd-planning/impl-plan-task-format` | TASK shape used by every example. |

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
| `pick-archetype` | haiku | Match input to one of four archetypes. |
| `adapt-example` | sonnet | Substitute task names + token estimates. |
| `compare` | sonnet | Reviewer-side comparison. |

## Templates

| File | Purpose |
|------|---------|
| `templates/impl-plan-examples.json` | JSON skeleton conforming to the output contract schema. |
| `templates/impl-plan-examples.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-impl-plan-examples.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[writing-implementation-plans]]
- [[impl-plan-task-format]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
