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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/coverage.toml`

```toml
# Paste under [tool] in pyproject.toml
# Adjust source = ["src"] to match your package directory.

[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/migrations/*",
    "*/conftest.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
]
fail_under = 80
show_missing = true

[tool.coverage.html]
directory = "htmlcov"
```

### `templates/diff-cover-ci.sh`

```bash
# scripts/diff-cover-ci.sh
# Run pytest with branch coverage, then gate new-code coverage via diff-cover.
# Usage: bash scripts/diff-cover-ci.sh [base-branch]
# Exits non-zero if new-code coverage is below 90%.
set -euo pipefail

BASE_BRANCH="${1:-origin/main}"

echo "==> Running pytest with coverage..."
pytest --cov=src --cov-branch --cov-report=xml --cov-report=term-missing

echo "==> Running diff-cover against ${BASE_BRANCH}..."
diff-cover coverage.xml \
  --compare-branch="${BASE_BRANCH}" \
  --fail-under=90 \
  --html-report diff-coverage.html

echo "==> diff-coverage report: diff-coverage.html"
```

### `templates/jest.coverage.js`

```javascript
// jest.config.js — coverage thresholds with global + per-directory gates.
// Adjust collectCoverageFrom globs to match your project structure.
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
    '!src/**/*.test.{ts,tsx}',
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    // Raise threshold for business-critical directories
    './src/services/': {
      branches: 90,
      functions: 90,
      lines: 90,
    },
  },
};
```
