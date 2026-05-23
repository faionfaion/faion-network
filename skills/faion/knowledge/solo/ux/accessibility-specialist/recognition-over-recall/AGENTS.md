---
slug: recognition-over-recall
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Nielsen Heuristic #6 applied: minimise the user's memory load by making objects, actions, and options visible — recognising a label is easier than recalling it from a prior screen.
content_id: "c767d6692d17824a"
complexity: medium
produces: rubric
est_tokens: 3500
tags: [usability-heuristic, cognition, ux, memory-load, accessibility]
---
# Recognition Rather Than Recall

## Summary

**One-sentence:** Nielsen Heuristic #6 applied: minimise the user's memory load by making objects, actions, and options visible — recognising a label is easier than recalling it from a prior screen.

**One-paragraph:** Nielsen Heuristic #6 applied: minimise the user's memory load by making objects, actions, and options visible — recognising a label is easier than recalling it from a prior screen. The methodology pins the artefact: a rubric scoring the UI on context-carry-over, recently-used surfaces, autosuggest coverage, and reference panel availability.

**Ефективно для:**

- Multi-step workflows where the user must remember earlier choices.
- Reviewers catching hidden state that forces recall.
- Accessibility reviewers helping users with cognitive load issues.
- Audit surface: rubric score per screen.

## Applies If (ALL must hold)

- Workflow has ≥3 sequential screens / states.
- User decisions depend on data from prior screens.
- Form filling or selection from large option sets is present.

## Skip If (ANY kills it)

- Single-screen task with no prior context.
- Trivial one-input form.
- Audience is system-level (rare exception).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workflow map | diagram | Product |
| UI screens | URLs / mockups | Frontend |
| Option sets / catalogues | data | Backend |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `none` | This methodology has no upstream dependency. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-recognition-over-recall` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-recognition-over-recall` | haiku | Schema check + threshold checks; deterministic. |
| `review-recognition-over-recall` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/recognition-over-recall.json` | JSON skeleton conforming to the output contract schema. |
| `templates/recognition-over-recall.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-recognition-over-recall.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[match-real-world]]
- [[flexibility-efficiency]]
- [[visibility-of-system-status]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
