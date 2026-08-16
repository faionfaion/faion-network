# AI-Generated Test Validation

## Summary

**One-sentence:** Validates AI-generated tests against four traps — mirror-test, vanity-coverage, mock-overuse, and assertion-drift — and emits a kept/rejected list.

**One-paragraph:** AI happily emits 80% coverage with tests that re-state the implementation. This methodology validates each AI-generated test against four traps: (1) mirror-test (the test asserts what the code does, not what it should do); (2) vanity-coverage (line coverage without behaviour assertions); (3) mock-overuse (mocking the thing under test); (4) assertion-drift (assertions that never fail). Output: keep/reject list + mutation-survival score per file.

**Ефективно для:**

- Solo dev who let an AI fill the test suite from a stub.
- Pre-merge gate on PRs where >50% of test LOC was AI-authored.
- Cleaning a legacy test suite where mutation-survival is dropping.
- Validating that AI-generated tests would catch regressions, not just shape.

## Applies If (ALL must hold)

- Test suite contains AI-generated tests labelled or detectable by author/commit message.
- Production code under test has changed at least once recently (so the tests have something to fail on).
- Mutation-testing tool is available (mutmut / pitest / Stryker) OR an equivalent kill-rate signal exists.
- Author has authority to delete tests, not just add.

## Skip If (ANY kills it)

- Test suite is entirely human-written.
- Mutation-testing impossible (no language tool available).
- Pure smoke tests where shape-checking is the goal (e.g. import tests).
- Pre-deletion legacy code about to be removed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Test files (with AI-author markers) | language-native | repo |
| Production code under test | language-native | repo |
| Mutation-testing tool | CLI | mutmut / pitest / Stryker |
| Coverage report | lcov / coverage.xml | CI |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ai-diff-size-discipline]] | Caps the AI diff so this validator runs on a reviewable batch. |
| [[deterministic-test-data-pattern]] | Required to compare mutation-survival across runs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules (no mirror-test, behavioural assertion required, no mock-of-SUT, mutation-survival floor, assertion-must-fail-once) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for test-validation report + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: mirror-test, vanity-coverage, mock-of-SUT, assertion-drift | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure (inventory → static-rules → mutation-run → triage → report) | 700 |
| `content/05-examples.xml` | essential | Worked example: 18 AI tests; 7 rejected, 11 kept | 600 |
| `content/06-decision-tree.xml` | essential | Routes by mutation-survival + mock-overuse + assertion presence | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ai_generated_test_validation_static_rules` | haiku | Mechanical AST checks (mock targets, assertion count). |
| `ai_generated_test_validation_mutation_run` | haiku | Run external mutation tool + parse output. |
| `ai_generated_test_validation_triage` | sonnet | Judgement call when a test is borderline. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the test-validation report |
| `templates/_smoke-test.json` | Minimum viable filled-in report for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-generated-test-validation.py` | Validate ai-generated-test-validation artefact against schema | Pre-commit; CI on each artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-diff-size-discipline]]
- [[exploratory-testing-charters]]
- [[flaky-test-elimination]]
- [[deterministic-test-data-pattern]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on (a) mutation_survival &gt;= 0.70, (b) static-rule rejections == 0, and (c) zero assertion-drift survivors. All three required for verdict=pass. Every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/ai-generated-test-validation.json",
  "type": "object",
  "required": [
    "report_id",
    "files_scanned",
    "tests_inventoried",
    "rejections",
    "mutation_survival",
    "verdict"
  ],
  "properties": {
    "report_id": {
      "type": "string",
      "pattern": "^TVR-[A-Z0-9-]{2,40}$"
    },
    "files_scanned": {
      "type": "integer",
      "minimum": 0
    },
    "tests_inventoried": {
      "type": "integer",
      "minimum": 0
    },
    "rejections": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "test",
          "rule_violated",
          "explanation"
        ]
      }
    },
    "mutation_survival": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    },
    "verdict": {
      "type": "string",
      "enum": [
        "pass",
        "rework"
      ]
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "report_id": "TVR-PRICING-API-Q2",
  "files_scanned": 6,
  "tests_inventoried": 18,
  "rejections": [
    {
      "test": "tests/test_pricing.py::test_compute_total_mirrors_impl",
      "rule_violated": "no-mirror-test",
      "explanation": "Asserts price = qty * unit by re-implementing the same multiplication."
    },
    {
      "test": "tests/test_pricing.py::test_apply_discount_no_assert",
      "rule_violated": "behavioural-assertion",
      "explanation": "Calls apply_discount but asserts nothing."
    }
  ],
  "mutation_survival": 0.78,
  "verdict": "pass"
}
```
