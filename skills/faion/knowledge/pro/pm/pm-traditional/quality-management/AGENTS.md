---
slug: quality-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Three-process discipline: Plan Quality (standards + thresholds), Manage Quality (process assurance), Control Quality (deterministic gates per deliverable).
content_id: "3d23e184e7b5346c"
complexity: medium
produces: config
est_tokens: 4200
tags: [quality-management, quality-gates, definition-of-done, cost-of-quality, defect-triage]
---
# Quality Management

## Summary

**One-sentence:** Three-process discipline: Plan Quality (standards + thresholds), Manage Quality (process assurance), Control Quality (deterministic gates per deliverable).

**One-paragraph:** Three-process discipline: Plan Quality (standards + thresholds), Manage Quality (process assurance), Control Quality (deterministic gates per deliverable). The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-quality-management.py` enforces the output contract.

**Ефективно для:**

- Programs with measurable quality standards (defects, performance, accessibility).
- Regulated programs requiring documented quality plan.
- Multi-vendor programs where quality varies by source.
- Programs comparing cost of conformance vs cost of non-conformance.

## Applies If (ALL must hold)

- Quality attributes can be defined as measurable thresholds (defect rate, p95 latency, WCAG compliance).
- Each deliverable has a Definition of Done.
- Defects can be triaged by severity + priority.

## Skip If (ANY kills it)

- Pure research / exploration where quality is undefined.
- Single-prototype throwaway work.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Quality standards | list of metric × threshold | PM + tech lead |
| Definition of Done | Markdown | team |
| Defect triage rubric | severity × priority matrix | QA lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[scrum-ceremonies]] | DoD is baked into Definition of Done in Scrum |
| [[project-integration]] | quality is one of the integrated areas |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `define-thresholds` | sonnet | Judgement: realistic + measurable thresholds. |
| `run-gate` | haiku | Mechanical artefact vs thresholds. |
| `triage-defects` | sonnet | Judgement: severity × priority + assignment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/quality-gate.py` | Quality-gate script: artefact + thresholds → pass/fail with violations |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-quality-management.py` | Validate the config artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[scrum-ceremonies]]
- [[project-integration]]
- [[lessons-learned]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

