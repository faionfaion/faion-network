<!--
purpose: PR description skeleton with idempotent AUTO-DESCRIBE block + human-notes block
consumes: PR body; bot run output
produces: config (PR template — pull_request_template.md)
depends-on: content/01-core-rules.xml (describe-block-idempotent)
token-budget-impact: low — ~150 tokens when loaded as context
-->
<!-- AUTO-DESCRIBE-START — managed by qodo /describe; do not edit -->

## Walkthrough
- {file_1}: {one_line_change_summary}
- {file_2}: {one_line_change_summary}

## Risk
{risk_level} — {risk_one_liner}

## Test plan
- {test_path_1}::{test_name_1}
- {test_path_2}::{test_name_2}

<!-- AUTO-DESCRIBE-END -->

## Notes for reviewer
<!-- HUMAN — survives re-runs of /describe -->

{free_form_human_notes}
