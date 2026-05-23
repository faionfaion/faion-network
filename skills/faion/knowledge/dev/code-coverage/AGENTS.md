# Code Coverage

## Summary

**One-sentence:** Produces a branch-coverage CI gate scoped to diff (90% on new code) plus mutation testing on critical modules.

**One-paragraph:** Produces a branch-coverage CI gate scoped to diff (90% on new code) plus mutation testing on critical modules. The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

**Ефективно для:** команд, що оперують цим артефактом регулярно і потребують детермінованого формату плюс перевірюваного результату.

## Applies If (ALL must hold)

- The project has a test runner emitting a coverage report (pytest-cov, c8, vitest --coverage).
- CI runs the test suite on every PR.
- The team has agreed branch coverage is the metric, not line.
- A baseline coverage % is known (run baseline first if not).

## Skip If (ANY kills it)

- Project is prototype-stage with no stable test suite.
- Test suite is integration-only (branch coverage uninformative on thin shims).
- Codebase is mostly framework boilerplate (Django admin pages, generated migrations) where coverage is meaningless.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Output target path | string | constitution / SDD spec |
| Owner (role:person) | string | team roster |
| Trigger event | event/threshold/schedule | constitution |
| Evidence anchor (URL / ticket / commit) | string | upstream context |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/api-testing` | Test suite this coverage measures. |
| `free/dev/software-developer/django-pytest` | Runner pattern this configures. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules specific to code-coverage | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/04-procedure.xml` | medium | Step-by-step procedure (when complexity >= medium) | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree from observable inputs to a rule conclusion | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold the output skeleton | sonnet | Mechanical, deterministic. |
| Refine domain-specific content | opus | Needs judgement. |
| Validate against output contract | sonnet | Schema check, deterministic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/coverage.toml` | pytest-cov branch-coverage config with diff-cover gate. |
| `templates/diff-cover-ci.sh` | CI step: produce coverage.xml then run diff-cover --fail-under=90. |
| `templates/jest.coverage.js` | Jest/Vitest branch-coverage config for JS/TS suites. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-coverage.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

- [[api-testing]] — see methodology AGENTS.md for context.
- [[code-review]] — see methodology AGENTS.md for context.
- [[django-pytest]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.
