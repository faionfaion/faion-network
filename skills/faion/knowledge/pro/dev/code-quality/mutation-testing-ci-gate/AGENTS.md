---
slug: mutation-testing-ci-gate
tier: pro
group: dev
domain: code-quality
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "c3a43c3fe8e98faa"
summary: Adopt mutation testing (Stryker / Mutmut / Pitest) as a CI quality gate so assertion-laxness becomes visible — especially for AI-generated tests that hit line coverage without actually testing behavior.
tags: [testing, quality-gate, mutation-testing, ci, ai-generated-tests]
---

# Mutation Testing as CI Quality Gate

## Summary

**One-sentence:** Stand up Stryker / Mutmut / Pitest as a CI gate that scores assertion strength via the mutation kill rate, replacing line coverage as the honest signal of test quality.

**One-paragraph:** Line coverage is theater — an AI-generated suite can hit 100% line coverage by importing every module and asserting nothing meaningful. Mutation testing introduces small synthetic bugs (mutants) into the code under test and re-runs the suite: if the suite catches the mutant, the assertion was load-bearing; if it survives, the test was decorative. This methodology defines how to introduce a mutation tool to an existing repo without exploding CI time, how to set defensible mutation-score floors per module, and how to wire it as a blocking gate only after a stabilization period. Primary output: a `.stryker.conf.json` / `.mutmut.conf` / `pitest.xml` plus a CI job and a per-module score baseline file.

## Applies If (ALL must hold)

- repo has an existing unit-test suite with line coverage ≥ 70% on changed paths
- CI runner allows jobs > 10 minutes OR a self-hosted runner exists
- language stack ∈ {JavaScript/TypeScript (Stryker), Python (Mutmut / Cosmic-Ray), Java/Kotlin (Pitest), C# (Stryker.NET), PHP (Infection)}
- AI-generated tests OR untrusted contributor tests land in the repo regularly

## Skip If (ANY kills it)

- coverage < 50% — fix coverage first; mutation testing on a thin suite mutates code that is not exercised, producing noise
- suite runtime > 30 min for the unit layer — mutation runs are 10-50× the unit-test runtime; stabilize unit speed first
- language without a maintained mutator (Rust mutation-testing tooling is immature outside `cargo-mutants`; Go has `go-mutesting` but limited operators)
- monorepo with > 100 modules and no incremental mutator — full-repo mutation will exceed CI budget; adopt incremental-mode tools (Stryker `--since`, Mutmut `--paths-to-mutate` on diff) before gating

## Prerequisites

- working unit-test command on the host stack (`npm test`, `pytest`, `mvn test`)
- CI configuration file present and editable (GitHub Actions / GitLab CI / CircleCI)
- baseline line coverage report (lcov, coverage.xml) so mutation work targets covered code only
- buy-in from the team on a mutation-score floor that will start lax and tighten over 4-8 weeks

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/testing-developer/qa-changed-lines-coverage-dashboard` | Diff-only coverage feeds the mutator's mutation scope — full-repo mutation explodes runtime |
| `geek/sdlc-ai/test-mutation-feedback-loop` | Geek-tier sibling for AI agents that author mutations; this pro-tier methodology is for human QA adopters |
| `solo/dev/testing-developer/qa-ai-generated-test-audit-checklist` | Pairs with mutation as the human-audit half of the assertion-quality story |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: kill-rate floor, incremental-only run, equivalent-mutant handling, no-coverage-no-mutate, gate-after-stabilize | ~900 |
| `content/02-output-contract.xml` | essential | Mutation report schema (per-module score, surviving-mutants list, equivalent count) and forbidden patterns | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair (CI-blow-up, equivalent-mutant inflation, line-coverage substitution, etc.) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tool_selection_per_stack` | haiku | Lookup-table decision; deterministic |
| `baseline_run_and_score_floor_proposal` | sonnet | Per-module judgment from baseline output |
| `surviving_mutant_triage` | sonnet | Per-mutant bounded judgment: real gap vs equivalent vs intentional |
| `ci_gate_threshold_curve` | opus | Cross-module synthesis: set per-module floors that ratchet up without breaking velocity |

## Templates

| File | Purpose |
|------|---------|
| `templates/stryker.conf.json` | JS/TS Stryker config with incremental + dashboard reporter |
| `templates/mutmut.cfg` | Python Mutmut config with --paths-to-mutate from diff |
| `templates/pitest.xml` | Java/Kotlin Pitest profile for incremental mutation |
| `templates/ci-mutation.yml` | GitHub Actions / GitLab CI snippet for a non-blocking → blocking gate |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/incremental-mutator.sh` | Reads `git diff --name-only origin/main` and constrains mutation to changed paths | Per PR in CI |
| `scripts/triage-survivors.py` | Parses Stryker/Mutmut survivors JSON, groups by file, flags equivalent-mutant candidates | After mutation run, before posting PR comment |

## Related

- parent skill: `pro/dev/code-quality/SKILL.md`
- peer methodologies: `solo/dev/testing-developer/qa-ai-generated-test-audit-checklist`, `geek/sdlc-ai/test-mutation-feedback-loop`, `solo/dev/testing-developer/qa-changed-lines-coverage-dashboard`
- external: [Stryker Mutator](https://stryker-mutator.io/) · [Mutmut](https://mutmut.readthedocs.io/) · [Pitest](https://pitest.org/) · [Coles et al., "Mutation Testing Advances: An Analysis and Survey" (Advances in Computers, 2019)](https://arxiv.org/abs/1907.04076)
