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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mutation-testing-ci-gate.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ci-prod-readiness-gates]]
- [[rust-testing-property]]

## Decision tree

See `content/06-decision-tree.xml`. Tree picks the mutator by language, gates shadow→blocking on noise rate, and routes survivors through triage.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/stryker.conf.json`

```json
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "mutate": [
    "src/**/*.ts",
    "!src/**/*.test.ts"
  ],
  "testRunner": "jest",
  "reporters": [
    "html",
    "clear-text",
    "dashboard"
  ],
  "incremental": true,
  "incrementalFile": ".stryker-tmp/incremental.json",
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 60
  },
  "timeoutMS": 60000
}
```

### `templates/mutmut.cfg`

```ini
[mutmut]
paths_to_mutate=src/
runtests=pytest -q
backup=false
use_coverage=true
tests_dir=tests/
```

### `templates/ci-mutation.yml`

```yaml
name: mutation
on:
  pull_request:
jobs:
  mutation:
    runs-on: ubuntu-latest
    continue-on-error: true   # FLIP TO false AFTER 14-DAY SHADOW PERIOD
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: incremental mutation
        run: scripts/incremental-mutator.sh
      - name: triage survivors
        run: python scripts/triage-survivors.py
```
