---
slug: qa-flake-ledger-template
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Defines a versioned flake ledger: per-test entries with first-seen, last-seen, run/fail counts, root-cause taxonomy, owner, and quarantine state.
content_id: "534af1233344063c"
complexity: medium
produces: spec
est_tokens: 5000
tags: [qa, flake, ledger, test-stability, ci]
---
# QA Flake Ledger Template

## Summary

**One-sentence:** Defines a versioned flake ledger: per-test entries with first-seen, last-seen, run/fail counts, root-cause taxonomy, owner, and quarantine state.

**One-paragraph:** Defines a versioned flake ledger: per-test entries with first-seen, last-seen, run/fail counts, root-cause taxonomy, owner, and quarantine state. Schema-locked: every flaky test gets one row; CI updates counts; owner is named; quarantine state is auto-promoted after threshold; weekly review burns down the ledger. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- CI has visible flake (≥1% intermittent fail rate) and no central record.
- Quarantining flakes ad-hoc leaks into the test budget with no review cadence.
- Test ownership is unclear; flakes survive months because no name is attached.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- CI has visible flake (≥1% intermittent fail rate) and no central record.
- Quarantining flakes ad-hoc leaks into the test budget with no review cadence.
- Test ownership is unclear; flakes survive months because no name is attached.

## Skip If (ANY kills it)

- Test suite < 50 tests where every flake is obvious without a ledger.
- Team retests on green and the policy is 'no retries, no ledger needed' — different control.
- Sub-1% flake rate sustained for ≥30 days — overhead doesn't pay back.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CI history | JSON test results last 30 days | CI provider api |
| Codeowners map | CODEOWNERS file | repo root |
| Quarantine mechanism | marker/tag | pytest/jest config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-flaky-test-root-cause-taxonomy]] | Root-cause taxonomy populates ledger entries. |
| [[qa-suite-health-metrics-canon]] | Suite health metrics feed promote/demote decisions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ingest-ci-results` | haiku | Parse CI JSON and compute fail/run per test. |
| `classify-root-cause` | sonnet | Apply taxonomy to flake symptoms. |
| `assign-owner` | haiku | Lookup CODEOWNERS by test path. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ledger.csv` | CSV template for tabular artefacts. |
| `templates/ingest.py` | Python scaffold realising the artefact in code. |
| `templates/_smoke-test.csv` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-flake-ledger-template.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[qa-flaky-test-root-cause-taxonomy]]
- [[qa-suite-health-metrics-canon]]
- [[qa-rollback-trigger-canon]]
- [[qa-test-strategy-template]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Does the suite show ≥1% sustained flake rate with no central record?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
