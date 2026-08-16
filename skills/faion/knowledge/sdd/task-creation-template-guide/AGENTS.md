# Task Creation Template Guide

## Summary

**One-sentence:** Step-by-step guide to filling the TASK template (front-matter + five-section body) for a new implementation task without inventing fields or skipping required content.

**One-paragraph:** Authors fill TASK files inconsistently when the template is left as silent skeleton: required fields skipped, optional fields invented, body sections mis-ordered. This methodology gives a step-by-step fill guide aligned with impl-plan-task-format: front-matter first (id/est_tokens/depends_on/owner/component), then body in fixed order (Goal, Inputs, Steps, Acceptance, Notes). Each step lists what to copy from upstream docs and what to write fresh.

**Ефективно для:**

- Solo founder authoring their first dozen TASKs; needs a step-by-step.
- Agent drafting TASK from spec + design; guide anchors structure.
- Reviewer scanning TASKs for completeness; guide is the rubric.
- Onboarding new collaborators to the TASK convention.

## Applies If (ALL must hold)

- impl-plan-task-format is the canonical TASK shape.
- templates/TASK_skeleton.md is available.
- Author can copy from upstream spec + design.md.
- TASKs are filed in TASK_*.md format.

## Skip If (ANY kills it)

- TASKs live in external tracker — different fill process.
- Single-line TASK — overhead exceeds benefit.
- Pre-impl-plan — no TASK template needed.
- Author already fluent; check task-creation-principles rubric instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| templates/TASK_skeleton.md | markdown | This methodology |
| impl-plan-task-format spec | markdown | impl-plan-task-format |
| spec.md + design.md | markdown | Spec + Design methodologies |
| Component map | list | impl-plan-components |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/impl-plan-task-format` | TASK shape this guide fills. |
| `solo/sdd/sdd-planning/task-creation-principles` | Principles validated post-fill. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `fill-step` | sonnet | Per-step content drafting. |
| `lint-fill` | haiku | Deterministic field-presence check. |
| `review-task` | sonnet | Reviewer pass after fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/task-creation-template-guide.json` | JSON skeleton conforming to the output contract schema. |
| `templates/task-creation-template-guide.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/task-creation-template-guide.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/task-creation-template-guide.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/task-template.md.j2` | Fully worked TASK_XXX skeleton (metadata, dependency tree, requirements coverage, out of scope, goals, acceptance criteria, risks, testing, implementation log, lessons learned) demonstrating the fill order this guide teaches. |
| `templates/task-template.md` | Fully worked TASK_XXX skeleton (metadata, dependency tree, requirements coverage, out of scope, goals, acceptance criteria, risks, testing, implementation log, lessons learned) demonstrating the fill order this guide teaches. Generated from `templates/task-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-task-creation-template-guide.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[impl-plan-task-format]]
- [[task-creation-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/task-creation-template-guide.json`

```json
{
  "artefact_id": "task-creation-template-guide-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "task_id": "task_id value",
  "fill_steps_completed": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "rubric_score": 1,
  "sections_present": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "component_in_map": true,
  "owner": "@solo-founder"
}
```
