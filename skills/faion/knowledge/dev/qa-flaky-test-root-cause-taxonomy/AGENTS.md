# QA Flaky Test Root-Cause Taxonomy

## Summary

**One-sentence:** A closed 8-category taxonomy for classifying flaky tests (time, order, network, concurrency, environment, randomness, external-state, infrastructure) with detectors and canonical fixes.

**One-paragraph:** A closed 8-category taxonomy for classifying flaky tests (time, order, network, concurrency, environment, randomness, external-state, infrastructure) with detectors and canonical fixes. One enum, eight categories. Each entry lists detector signals and the canonical fix family. Flake ledger references this taxonomy via root_cause attribute. Decision tree, output contract, failure modes, and the decision tree live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Flake ledger exists or about to exist; needs a stable enum.
- Engineers re-investigate the same symptom because no shared taxonomy exists.
- Test stability KPI needs root-cause-level breakdown for prioritisation.
- Output produces `rubric` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Flake ledger exists or about to exist; needs a stable enum.
- Engineers re-investigate the same symptom because no shared taxonomy exists.
- Test stability KPI needs root-cause-level breakdown for prioritisation.

## Skip If (ANY kills it)

- Suite is < 50 tests; per-test ad-hoc investigation is fine.
- Org enforces a different (e.g. Google) taxonomy — adopt theirs.
- Tests are all UI E2E; specialist UI flake taxonomy is more useful.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent flake samples | list of failing test logs | CI / flake ledger |
| Existing root-cause label set | list | if any |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-flake-ledger-template]] | Ledger that consumes this taxonomy enum. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-failure` | sonnet | Map log signals to one of the 8 categories. |
| `propose-fix-family` | sonnet | Recommend the canonical fix family for the chosen category. |

## Templates

| File | Purpose |
|------|---------|
| `templates/taxonomy.json` | JSON template scaffolding the artefact contract. |
| `templates/classify.py` | Python scaffold realising the artefact in code. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-flaky-test-root-cause-taxonomy.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[qa-flake-ledger-template]]
- [[qa-suite-health-metrics-canon]]
- [[qa-rollback-trigger-canon]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are we classifying flakes by root cause to drive remediation?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
