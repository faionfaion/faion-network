# Staging Smoke Checklist by Surface

## Summary

**One-sentence:** Per-surface staging smoke checklist - top-3 surfaces with click-expect items, sign-off line, repo-committed, abort-on-fail gate before every production promotion.

**One-paragraph:** Continuous delivery talks about smoke testing in the abstract, but solo developers need a concrete daily artefact. This methodology produces a markdown checklist listing the three highest-impact surfaces of the system, each item phrased as click-expect, with a sign-off line including initials + UTC timestamp + build SHA. The file lives in the repo next to the deploy script and re-runs every time staging gets a new build. Replaces the 'I'll just click around' pattern that silently misses regressions in surfaces the dev did not touch.

**Ефективно для:**

- Solo founder без QA - замiнюe ad-hoc click-around на повторюваний gate.
- Маленька команда без E2E coverage - дешевий smoke між unit і повним прогоном.
- Часті production-deploy без CI/CD pipeline - artefact як обовязковий промо-rito.
- Нова фіча торкається 3 surfaces - оновити checklist разом з кодом.
- Post-incident, коли regression проскочив - закрити gap саме на тому surface.

## Applies If (ALL must hold)

- Project has a distinct staging environment with the same shape as production.
- Promotion from staging to production is a deliberate action (script or manual approval), not auto-promote.
- Dev is the sole owner of staging sign-off (no separate QA gate).
- Repo has at least one user-facing surface (web UI, API, CLI) with observable behaviour.

## Skip If (ANY kills it)

- Trunk-based deploys directly to prod without staging - there is nothing to smoke.
- Library or pure backend with no UI/API surface - use unit/contract testing instead.
- System has full E2E automation covering the high-impact surfaces - checklist is redundant.
- Pre-launch project with fewer than 2 surfaces - inline test notes suffice.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Staging URL + credentials | URL + auth | platform |
| Top-3 surfaces by impact | ranked list | product |
| Stable repo path | file path under ops/ or repo root | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[deploy-notes-template-with-rollback]] | deploy artefact this checklist links into. |
| [[qa-rc-smoke-pack-template]] | broader smoke-pack convention this artefact specializes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: top-3 cap, click-expect format, sign-off line, repo-committed, abort-on-fail, skip-gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: pick surfaces, write items, commit, run, gate | ~800 |
| `content/05-examples.xml` | essential | Worked example: SaaS web + API + webhook smoke checklist | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals to a rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-surfaces` | sonnet | Impact ranking requires per-product judgement. |
| `write-items` | haiku | Mechanical click-expect drafting from a known surface. |
| `verify-format` | haiku | Pattern check: click-expect shape + sign-off line. |
| `gate-promotion` | opus | Stakes high; a wrong yes ships a regression. |

## Templates

| File | Purpose |
|------|---------|
| `templates/staging-smoke.md` | Markdown skeleton for the smoke checklist (3 surfaces + sign-off line). |
| `templates/_smoke-test.md` | Filled-in minimum viable staging-smoke for the validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-staging-smoke-checklist-by-surface.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[deploy-notes-template-with-rollback]]
- [[qa-rc-smoke-pack-template]]
- [[spec-driven-debugging]]

## Decision tree

See `content/06-decision-tree.xml`. The tree checks preconditions, then surface count, then item format, then sign-off presence. Every leaf maps to a rule id from `content/01-core-rules.xml`, with skip-this-methodology as the default for unmet preconditions.
