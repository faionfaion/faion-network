---
slug: traceability-matrix-template-csv
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Ready-to-use CSV traceability matrix + Jira export script for weekly refresh; closes the gap between BA discovery and engineering execution.
content_id: "226ff25f78ffe387"
complexity: medium
produces: spec
est_tokens: 5000
tags: [traceability, matrix, csv, requirements, ba]
---
# Traceability Matrix Template (CSV)

## Summary

**One-sentence:** Ready-to-use CSV traceability matrix + Jira export script for weekly refresh; closes the gap between BA discovery and engineering execution.

**One-paragraph:** Ready-to-use CSV traceability matrix + Jira export script for weekly refresh; closes the gap between BA discovery and engineering execution. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- tracability matrix потрібна щотижнево — не one-off.
- Jira / ADO / Polarion exposed export → fillable CSV.
- BA уникає мануального reformatting кожного спринту.
- matrix є input для CR impact rubric — структура має бути стабільною.
- коли коломна mapping ламається — fail-loudly, не silent drop.

## Applies If (ALL must hold)

- task is 'role-business-analyst/Traceability matrix weekly refresh' or a close variant.
- operator has the artefacts named in Prerequisites before starting.
- output will be consumed by a downstream agent or human reviewer (not discarded).
- tier == pro or higher.

## Skip If (ANY kills it)

- team already maintains a working traceability matrix — replace, do not duplicate.
- the change is greenfield prototype with no production users.
- regulatory / compliance context overrides in-methodology guidance (defer to legal).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the spec artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/traceability-matrix-template-csv.md` | Working spec skeleton with 5-line header |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-traceability-matrix-template-csv.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[traceability-tooling-comparison-jira-ado-polarion]]
- [[change-request-impact-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
