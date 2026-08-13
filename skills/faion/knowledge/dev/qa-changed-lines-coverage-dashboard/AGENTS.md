# Changed-Lines (Diff) Coverage Dashboard

## Summary

**One-sentence:** Configure CI to report coverage only on lines changed in the PR diff, render it as a PR comment with per-file gauges, and treat that number — not whole-repo coverage — as the team's coverage target.

**One-paragraph:** Whole-repo coverage is the most-gamed metric in testing. A team can hit 80% repo coverage by piling structural tests on already-tested code while new features ship un-covered. Diff coverage cuts through the noise: for THIS PR, what percentage of the lines you added or changed is actually exercised by a test? AI-generated test PRs especially benefit from this measure because they often add many tests around already-covered code while leaving the new business logic thin. Mechanism: configure the coverage tool (coverage.py, jest --coverage, c8, JaCoCo) to emit lcov/coverage.xml, run a diff-coverage tool (diff-cover, codecov diff, gocover-cobertura + diff), publish a PR comment with per-file changed-lines coverage, gate merge on a per-file threshold (default 80% on changed lines), and dashboard the trend over time. Primary output: a CI config + a PR-comment template + a `coverage-diff.yml` policy file.

**Ефективно для:**

- Teams gaming whole-repo coverage by testing already-tested code.
- AI-assisted PRs that add tests but leave new business logic thin.
- Migrating from coverage-as-vanity-metric to coverage-as-merge-gate.
- Setting up a per-file gate where billing or auth code needs a higher floor.
- Producing a monthly trend you can actually review and act on.

## Applies If (ALL must hold)

- Repo runs unit and/or integration tests in CI with coverage instrumentation already enabled.
- PR-based workflow with merges to a main branch.
- The team currently looks at coverage (or could be persuaded to).
- One of the supported language stacks (coverage.py, jest/c8/nyc, JaCoCo, Go cover, coverlet, simplecov, pcov/Xdebug).

## Skip If (ANY kills it)

- Coverage instrumentation is broken or unreliable on this stack — fix that first.
- Repo has 0 baseline coverage AND no tests on main — adding diff coverage as a blocker rejects every PR; tackle baseline coverage first.
- Tests run only on schedule, not per-PR — wire PR-time tests first.
- Monorepo with mixed languages and no per-language coverage runner — set up per-language gates before adopting a unified dashboard.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Coverage report from CI | lcov / coverage.xml / jacoco.xml | engineering |
| PR-comment automation | GitHub Actions / GitLab CI / Bitbucket Pipelines | engineering |
| Diff definition | `git diff --merge-base origin/main` or equivalent | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-ac-to-assertion-mapping]] | Diff coverage answers "did you test the new code"; AC mapping answers "did you test the right behaviour". |
| [[qa-risk-matrix-method]] | The risk matrix drives per-file threshold overrides (higher in billing, lower in scripts). |
| [[qa-exploratory-charter-template]] | What diff coverage cannot catch — exploratory sessions cover that gap. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + skip rule: diff-only as the gate, per-file threshold, no full-repo deception, trend dashboard, exclusion discipline | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for coverage-diff.yml + PR-comment + dashboard + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: emit lcov, run diff-cover, publish PR comment, per-file gate, trend dashboard | ~800 |
| `content/05-examples.xml` | essential | Worked example: Python repo wiring diff-cover with billing override | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `diff_extraction` | haiku | Deterministic via git diff. |
| `coverage_report_parsing` | haiku | Tool-specific parser; no judgement. |
| `per_file_threshold_proposal` | sonnet | Bounded judgement on which files deserve which floor. |
| `dashboard_layout_design` | sonnet | Decide which trends + cohorts the team will actually read. |

## Templates

| File | Purpose |
|------|---------|
| `templates/coverage-diff.yml` | Policy file with per-file thresholds, exclusion list with reasons, and the report_full_repo_trend toggle. |
| `templates/pr-comment.md` | PR-comment template with per-file gauges and trend link. |
| `templates/dashboard.json` | Grafana / Datadog dashboard config for the trend. |
| `templates/_smoke-test.json` | Minimum viable artefact for validator self-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-changed-lines-coverage-dashboard.py` | Validate the diff-coverage artefact against `content/02-output-contract.xml` schema. | Pre-merge gate; on PR open. |

## Related

- [[qa-ac-to-assertion-mapping]]
- [[qa-risk-matrix-method]]
- [[qa-exploratory-charter-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs — coverage-instrumentation status, baseline coverage, per-PR test runs, language coverage support — onto a rule id from `content/01-core-rules.xml`. Walk it before adopting the gate so a broken instrumentation does not become the team's blocker.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/coverage-diff.yml`

```yaml
default_threshold: 80
overrides:
  - paths: ["billing/**", "checkout/**"]
    threshold: 90
    reason: money-touching code needs a higher coverage floor
  - paths: ["auth/**", "security/**"]
    threshold: 90
    reason: security-critical paths must be tested on every change
  - paths: ["scripts/**", "tools/**"]
    threshold: 0
    reason: ops scripts intentionally exempt from the merge gate
  - paths: ["migrations/**", "**/__init__.py"]
    threshold: 0
    reason: generated or near-empty files have no meaningful coverage
report_full_repo_trend: true
```

### `templates/dashboard.json`

```json
{
  "title": "Diff coverage trend",
  "panels": [
    {
      "type": "stat",
      "title": "Median diff coverage (7d)",
      "metric": "median_diff_coverage_7d"
    },
    {
      "type": "stat",
      "title": "Median diff coverage (30d)",
      "metric": "median_diff_coverage_30d"
    },
    {
      "type": "table",
      "title": "Low coverage files",
      "metric": "low_coverage_files"
    },
    {
      "type": "stat",
      "title": "Exclusion list size",
      "metric": "exclusion_list_size"
    }
  ],
  "review_cadence": "monthly testing meeting"
}
```

### `templates/_smoke-test.json`

```json
{
  "policy": {
    "default_threshold": 80,
    "overrides": [
      {
        "paths": [
          "billing/**"
        ],
        "threshold": 90,
        "reason": "money-touching code needs higher floor"
      }
    ],
    "report_full_repo_trend": true
  },
  "pr_comment": {
    "headline_metric": "diff_coverage_percent",
    "per_file": [
      {
        "path": "src/signup.py",
        "percent": 92,
        "gate_pass": true
      }
    ],
    "full_repo_trend_line": "trend: 78.4% (-0.1pp)",
    "merge_gate_verdict": "pass"
  },
  "dashboard": {
    "timestamp": "2026-05-23T10:00:00Z",
    "median_diff_coverage_7d": 84.2,
    "median_diff_coverage_30d": 82.7,
    "low_coverage_files": [
      "src/legacy/forms.py"
    ],
    "exclusion_list_size": 4
  }
}
```
