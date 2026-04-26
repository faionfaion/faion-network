# Code Coverage

## Summary

Coverage measures which lines and branches execute during tests. Use branch coverage (not line-only)
as the gate metric, enforce it on diffs (new code), set per-module thresholds via `diff-cover`, and
pair with mutation testing on critical modules to validate assertion quality.

## Why

High line coverage can coexist with completely missing branches and zero-assertion tests. Branch
coverage + diff gating closes the two most common loopholes: the "test exists but asserts nothing"
gap and the "legacy code drags total down" excuse. Mutation testing (`mutmut`) is the only reliable
way to distinguish coverage that tests behavior from coverage that merely executes lines.

## When To Use

- Setting a CI gate on new-code diff coverage (not absolute repo total)
- Identifying critical untested paths in legacy code prior to refactor
- Pre-release: surface modules below threshold, prioritize test work there
- Code review: confirm new code is covered without chasing 100% globally
- Onboarding tests for a third-party library wrapper before upgrading the dep

## When NOT To Use

- As the primary quality metric — 100% coverage with no assertions is worse than 60% with rich ones
- Generated code (migrations, OpenAPI clients, protobuf stubs) — exclude in `.coveragerc`
- UI / E2E smoke tests where flakiness outweighs coverage signal
- Single-file scripts or spike code — instrumentation overhead not justified

## Content

| File | What's inside |
|------|---------------|
| `content/01-coverage-types.xml` | Line vs branch vs path vs condition coverage; why branch is the practical floor |
| `content/02-tooling.xml` | pytest-cov config, jest/vitest thresholds, CI workflow, `diff-cover` gating |
| `content/03-antipatterns.xml` | Coverage gaming, `pragma: no cover` abuse, parallel-run data loss, async pitfalls |

## Templates

| File | Purpose |
|------|---------|
| `templates/coverage.toml` | `[tool.coverage.run/report]` block for `pyproject.toml` |
| `templates/jest.coverage.js` | Jest `coverageThreshold` config with global + per-directory thresholds |
| `templates/diff-cover-ci.sh` | CI script: run pytest + `diff-cover --fail-under=90` vs `origin/main` |
