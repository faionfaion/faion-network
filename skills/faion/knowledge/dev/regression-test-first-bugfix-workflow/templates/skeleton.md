<!--
purpose: Canonical skeleton for the red-test-first bugfix workflow record.
consumes: An alert URL + payload-derived reproducing inputs + a developer owner.
produces: A workflow-record file at .product/regression-records/<slug>.md, matching content/02-output-contract.xml.
depends-on: templates/header.yaml.
token-budget-impact: ~500 tokens to fill end-to-end.
-->
---
version: 0.1.0
owner: swe:<owner_full_name>
last_reviewed: YYYY-MM-DD
alert_url: <alert_url>
fix_pr_url: <pr_url>
---

# Alert

- kind: sentry | datadog | customer-ticket | log-aggregator
- url: <alert_url>
- alert_id: <alert_id>
- observed_outcome: exception | wrong-output — <observed_outcome>
- side_effect: <row written / email sent / charge made, or none>
- reproducing_inputs (lifted from the alert payload, PII replaced field-by-field): <json_snippet>
- pii_substitutions: <field -> shape of the replacement, one per line>
- deterministic: true (same failure on 3 runs against the unfixed code)

# Red Test (committed FIRST)

- status: committed | pending
- path: tests/regression/test_<slug>.py
- commit: <short_hash> (test only; message carries the alert URL)
- commit_message_has_alert_url: true
- asserts (the alert's exception type / message fragment or wrong value):
  - <assertion_1>
  - <assertion_2>
- side_effect_asserts: <the side effect is absent>
- red_ci_run_url: <red_ci_run_url>
- failure_matches_alert: true
- stable_runs: 3
- if pending (hotfix): follow_up_ticket_url: <url>, due_at: <merged_at + 14 days at the latest>

# Fix

- pr_url: <pr_url>
- first_fix_commit: <fix_commit> (a separate commit on top of the red test)
- diff_lines: <diff_lines>
- touches_red_test_assertions: false
- hotfix: true | false
- refactor_pr_url: <separate PR, if any>
- approach: <one paragraph — why this is the smallest correct change>

# Verification

- ci_run_url: <ci_run_url>
- passed: true (read from CI, never from a local run)
- skipped_or_xfail: false

# Review

- merged_at: <merged_at>
- next_review_at: <next_review_at> (merged_at + 90 days)
- alert_resolved: true | false (false while a red test is pending)
- outcome (filled at the review): reviewed_at, regression_events_in_window, same_signature_new_issue
