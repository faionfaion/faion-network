<!--
purpose: Canonical skeleton for the red-test-first bugfix workflow record.
consumes: An alert URL + reproducing input + a developer owner.
produces: A workflow-record file at .product/regression-records/<slug>.md.
depends-on: templates/header.yaml.
token-budget-impact: ~400 tokens to fill end-to-end.
-->
---
version: 0.1.0
owner: swe:<person>
last_reviewed: YYYY-MM-DD
alert_url: https://sentry.io/...
fix_pr_url: https://github.com/.../pull/...
---

# Alert

- kind: sentry | datadog | customer-ticket | log-aggregator
- url: <alert URL>
- reproducing input: <json | snippet>

# Red Test (committed FIRST)

- path: tests/regression/test_<slug>.py
- commit: <short hash>
- asserts:
  - <assertion 1>
  - <assertion 2>

# Fix

- pr_url: <PR URL>
- diff_lines: <int>
- approach: <one paragraph — why this is the smallest correct change>

# Verification

- ci_run_url: <CI run URL>
- passed: true|false

# Review

- cadence: monthly|quarterly
- next_review_at: YYYY-MM-DD
- outcome: <filled at the next review — alert reproduced again? yes/no>
