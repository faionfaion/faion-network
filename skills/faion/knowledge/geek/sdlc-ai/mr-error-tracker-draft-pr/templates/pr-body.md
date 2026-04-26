<!-- Required PR body skeleton for error-tracker → draft-PR pipeline.
     All four sections are mandatory; missing any one fails policy gate.
     Variables in {curly_braces} are filled by the agent at PR-open time. -->

## Sentry alert
{alert_url}

## Root cause (LLM-generated)
{root_cause_paragraph}

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
