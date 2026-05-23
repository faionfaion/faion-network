# Mutation Testing Bootstrap

## Summary

**One-sentence:** Bootstraps a per-language mutation-testing config (mutmut / stryker) with a survivor-rate gate wired into CI.

**One-paragraph:** Line + branch coverage measures whether tests touched code, not whether they would notice a bug. Mutation testing flips operators / boundaries and checks whether tests fail — the surviving mutants are the holes. This methodology bootstraps mutation testing per language (mutmut for Python, stryker for JS/TS, infection for PHP), pins a survivor-rate gate (≤25% to start, ratcheting), scopes mutants to changed files only in PRs, and enforces a 10-minute CI budget. Output is a config artefact validated against the schema before merge.

**Ефективно для:**

- Teams with high line coverage but low confidence in their assertions.
- Critical paths (payments, auth, RBAC) where mutant-survival is unacceptable.
- PR-scope gating — only mutate changed files to keep CI under 10 minutes.
- Researchers comparing test-suite quality across modules.

## Applies If (ALL must hold)

- Existing test suite passes consistently (no flakes).
- Line coverage already ≥80% — mutation testing is wasted on poorly-covered code.
- Language has a maintained mutation-testing tool (mutmut / stryker / infection / pitest).
- CI budget allows a 10-minute incremental job per PR.

## Skip If (ANY kills it)

- Prototype or spike — mutation testing is overhead.
- Line coverage < 80% — fix coverage first via `code-coverage`.
- Flaky test suite — fix flakes first; mutation testing on flakes is noise.
- Generated code — mutation results are not actionable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Language | string | repo conventions |
| Test framework + runner | pytest / vitest / jest / phpunit | package config |
| Coverage baseline | ≥80% line+branch | coverage tool |
| PR-scope file list | git diff --name-only | git |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| methodology-versioning-and-changelog | Bootstrap is a versioned event. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: r1-tool-per-language, r2-scope-pr-changed-files, r3-survivor-gate, r4-ci-budget-10m, r5-no-flakes | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the bootstrap config + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: mutate-everything, ignore-survivors, equivalent-mutant-silence, no-budget-cap, flake-noise | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: pick tool → wire config → measure baseline → set survivor gate → wire into CI | 800 |
| `content/06-decision-tree.xml` | essential | Maps (language, coverage band, CI budget, flake rate) → tool + gate + scope | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-tool` | haiku | Lookup by language. |
| `draft-config` | sonnet | Per-repo judgement (scope, exclusions, budget). |
| `survivor-review` | opus | Surviving mutants need cross-test judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mutmut.cfg` | Python (mutmut) config skeleton. |
| `templates/stryker.conf.mjs` | Stryker JS/TS config skeleton. |
| `templates/mutation-bootstrap.json` | Decision-record JSON skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mutation-testing-bootstrap.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[methodology-versioning-and-changelog]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
