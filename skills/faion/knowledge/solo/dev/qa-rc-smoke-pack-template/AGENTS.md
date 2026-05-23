---
slug: qa-rc-smoke-pack-template
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: A ≤10-step smoke pack covering critical paths (auth, payment, write, search, export) executed against every release candidate before promotion.
content_id: "11521a2bfc823250"
complexity: medium
produces: checklist
est_tokens: 4300
tags: [qa, smoke-test, release-candidate, checklist, gate]
---
# QA Release Candidate Smoke Pack

## Summary

**One-sentence:** A ≤10-step smoke pack covering critical paths (auth, payment, write, search, export) executed against every release candidate before promotion.

**One-paragraph:** A ≤10-step smoke pack covering critical paths (auth, payment, write, search, export) executed against every release candidate before promotion. Steps are scripted (one command each), produce binary outputs, cover the top revenue/data paths, and run in ≤5 min. Pack is versioned and reviewed every release. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Have release candidates that get promoted to production with no consistent smoke gate.
- Production has had ≥1 incident in the last 90 days that a smoke test would have caught.
- Manual smoke is informal and varies by who runs it.
- Output produces `checklist` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Have release candidates that get promoted to production with no consistent smoke gate.
- Production has had ≥1 incident in the last 90 days that a smoke test would have caught.
- Manual smoke is informal and varies by who runs it.

## Skip If (ANY kills it)

- Full E2E suite runs <5 min and gates promotion already — duplicates coverage.
- No formal RC stage (continuous deploy with flags) — different control surface.
- Pre-product team with no production users — premature.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Critical-path inventory | list of business journeys | product/critical-paths.md |
| RC environment | staging URL + creds | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[release-qa-cycle-template]] | Smoke pack is one stage of the release cycle. |
| [[qa-perf-run-verdict-template]] | Perf verdict runs after smoke pack. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-steps` | sonnet | Derive ≤10 steps from critical-paths.md. |
| `script-step` | sonnet | Translate each step into a runnable command. |
| `review-coverage` | opus | Cross-cutting: does the pack cover top incident areas? |

## Templates

| File | Purpose |
|------|---------|
| `templates/smoke_pack.yaml` | YAML configuration scaffolding the artefact. |
| `templates/run_pack.sh` | Shell script scaffolding the runnable artefact. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-rc-smoke-pack-template.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[release-qa-cycle-template]]
- [[qa-bug-bash-runbook]]
- [[qa-rollback-trigger-canon]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Does the team promote release candidates to production with no consistent smoke gate?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
