# Code Coverage

## Summary

**One-sentence:** Configures branch + diff coverage as a CI gate and emits a machine-readable uncovered-lines artefact that LLM test-author subagents can act on.

**One-paragraph:** Line coverage alone passes when an if-branch fires but its else-branch never runs — half the logic is untested with 100% on the dashboard. This methodology forces branch coverage on every project, enforces diff-cover on PRs so legacy gaps don't block ongoing work, sets per-directory thresholds (critical paths 90%+, glue code 70%), and produces a tiny JSON of uncovered lines per touched file so an LLM test-author can write targeted tests without parsing 100KB of XML. Fowler's anchor stays: coverage is a gap-finder, not a goal — the gate is the floor, mutation testing is the ceiling.

**Ефективно для:**

- Стартові проекти: налаштувати branch + diff-cover з нуля, без накопиченого боргу.
- Legacy-репо з низьким покриттям: diff-cover розблоковує нові PR без вимоги "довести покриття до 80% спочатку".
- AI-loop тест-генерації: jq-фільтр витягує лише непокриті рядки → ~2K токенів контексту замість 100K XML.
- Команди, яким нав'язали SaaS-coverage (Codecov), а вони хочуть звести залежність до GitHub-артефакта.

## Applies If (ALL must hold)

- Project has a working test runner (pytest, jest, vitest, go test, cargo test, etc.).
- CI runs on every PR and has write-access to publish artefacts / comments.
- A repo `main` (or `develop`) branch exists to diff against.

## Skip If (ANY kills it)

- One-off script / throwaway prototype — gating cost exceeds the value.
- UI-snapshot-heavy codebase where visual diff is the real signal (line coverage is misleading).
- Generated / migration code (ORM migrations, protobuf stubs) — exclude rather than try to cover.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Test runner config | `pyproject.toml` / `jest.config.js` / `vitest.config.ts` | repo root |
| CI workflow file | YAML | `.github/workflows/` |
| Critical-path manifest | Markdown list of dirs requiring ≥90% | repo `AGENTS.md` or docs |
| Baseline branch | git ref | `main` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Coverage is a foundational rubric — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: branch-required, diff-cover-on-pr, per-dir-thresholds, exclusion-policy, no-pragma-ratcheting, mutation-quarterly, extract-don't-paste | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for coverage-gate config + uncovered-lines extract | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: gaming, pragma-ratchet, threshold-lowering, async-config-gap | 700 |
| `content/04-procedure.xml` | essential | 5-step setup procedure from green-field to gating PR | 800 |
| `content/06-decision-tree.xml` | essential | Routing: language → tool → config-stack → gate-mode | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect_stack` | haiku | File-pattern matching; no inference required. |
| `write_config` | haiku | Filling a known template; deterministic. |
| `extract_uncovered` | haiku | `jq` / XPath transform over coverage XML. |
| `write_targeted_tests` | sonnet | Per-file generation with source pinned in context. |
| `mutation_review` | opus | Cross-file synthesis; quarterly batch only. |

## Templates

| File | Purpose |
|------|---------|
| `templates/coverage.pyproject.toml` | Python: branch=true, fail_under=80, exclude_lines |
| `templates/jest.coverage.config.js` | JS/TS: V8 provider, per-dir thresholds, lcov reporter |
| `templates/diff-cov-report.sh` | Runs pytest + diff-cover, emits per-file uncovered-lines prompt fragments |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[code-review-process]] — the gate this methodology produces runs inside the review process.
- [[refactoring-patterns]] — high-churn + low-coverage → first refactor candidates.

## Decision tree

See `content/06-decision-tree.xml`. The tree first branches on detected stack (Python / JS-TS / Go / Rust / mixed) → picks the canonical coverage tool → asks whether the repo is green-field or legacy. Green-field gets a single global threshold; legacy gets diff-cover only (so historical gaps do not block PRs). All leaves reference rules from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/coverage.pyproject.toml`

```toml
# Coverage configuration for pyproject.toml
# Copy the [tool.coverage.*] sections into your project's pyproject.toml

[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/migrations/*",
    "*/conftest.py",
    "*/manage.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
    "\\.\\.\\.",
]
fail_under = 80
show_missing = true

[tool.coverage.html]
directory = "htmlcov"

# pytest integration — add to [tool.pytest.ini_options]
# addopts = "--cov=src --cov-branch --cov-report=term-missing --cov-report=html --cov-fail-under=80"
```

### `templates/jest.coverage.config.js`

```javascript
// jest.config.js — coverage configuration
// Adjust collectCoverageFrom paths for your project structure.
/** @type {import('jest').Config} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  collectCoverage: true,
  coverageProvider: 'v8', // Native V8 — more accurate for ESM and async
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.ts',      // barrel re-exports — no logic to test
    '!src/**/*.test.{ts,tsx}',
    '!src/**/*.spec.{ts,tsx}',
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
    // Raise thresholds for critical paths:
    // './src/auth/': { branches: 90, functions: 90, lines: 90, statements: 90 },
    // './src/billing/': { branches: 90, functions: 90, lines: 90, statements: 90 },
  },
};
```

### `templates/diff-cov-report.sh`

```bash
#!/usr/bin/env bash
# diff-cov-report.sh — enforce diff-coverage and emit uncovered lines for agent.
# Usage: diff-cov-report.sh [base-branch] [target-percent]
# Example: diff-cov-report.sh origin/main 90
set -euo pipefail

BASE="${1:-origin/main}"
TARGET="${2:-90}"

# Run full test suite with branch coverage
pytest --cov=src --cov-branch --cov-report=xml -q

# Run diff-cover: fails if diff-coverage < TARGET
diff-cover coverage.xml \
  --compare-branch="$BASE" \
  --fail-under="$TARGET" \
  --markdown-report diff-cov.md \
  --json-report   diff-cov.json

echo ""
echo "## Agent-ready: uncovered changed lines per file"
jq -r '
  .src_stats | to_entries[]
  | select(.value.uncovered_lines | length > 0)
  | "FILE: \(.key)\nUNCOVERED_LINES: \(.value.uncovered_lines | join(","))\n"
' diff-cov.json
```
