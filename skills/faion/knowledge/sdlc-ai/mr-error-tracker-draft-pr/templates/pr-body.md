<!--
purpose: Draft PR body for an error-tracker-triggered fix — alert link, root cause, test added, reviewer checklist.
consumes: the error-tracker alert and the located recent diff (see Prerequisites)
produces: draft PR body artefact
depends-on: content/02-output-contract.xml
token-budget-impact: ~140 tokens when filled
-->

## Sentry alert
<alert_url>

## Root cause (LLM-generated)
<root_cause_paragraph>

## Test added
`{test_file_path}::{test_function_name}`

## Reviewer checklist
- [ ] I have validated the patch addresses the alert above (not a near-duplicate).
- [ ] CI is green on the new regression test.
- [ ] The fix does not silently change public API or data shape.
- [ ] Severity-1 changes have a rollback plan or feature flag.

<!-- AUTO-DESCRIBE-START — managed by tracker; do not edit above this line -->
<!-- AUTO-DESCRIBE-END -->

## Notes for reviewer
<!-- Human-edited section; survives re-runs of the tracker template. -->
