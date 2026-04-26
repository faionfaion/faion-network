# Code Coverage

## Summary

A metric family (line, branch, path, condition) for identifying untested code paths. Use branch coverage as the minimum signal; combine with diff-coverage on changed lines to avoid legacy gaps blocking PRs. Target: 80% branch coverage globally, 90%+ on critical paths (auth, billing, data integrity). Coverage measures execution, not assertion strength — pair with mutation testing for critical modules.

## Why

Coverage reports make untested branches visible so an agent or developer can write targeted tests. Branch coverage reveals untested else-branches that line coverage misses. Diff-coverage focuses the gate on new code, so accumulated legacy gaps do not block ongoing work. Martin Fowler's canonical note: coverage is a tool for finding gaps, not a goal — optimize for meaningful assertions, not numbers.

## When To Use

- Feeding coverage reports back to an LLM test-author to know which branches still lack tests.
- CI gate: enforce minimum diff-coverage on lines changed by a PR.
- Onboarding a new repo: run coverage once to map what is and is not tested.
- Targeted refactor planning: high-churn + low-coverage files are the first refactor candidates.

## When NOT To Use

- Tiny one-shot scripts with no test infrastructure — wiring coverage costs more than it returns.
- UI/visual code where snapshot/visual tests give better signal than line coverage.
- Generated/migration code — exclude from coverage, do not attempt to test.
- As a single quality KPI for performance reviews — Goodhart's law applies.

## Content

| File | What's inside |
|------|---------------|
| `content/01-types.xml` | Line vs branch vs path vs condition coverage; why branch is the default; tool config for Python and JS/TS. |
| `content/02-workflow.xml` | Coverage-driven test loop, diff-cover usage, CI/CD integration, exclusion rules, agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/coverage.pyproject.toml` | pyproject.toml coverage config: branch=true, omit list, fail_under=80, exclude_lines. |
| `templates/jest.coverage.config.js` | Jest coverage config: collectCoverageFrom, thresholds (global + per-dir), reporters. |
| `templates/diff-cov-report.sh` | Run pytest + diff-cover, emit per-file uncovered lines as agent-ready prompt fragments. |
