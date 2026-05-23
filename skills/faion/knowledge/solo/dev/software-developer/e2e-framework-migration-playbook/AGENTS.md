---
slug: e2e-framework-migration-playbook
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Execute a 4-wave 3-month framework or language migration (PoC, parallel build, cutover, decommission) with explicit entry/exit gates per wave.
content_id: "f16ec07305273b67"
complexity: deep
produces: playbook-step
est_tokens: 4800
tags: [dev, migration, refactor, strangler, branch-by-abstraction, cypress, playwright]
---
# E2E Framework Migration Playbook

## Summary

**One-sentence:** Execute a 4-wave 3-month framework or language migration (PoC, parallel build, cutover, decommission) with explicit entry/exit gates per wave.

**One-paragraph:** Strangler pattern and branch-by-abstraction exist as concepts; this playbook turns them into an executable plan for the common 3-month migration: Cypress→Playwright, Selenium→Playwright, Vue 2→3, Angular X→Y, Python 3.10→3.12, monolith→service. Wave 1 PoC (one feature ported, parity proven), Wave 2 parallel build (incrementally port modules, dual-running with feature flags, codemods where possible), Wave 3 cutover (flag flip, new framework default, old kept as fallback), Wave 4 decommission (remove old framework, remove flags, delete legacy code). Each wave has explicit entry/exit criteria, test gates, rollback plan, comms plan.

**Ефективно для:**

- Cypress→Playwright, Selenium→Playwright migrations.
- Vue 2→3, Angular major-version, React class→function refactors.
- Python 3.x or Node LTS upgrades touching many modules.
- Library swaps that touch a meaningful surface but don't require a full rewrite.

## Applies If (ALL must hold)

- Migration spans >=5 modules or >=50 tests OR a full app framework.
- Estimated migration length is 6 weeks to 6 months.
- Team must ship customer features during the migration (cannot freeze the codebase).
- Target framework / language is at least 1.0 stable (not betas).

## Skip If (ANY kills it)

- Migration is a one-shot <=2 week refactor — use sprint workflow, not multi-wave plan.
- Migration target is unstable (pre-1.0 framework) — defer until target stabilises.
- Migration is forced by external deadline with no slack — accept higher-risk path explicitly.
- Migration scope cannot be split into incremental waves (atomic flag-day) — use big-bang playbook.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ADR justifying the migration: business case, alternative considered, target framework, expected payoff | ADR | tech-lead |
| Inventory of impacted surface (modules, tests, dependencies, deployment artifacts) | table | tech-lead |
| Baseline metrics: test coverage, test run time, build time, perf benchmarks, error rate | numbers | ops |
| Named migration lead with bandwidth (typically 50%+ of one engineer) | role assignment | tech-lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[feature-flags]] | Wave 2 dual-run depends on flag-gated rollout. |
| [[trunk-based-development]] | Waves ship behind flags, not long-lived branches. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (parity-before-cutover, codemod-where-mechanical, dual-test-window, rollback-per-wave, decommission-non-skippable) | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for wave record + migration tracker + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 1100 |
| `content/04-procedure.xml` | essential | 4-step procedure: PoC → parallel build → cutover → decommission | 900 |
| `content/05-examples.xml` | essential | Worked example: Cypress→Playwright over 12 weeks | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory_impacted_surface` | sonnet | Walk codebase, identify dependencies on the old framework. |
| `codemod_authoring` | opus | Cross-file transformation rules — needs precise semantic synthesis. |
| `parity_test_design` | sonnet | Per-module parity tests comparing old vs new framework outputs. |
| `cutover_runbook_drafting` | sonnet | Assemble pre-flight checks + flag-flip steps + post-flight checks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wave-record.json` | Wave exit-gate record skeleton matching the 02-output-contract schema; copy per wave (1..4) and fill before submitting to the validator. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-e2e-framework-migration-playbook.py` | Validate the wave record artefact metadata against 02-output-contract schema | Per-wave exit gate |

## Related

- [[feature-flags]]
- [[trunk-based-development]]
- [[technical-debt]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps migration scope, duration, and target maturity to a rule from `01-core-rules.xml`, telling the agent whether to invoke the wave playbook or skip in favour of sprint-scale refactor or big-bang. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
