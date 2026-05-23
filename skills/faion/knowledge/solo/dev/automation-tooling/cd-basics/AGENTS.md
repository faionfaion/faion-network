---
slug: cd-basics
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Keeps every commit in a releasable state via CI tests, feature flags, backward-compatible migrations, IaC, and a one-button production deploy gate.
content_id: "1194c7724ddade5a"
complexity: medium
produces: spec
est_tokens: 5000
tags: [continuous-delivery, feature-flags, expand-contract-migration, iac, releasable-mainline]
---
# Continuous Delivery Basics

## Summary

**One-sentence:** Keeps every commit in a releasable state via CI tests, feature flags, backward-compatible migrations, IaC, and a one-button production deploy gate.

**One-paragraph:** Keeps every commit in a releasable state via CI tests, feature flags, backward-compatible migrations, IaC, and a one-button production deploy gate. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Service has CI in place + comprehensive automated tests.
- Stakeholders want releases on commit, not on a manual testing campaign.
- Team owns the deploy pipeline and can iterate on it.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Service has CI in place + comprehensive automated tests.
- Stakeholders want releases on commit, not on a manual testing campaign.
- Team owns the deploy pipeline and can iterate on it.

## Skip If (ANY kills it)

- No CI or no automated tests yet — install CI and tests first.
- Compliance regime requires manual change-control gates per release — adapt or do not adopt CD.
- Codebase is unstable enough that mainline is rarely deployable — stabilise first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CI workflow | .github/workflows/ci.yml or equivalent | infra |
| Test suite coverage | ≥70% line coverage on critical paths | team |
| IaC for environments | terraform/pulumi or equivalent | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cd-pipelines]] | concrete pipeline YAML + deployment strategies |

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
| `audit-prereqs` | haiku | Check CI + tests + IaC + flags presence. |
| `design-pipeline` | sonnet | Map workflow to build → test → staging → prod stages. |
| `phased-rollout-plan` | sonnet | Propose adoption phases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/expand_contract_migration.sql` | Expand–contract migration: phase 1 (add nullable column) + phase 2 (backfill) + phase 3 (drop old) |
| `templates/release_checklist.md` | Per-commit release checklist: green CI + flag-default-off + DB migration phase |
| `templates/_smoke-test.sql` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cd-basics.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[cd-pipelines]]
- [[continuous-delivery]]
- [[feature-flags-types-lifecycle]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are CI, automated tests, and IaC already in place?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
