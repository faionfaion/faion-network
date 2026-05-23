# Mutation Testing as CI Quality Gate

## Summary

**One-sentence:** Produces a CI config (Stryker / Mutmut / Pitest) that gates PRs on mutation-kill-rate per module, with incremental scope on diff, a shadow-then-block ramp, and equivalent-mutant triage.

**One-paragraph:** Line coverage is theater — an AI-generated suite can hit 100% line coverage while asserting nothing. Mutation testing injects synthetic bugs (mutants) and re-runs the suite: if the suite catches the mutant, the assertion was load-bearing; if not, the test was decorative. This methodology stands up Stryker / Mutmut / Pitest as a CI gate scoped to diff-only mutation, ramps it shadow→blocking over 4-8 weeks, and triages equivalent mutants.

**Ефективно для:**

- AI-generated tests, що тримають 100% line coverage без реальних assert'ів.
- Stryker (JS/TS), Mutmut (Python), Pitest (JVM), Stryker.NET (C#), Infection (PHP).
- Incremental mutation на diff, не full repo.
- Shadow 4-8 тижнів → blocking гейт без fleet breakage.

## Applies If (ALL must hold)

- Repo has an existing unit-test suite with line coverage >= 70% on changed paths.
- CI runner allows > 10 min jobs OR self-hosted runner exists.
- Language stack has a maintained mutator (JS/TS, Python, JVM, C#, PHP).
- AI-generated tests OR untrusted contributor tests land regularly.

## Skip If (ANY kills it)

- Coverage < 50% — fix coverage first.
- Suite runtime > 30 min for unit layer — mutation is 10-50x slower.
- Language without a maintained mutator (Rust/Go mutators are immature).
- Monorepo > 100 modules without an incremental-mode tool.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Working unit-test command | make / npm / pytest | repo |
| CI config (GHA / GitLab / Circle) | YAML | repo |
| Baseline line-coverage report | lcov / coverage.xml | CI artefacts |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ci-prod-readiness-gates]] | Mutation testing slots into the broader prod-readiness gate framework |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 7-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tool-selection-per-stack` | haiku | Lookup-table decision; deterministic. |
| `baseline-run-and-score-floor-proposal` | sonnet | Per-module judgment from baseline output. |
| `surviving-mutant-triage` | sonnet | Per-mutant bounded judgment: real gap vs equivalent vs intentional. |
| `ci-gate-threshold-curve` | opus | Cross-module synthesis: set per-module floors that ratchet up without breaking velocity. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stryker.conf.json` | Stryker config with incremental + dashboard reporter. |
| `templates/mutmut.cfg` | Mutmut config with --paths-to-mutate from diff. |
| `templates/pitest.xml` | Pitest profile for incremental mutation. |
| `templates/ci-mutation.yml` | GitHub Actions snippet for non-blocking → blocking mutation gate. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mutation-testing-ci-gate.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |
| `scripts/incremental-mutator.sh` | Reads `git diff --name-only origin/main` and constrains mutation to changed paths. | per PR in CI |
| `scripts/triage-survivors.py` | Parses Stryker/Mutmut survivors JSON; groups by file; flags equivalent-mutant candidates. | after mutation run, before posting PR comment |

## Related

- [[ci-prod-readiness-gates]]
- [[rust-testing-property]]

## Decision tree

See `content/06-decision-tree.xml`. Tree picks the mutator by language, gates shadow→blocking on noise rate, and routes survivors through triage.
