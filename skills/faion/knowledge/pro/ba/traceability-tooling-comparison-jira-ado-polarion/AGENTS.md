---
slug: traceability-tooling-comparison-jira-ado-polarion
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Comparison + setup-guide report for traceability tooling (Jira, Azure DevOps, Polarion, Confluence): link types, custom fields, trace gates, gotchas.
content_id: "c5d8cfe44402e4bb"
complexity: medium
produces: report
est_tokens: 5000
tags: [traceability, jira, ado, polarion, tool-comparison, ba]
---
# Traceability Tooling Comparison (Jira / ADO / Polarion)

## Summary

**One-sentence:** Comparison + setup-guide report for traceability tooling (Jira, Azure DevOps, Polarion, Confluence): link types, custom fields, trace gates, gotchas.

**One-paragraph:** Comparison + setup-guide report for traceability tooling (Jira, Azure DevOps, Polarion, Confluence): link types, custom fields, trace gates, gotchas. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned report artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- BA інherited Jira/ADO/Polarion setup, який не сам проектував.
- потрібна decision-record «який tool під які requirements».
- пастка кастомних полів і link-type консистентності.
- trace-gate gotchas per tool (audit-trail, permission model).
- звіт читає sponsor / PMO без glossary.

## Applies If (ALL must hold)

- task is 'role-business-analyst/Requirements traceability across the full project lifecycle'.
- operator has the artefacts named in Prerequisites before starting.
- output will be consumed by a downstream agent or human reviewer.
- tier == pro or higher.

## Skip If (ANY kills it)

- team already maintains a working tooling-comparison artefact — replace, do not duplicate.
- the change is greenfield prototype with no production users.
- regulatory / compliance context overrides in-methodology guidance.

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
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the report artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/traceability-tooling-comparison-jira-ado-polarion.md` | Working report skeleton with 5-line header |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-traceability-tooling-comparison-jira-ado-polarion.py` | Validate the report artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[traceability-matrix-template-csv]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
