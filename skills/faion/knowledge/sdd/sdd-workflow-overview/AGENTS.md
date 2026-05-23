# SDD Workflow Overview

## Summary

**One-sentence:** Specification-Driven Development overview: a five-phase lifecycle (spec → design → impl-plan → tasks → review) where intent is the source of truth and each phase produces a versioned artefact that gates the next.

**One-paragraph:** Specification-Driven Development overview: a five-phase lifecycle (spec → design → impl-plan → tasks → review) where intent is the source of truth and each phase produces a versioned artefact that gates the next. The methodology pins the artefact: a top-level SDD manifest that names the feature, lists artefact paths, current phase, and the gate result that authorised entry into that phase.

**Ефективно для:**

- Solo founders adopting SDD for the first time — needs a single map of how the pieces fit.
- Reviewers checking that a feature is in the right phase before further work.
- Onboarding new contributors / subagents into the workflow.
- Audit surface: every feature has a manifest stating its current phase and last gate result.

## Applies If (ALL must hold)

- A multi-phase workflow is being adopted for feature delivery.
- Artefacts (spec, design, impl-plan) are written before code, not retrofitted.
- Multiple humans or agents contribute and need shared vocabulary.

## Skip If (ANY kills it)

- One-off script with no spec, design, or plan needed.
- Existing workflow already has a documented phase model that the team prefers.
- Pre-PMF prototyping where speed > rigour.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature folder | directory | Project repo |
| Phase artefact paths | list | Project layout |
| Gate config | yaml | CI / pipeline |

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
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-sdd-workflow-overview` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-sdd-workflow-overview` | haiku | Schema check + threshold checks; deterministic. |
| `review-sdd-workflow-overview` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sdd-workflow-overview.json` | JSON skeleton conforming to the output contract schema. |
| `templates/sdd-workflow-overview.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sdd-workflow-overview.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[writing-specifications]]
- [[writing-design-documents]]
- [[writing-implementation-plans]]
- [[task-creation-parallelization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
