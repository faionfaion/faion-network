# Flexibility and Efficiency of Use

## Summary

**One-sentence:** Nielsen Heuristic #7 applied: design for both novice and expert users simultaneously by providing accelerators (keyboard shortcuts, bulk operations, templates) that novices can ignore but experts use daily, plus progressive disclosure and multiple paths to the same goal.

**One-paragraph:** Nielsen Heuristic #7 applied: design for both novice and expert users simultaneously by providing accelerators (keyboard shortcuts, bulk operations, templates) that novices can ignore but experts use daily, plus progressive disclosure and multiple paths to the same goal. The methodology pins the artefact: a flexibility rubric scoring a UI on accelerator coverage, customisation depth, and parallel-path availability, with a remediation list per gap.

**Ефективно для:**

- Productivity SaaS with both first-time users and daily power users.
- UI reviews looking for hidden expert paths (shortcuts, bulk ops).
- Accessibility reviewers checking multi-modal access to the same goal.
- Audit surface: rubric score is reviewable and reproducible.

## Applies If (ALL must hold)

- Product is used by both novices and experts.
- Repetitive workflows exist that experts perform daily.
- The UI is operated by humans (not API-only).

## Skip If (ANY kills it)

- One-shot wizard with no repeat use.
- Single-user-type tool (only novices or only experts).
- Backend / API-only product with no UI.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target screen | URL / mockup | Product |
| Persona list | markdown | Research |
| Workflow inventory | list | Product analytics |

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
| `draft-flexibility-efficiency` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-flexibility-efficiency` | haiku | Schema check + threshold checks; deterministic. |
| `review-flexibility-efficiency` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/flexibility-efficiency.json` | JSON skeleton conforming to the output contract schema. |
| `templates/flexibility-efficiency.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-flexibility-efficiency.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[recognition-over-recall]]
- [[match-real-world]]
- [[visibility-of-system-status]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
