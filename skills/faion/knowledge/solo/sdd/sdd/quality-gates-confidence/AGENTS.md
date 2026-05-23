---
slug: quality-gates-confidence
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Six sequential quality-gate levels (L1 lint → L6 stakeholder sign-off) with an explicit confidence score per gate, so defects are caught at the earliest cheap stage rather than at the end of the SDD pipeline.
content_id: "b93c384fef5e89ea"
complexity: medium
produces: report
est_tokens: 3800
tags: [quality-gates, testing, validation, confidence, ci-cd]
---
# Quality Gates and Confidence Checks

## Summary

**One-sentence:** Six sequential quality-gate levels (L1 lint → L6 stakeholder sign-off) with an explicit confidence score per gate, so defects are caught at the earliest cheap stage rather than at the end of the SDD pipeline.

**One-paragraph:** Six sequential quality-gate levels (L1 lint → L6 stakeholder sign-off) with an explicit confidence score per gate, so defects are caught at the earliest cheap stage rather than at the end of the SDD pipeline. The methodology pins the artefact: every gate has a binary pass/fail signal, a numeric confidence, an owner, and a documented escalation path when confidence is below threshold.

**Ефективно для:**

- SDD batch runs that need a halt rule before promoting to the next phase.
- Solo operators who want a 'red light / green light' summary instead of a noisy CI log.
- Reviewers who need a single decision artefact instead of trawling through diffs.
- Audit surface: every promotion between phases has a recorded gate result.

## Applies If (ALL must hold)

- An SDD pipeline runs multiple phases (spec → design → impl-plan → code → review).
- More than one agent or human contributes artefacts that must be promoted.
- Defect cost rises sharply across phases (cheap at lint, expensive at production).

## Skip If (ANY kills it)

- Throwaway prototype / spike — gating overhead exceeds the value of the artefact.
- Pipeline has a single trusted reviewer who already gates manually.
- Project does not run automated checks; gating without instrumentation is theatre.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-phase artefacts | files | SDD lifecycle |
| CI run output | log | CI provider |
| Reviewer roster | list | Team config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd/sdd-workflow-overview` | Defines which phases the gates promote between. |

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
| `draft-quality-gates-confidence` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-quality-gates-confidence` | haiku | Schema check + threshold checks; deterministic. |
| `review-quality-gates-confidence` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/quality-gates-confidence.json` | JSON skeleton conforming to the output contract schema. |
| `templates/quality-gates-confidence.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-quality-gates-confidence.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[sdd-workflow-overview]]
- [[reflexion-learning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
