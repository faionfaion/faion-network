# QA Test Strategy Template

## Summary

**One-sentence:** A 1-page test strategy spec: risks, scope, layers (unit/integration/contract/e2e/perf/sec), out-of-scope, owner, and exit criteria — anchored on declared risks.

**One-paragraph:** A 1-page test strategy spec: risks, scope, layers (unit/integration/contract/e2e/perf/sec), out-of-scope, owner, and exit criteria — anchored on declared risks. Strategy is risk-first: list risks, then map each to a layer + technique + owner + exit criterion. Out-of-scope is explicit. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Starting QA for a new feature with ≥2 weeks of dev work.
- Reviewing an existing strategy that lists tests but not the risks they address.
- Aligning multiple stakeholders (dev/qa/security/sre) on what 'tested' means for this release.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Starting QA for a new feature with ≥2 weeks of dev work.
- Reviewing an existing strategy that lists tests but not the risks they address.
- Aligning multiple stakeholders (dev/qa/security/sre) on what 'tested' means for this release.

## Skip If (ANY kills it)

- Trivial bug fix or single-line change — strategy is overkill.
- Org template already exists with equivalent shape — adopt theirs.
- Pre-product spike code with no QA contract.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec | Markdown | Linked spec/issue |
| Risk register | List | spec or threat-model |
| Layer matrix | test types available | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-prioritization-rubric]] | Risks rated by severity rubric. |
| [[qa-test-data-catalog]] | Fixtures referenced by id. |

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
| `derive-risks` | opus | Cross-cutting synthesis of feature spec + threat model. |
| `map-to-layer` | sonnet | Pick layer + technique per risk. |
| `set-exit` | sonnet | Declare exit criteria per layer. |

## Templates

| File | Purpose |
|------|---------|
| `templates/strategy.md` | Markdown skeleton for the artefact. |
| `templates/risks_table.csv` | CSV template for tabular artefacts. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-test-strategy-template.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[qa-prioritization-rubric]]
- [[qa-test-data-catalog]]
- [[qa-bug-bash-runbook]]
- [[release-qa-cycle-template]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the feature large enough (≥2 weeks dev) that we need a documented test strategy?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
