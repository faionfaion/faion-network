# QA Test Data Catalog

## Summary

**One-sentence:** A central, versioned catalog of named test fixtures (id, shape, source, refresh policy, PII status) ensuring tests use canonical data, not bespoke ad-hoc rows.

**One-paragraph:** A central, versioned catalog of named test fixtures (id, shape, source, refresh policy, PII status) ensuring tests use canonical data, not bespoke ad-hoc rows. One catalog file lists every named fixture with a stable id, owning service, refresh policy, PII flag, and consumer list. Tests import by id; ad-hoc fixtures are blocked. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Multiple test files create similar fixtures locally; data drift is causing flakes.
- Need PII compliance: explicit accounting of which fixtures contain anonymised data.
- Adding new services needs known-good seed data and there's no canonical source.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Multiple test files create similar fixtures locally; data drift is causing flakes.
- Need PII compliance: explicit accounting of which fixtures contain anonymised data.
- Adding new services needs known-good seed data and there's no canonical source.

## Skip If (ANY kills it)

- Single test file with <50 tests — local factories are fine.
- Greenfield project pre-MVP — wait for shape to stabilise.
- Hermetic test setup that builds everything from primitives; catalog adds overhead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing fixture inventory | grep of factory_boy / pytest fixture | repo |
| PII matrix | list of sensitive fields | compliance/security |
| Seed data source | DB dump or synthetic generator | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-test-strategy-template]] | Strategy chooses which fixtures map to which test type. |
| [[django-services]] | Services own the canonical write paths used to materialise fixtures. |

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
| `inventory-fixtures` | haiku | Mechanical: grep + parse fixture decorators. |
| `classify-pii` | sonnet | Map fields to PII matrix; flag sensitive fixtures. |
| `write-catalog` | sonnet | Translate inventory into the canonical schema. |

## Templates

| File | Purpose |
|------|---------|
| `templates/catalog.json` | JSON template scaffolding the artefact contract. |
| `templates/factories.py` | Python scaffold realising the artefact in code. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-test-data-catalog.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[qa-test-strategy-template]]
- [[qa-flake-ledger-template]]
- [[django-services]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are tests creating fixtures ad-hoc with drift symptoms or PII concerns?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
