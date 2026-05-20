---
slug: e2e-framework-migration-playbook
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Wave-based migration template anchoring tests, feature flags, codemods, and cutover for a typical 3-month framework / language migration (e.g., Cypress → Playwright, Vue 2 → Vue 3).
content_id: "3233fcb6e6b8b2a5"
tags: [dev, migration, refactor, strangler, branch-by-abstraction, cypress, playwright, framework]
---

# E2E Framework Migration Playbook

## Summary

**One-sentence:** A 4-wave migration template (proof-of-concept, parallel-build, cutover, decommission) with checklists for tests / flags / codemods / observability that drives a 3-month framework or language migration end-to-end.

**One-paragraph:** Strangler pattern and branch-by-abstraction exist as concepts; this methodology turns them into an executable plan for the common 3-month migration: Cypress→Playwright, Selenium→Playwright, Vue 2→3, Angular X→Y, Python 3.10→3.12, monolith→service. Mechanism: Wave 1 PoC (one feature ported, parity proven), Wave 2 parallel build (incrementally port modules, dual-running with feature flags, codemods automated where possible), Wave 3 cutover (flag flip, new framework default, old kept as fallback), Wave 4 decommission (remove old framework, remove flags, delete legacy code). Each wave has explicit entry / exit criteria, test gates, rollback plan, comms plan. Primary output: a migration tracker + per-wave checklist + a sane way to ship features DURING the migration.

## Applies If (ALL must hold)

- migration spans a meaningful surface (>= 5 modules or >= 50 tests OR a full app framework)
- estimated migration length is 6 weeks to 6 months (multi-quarter migrations need additional sub-playbooks)
- team must ship customer features DURING the migration (cannot freeze the codebase)
- target framework / language is at least 1.0 stable (not betas; betas need a different risk plan)

## Skip If (ANY kills it)

- migration is a one-shot &lt;= 2-week refactor — use sprint workflow, not a multi-wave plan
- migration target is unstable (pre-1.0 framework) — defer until target stabilizes OR plan as an experiment, not a migration
- migration is forced by external deadline with no slack — accept higher-risk path, document explicitly
- migration scope cannot be split into incremental waves (atomic flag-day cutover) — use big-bang playbook instead

## Prerequisites

- decision document (ADR) justifying the migration: business case, alternative considered, target framework, expected payoff
- inventory of impacted surface (modules, tests, dependencies, deployment artifacts)
- baseline metrics captured: test coverage, test run time, build time, perf benchmarks, error rate
- named migration lead with bandwidth (typically 50%+ of one engineer)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/strangler-pattern` | Wave 2 (parallel build) is strangler pattern in practice; consume the canonical pattern |
| `solo/dev/software-architect/branch-by-abstraction` | Sub-pattern for in-place migrations within a single codebase |
| `solo/sdd/sdd/architecture-decision-records` | Each wave produces decisions that should be ADR-recorded |
| `solo/dev/testing-developer/test-coverage-floor` | Test gate per wave depends on this baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: parity-before-cutover, codemod-where-mechanical, dual-write-or-dual-test-window, rollback-path-per-wave, decommission-is-non-skippable | ~1000 |
| `content/02-output-contract.xml` | essential | Wave record + migration tracker schema + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (parallel-run-forever, codemod-overconfidence, etc.) with detector + repair | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory_impacted_surface` | sonnet | Walk codebase, identify dependencies on the old framework |
| `codemod_authoring` | opus | Cross-file transformation rules — needs precise semantic synthesis |
| `parity_test_design` | sonnet | Per-module parity tests comparing old vs new framework outputs |
| `cutover_runbook_drafting` | sonnet | Mechanical: assemble pre-flight checks + flag-flip steps + post-flight checks |

## Templates

| File | Purpose |
|------|---------|
| `templates/migration-tracker.md` | Top-level tracker with wave status + module status |
| `templates/wave-record.json` | Per-wave entry/exit + decisions + dates |
| `templates/cutover-runbook.md` | Pre / during / post flag-flip steps |
| `templates/codemod-skeleton.py` | Codemod template (jscodeshift / libcst / similar) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/audit-old-framework-usage.py` | Counts remaining imports / usages of the old framework | Weekly during waves 2-4 |
| `scripts/run-parity-tests.py` | Runs paired tests on old + new framework, returns diff | Wave 1 PoC; Wave 2 per module |

## Related

- parent skill: `solo/dev/software-developer/`
- peer methodologies: `strangler-pattern`, `branch-by-abstraction`, `feature-flag-lifecycle`
- external: [Fowler — StranglerFigApplication](https://martinfowler.com/bliki/StranglerFigApplication.html) · [Cypress→Playwright Migration Guide](https://playwright.dev/docs/cypress) · [Vue Migration Build](https://v3-migration.vuejs.org/migration-build.html)
