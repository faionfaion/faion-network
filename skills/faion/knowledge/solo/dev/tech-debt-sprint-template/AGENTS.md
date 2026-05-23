---
slug: tech-debt-sprint-template
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Two-week tech-debt sprint template producing a versioned, owner-signed plan artefact: scope, guardrails, daily sync, retro, exit metrics."
content_id: "4db87061697bde5e"
complexity: medium
produces: playbook-step
est_tokens: 5200
tags: [tech-debt, sprint, ritual, refactor, solo]
---
# Tech Debt Sprint Template

## Summary

**One-sentence:** Two-week tech-debt sprint template producing a versioned, owner-signed plan artefact: scope, guardrails, daily sync, retro, exit metrics.

**One-paragraph:** Solo + small-team teams accumulate debt between feature pushes; ad-hoc cleanup weeks produce no measurable outcome because scope, owner, and exit metric are never written down. This methodology pins a two-week debt sprint to a reusable template: scope (<=5 named items, each sized XS-L), guardrails (no new features, freeze migrations), daily 10-min sync (shipped / blocked / cut), retro template (metric movement + carry-over), exit metrics (lint warnings, coverage on touched code, p95 build time). Output is a versioned plan artefact reviewed by a named owner and consumed by retro at sprint end.

**Ефективно для:**

- Recurring quarterly debt-paydown ritual without plan or metric.
- Past cleanup weeks produced no retro - install template + metrics.
- Solo operator burning evenings on debt - timebox + close out.
- Team carries >50 lint warnings - sprint to cut by 50%.
- Test coverage on touched modules <60% - sprint to lift it.

## Applies If (ALL must hold)

- team / operator has run >=1 prior quarter and accumulated visible debt items
- exit metrics can be computed automatically (linter, coverage, build time)
- named owner is accountable for the artefact and the retro
- two contiguous weeks of capacity are available with no feature commit

## Skip If (ANY kills it)

- team already has a working debt-sprint template - replace fields, don't duplicate
- debt is concentrated in one file - just refactor it, no sprint needed
- regulatory deadline overrides scope freeze - defer to compliance

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Debt item list | markdown list with size estimates | team backlog / lint output |
| Baseline metrics | JSON: lint_warn, coverage_pct, p95_build_sec | CI dashboard |
| Named owner | GitHub handle / email | team roster |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[timeboxed-refactor-session-template]] | intra-sprint refactor sessions feed this artefact |
| [[weekly-branch-hygiene-checklist]] | branch hygiene runs every Friday during the sprint |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure (input / action / output / gate) | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scope-debt-items` | sonnet | Per-item sizing requires judgement against codebase. |
| `draft-retro-template` | haiku | Bounded template fill from prior sprint. |
| `compute-exit-metrics` | haiku | Mechanical lint + coverage delta. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high (freeze decisions). |

## Templates

| File | Purpose |
|------|---------|
| `templates/tech-debt-sprint-template.md` | Markdown skeleton for the Tech Debt Sprint Template artefact. |
| `templates/_smoke-test.json` | Minimum viable tech-debt-sprint-template record for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tech-debt-sprint-template.py` | Validate Tech Debt Sprint Template artefact against content/02-output-contract.xml. | After draft, before merge; pre-commit hook. |

## Related

- [[timeboxed-refactor-session-template]]
- [[weekly-branch-hygiene-checklist]]
- [[test-pyramid-policy-enforcement]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps measurable-debt, capacity, and named-ownership signals onto a rule from 01-core-rules.xml. Use it before opening a sprint: it catches blind-sprint and collective-owner upstream.
