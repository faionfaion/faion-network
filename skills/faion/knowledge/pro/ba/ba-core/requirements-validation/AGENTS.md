---
slug: requirements-validation
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a validation report confirming each requirement meets value-alignment, feasibility, and review criteria before sign-off.
content_id: "7a0eec1a71c7f450"
complexity: medium
produces: report
est_tokens: 4300
tags: [ba, validation, review, sign-off, quality]
---
# Requirements Validation

## Summary

**One-sentence:** Produces a validation report confirming each requirement meets value-alignment, feasibility, and review criteria before sign-off.

**One-paragraph:** Produces a validation report confirming each requirement meets value-alignment, feasibility, and review criteria before sign-off. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Pre-baseline checkpoint — requirements готові до schedule-lock.
- Compliance/contract context — треба documented evidence що requirement'и перевірені.
- Cross-team handoff — щоб dev/QA довіряли requirement'у на вході.
- Post-defect aftermath: треба нагнати validation gate, який пропустили раніше.

## Applies If (ALL must hold)

- Requirements bundle is about to be baselined / approved.
- Compliance or contract requires documented validation evidence.
- Cross-team handoff where downstream owners need confidence in requirement quality.
- Defect investigation traces back to a requirement that was never validated.

## Skip If (ANY kills it)

- Throwaway prototype.
- Requirements churn faster than validation can complete.
- Validation gate is purely ceremonial and adds no signal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Requirements register | Output of requirements-documentation | BA |
| Value drivers | Output of strategy-analysis or roadmap | PM |
| Feasibility check from engineering | Markdown | engineering |
| Review checklist template | Markdown | BA team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[requirements-documentation]] | input requirements |
| [[acceptance-criteria]] | AC count is part of validation gate |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `run-review-checklist` | haiku | Mechanical check against checklist. |
| `score-value-alignment` | sonnet | Match requirement to value driver. |
| `draft-validation-report` | sonnet | Synthesise report with per-requirement verdict. |

## Templates

| File | Purpose |
|------|---------|
| `templates/review-checklist.md` | Per-requirement validation checklist. |
| `templates/sign-off-form.md` | Sign-off form with reviewer + date + verdict. |
| `templates/req-value-trace.sh` | Shell helper linking requirements to value drivers. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-requirements-validation.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[requirements-documentation]]
- [[acceptance-criteria]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
