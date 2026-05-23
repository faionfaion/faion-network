---
slug: feature-flags-services-testing
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Picks a flag service, writes pytest fixtures that exercise both ON and OFF code paths, runs a weekly stale-flag CI audit, and wires a flag agent for definition + cleanup.
content_id: "0c9678e57760bff3"
complexity: medium
produces: spec
est_tokens: 5000
tags: [feature-flags, testing, pytest, openfeature, agentic-workflow]
---
# Feature Flag Services, Testing, and Agentic Workflow

## Summary

**One-sentence:** Picks a flag service, writes pytest fixtures that exercise both ON and OFF code paths, runs a weekly stale-flag CI audit, and wires a flag agent for definition + cleanup.

**One-paragraph:** Picks a flag service, writes pytest fixtures that exercise both ON and OFF code paths, runs a weekly stale-flag CI audit, and wires a flag agent for definition + cleanup. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Operating ≥10 active flags and needing platform features: dashboards, audit log, targeting UI.
- Want CI to catch stale flags (toggle live >90 days, both branches dead) before they rot.
- Want agents to draft flag definitions + cleanup tickets after release.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Operating ≥10 active flags and needing platform features: dashboards, audit log, targeting UI.
- Want CI to catch stale flags (toggle live >90 days, both branches dead) before they rot.
- Want agents to draft flag definitions + cleanup tickets after release.

## Skip If (ANY kills it)

- Less than 3 flags total — service is overkill.
- No CI capacity to add a weekly audit step — manual hygiene only.
- Flag service offering does not meet compliance — stay in-process.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Flag manager or SDK | feature-flags-core-implementation or OpenFeature SDK | team |
| CI runner | GitHub Actions or equivalent | infra |
| Agent platform | Claude Code or similar | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[feature-flags-core-implementation]] | manager + registration upstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `select-service` | sonnet | Match needs against OpenFeature/LaunchDarkly/GrowthBook/Statsig. |
| `write-fixtures` | haiku | Mechanical pytest fixtures. |
| `stale-flag-audit` | sonnet | Heuristic for stale detection. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest_flags.py` | pytest fixtures that exercise ON and OFF branches |
| `templates/stale_flag_audit.py` | Stale flag detector: live >90 days AND both branches still present in code |
| `templates/_smoke-test.py` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-flags-services-testing.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[feature-flags-core-implementation]]
- [[feature-flags-rollout-targeting]]
- [[feature-flags-types-lifecycle]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Do you have ≥3 flags AND CI capacity to audit them?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
