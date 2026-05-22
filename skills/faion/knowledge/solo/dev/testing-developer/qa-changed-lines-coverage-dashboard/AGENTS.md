---
slug: qa-changed-lines-coverage-dashboard
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "a048fada4a40ef54"
summary: A diff-only coverage dashboard wired into PRs so the visible metric is changed-lines coverage (not whole-repo coverage) — the only honest signal of test investment per change.
tags: [coverage, diff-coverage, ci, qa, anti-coverage-gaming, dashboard]
---

# Changed-Lines (Diff) Coverage Dashboard

## Summary

**One-sentence:** Configure the CI to report coverage only on lines changed in the PR diff, render it as a PR comment with per-file gauges, and treat that number — not the whole-repo coverage — as the team's coverage target.

**One-paragraph:** Whole-repo coverage is the most-gamed metric in testing. A team can hit 80% repo coverage by piling structural tests on already-tested code while new features ship un-covered. Diff coverage cuts through the noise: for THIS PR, what percentage of the lines you added or changed is actually exercised by a test? AI-generated test PRs especially benefit from this measure because they often add many tests around already-covered code while leaving the new business logic thin. Mechanism: configure the coverage tool (coverage.py, jest --coverage, c8, JaCoCo) to emit lcov/coverage.xml, run a diff-coverage tool (diff-cover, codecov diff, gocover-cobertura + diff), publish a PR comment with per-file changed-lines coverage, gate merge on a per-file threshold (default 80% on changed lines), and dashboard the trend over time. Primary output: a CI config + a PR-comment template + a `coverage-diff.yml` policy file.

## Applies If (ALL must hold)

- repo runs unit and/or integration tests in CI with coverage instrumentation already enabled
- PR-based workflow with merges to a main branch
- the team currently looks at coverage (or could be persuaded to)
- one of the supported language stacks (Python coverage.py, Node jest/c8/nyc, Java JaCoCo, Go cover, C# coverlet, Ruby simplecov, PHP pcov / Xdebug)

## Skip If (ANY kills it)

- coverage instrumentation is broken or unreliable on this stack — fix that first
- repo has 0 baseline coverage AND no tests on main — adding diff coverage as a blocker will reject every PR; tackle baseline coverage first
- tests run only on schedule, not per-PR — wire PR-time tests first
- monorepo with mixed languages and no per-language coverage runner — set up per-language gates before adopting a unified dashboard

## Prerequisites

- working coverage report (lcov, coverage.xml, jacoco.xml) emitted by CI
- access to PR-comment automation (GitHub Actions, GitLab CI, Bitbucket Pipelines)
- a definition of the change set (typically `git diff --merge-base origin/main` in the PR)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/code-quality/mutation-testing-ci-gate` | Diff coverage is the first signal; mutation testing is the harder follow-up |
| `solo/dev/testing-developer/qa-ai-generated-test-audit-checklist` | Audit checklist uses diff coverage as one input |
| `pro/marketing/growth-marketer/conversion-tracking` | Sibling pattern of measuring deltas not totals |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: diff-only target, per-file gate, no full-repo deception, dashboard trend, exclusion list discipline | ~900 |
| `content/02-output-contract.xml` | essential | PR-comment schema, coverage-diff policy schema, dashboard schema | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: full-repo substitution, exclusion sprawl, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `diff_extraction` | haiku | Deterministic via git diff |
| `coverage_report_parsing` | haiku | Tool-specific parser; no judgment |
| `per_file_threshold_proposal` | sonnet | Cross-file bounded judgment on which files deserve which floor |

## Templates

| File | Purpose |
|------|---------|
| `templates/coverage-diff.yml` | Policy file with per-file thresholds and exclusion list |
| `templates/pr-comment.md` | PR-comment template with per-file gauges and trend link |
| `templates/dashboard.json` | Grafana / Datadog dashboard config for the trend |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/diff-cover-run.sh` | Wraps language-specific diff-cover tools, produces a unified JSON report | Per PR |
| `scripts/coverage-trend.py` | Pushes per-PR diff-coverage data to the dashboard backend | Per PR after merge |

## Related

- parent skill: `solo/dev/testing-developer/SKILL.md`
- peer methodologies: `pro/dev/code-quality/mutation-testing-ci-gate`, `solo/dev/testing-developer/qa-ai-generated-test-audit-checklist`
- external: [diff-cover (Bachman, OpenEdX)] · [Codecov diff-coverage docs] · [JaCoCo --diff-report] · [Karpathy 2019 critique of coverage-gaming]
