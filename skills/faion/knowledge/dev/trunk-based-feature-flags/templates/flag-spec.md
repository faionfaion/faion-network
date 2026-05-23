<!--
purpose: Per-flag spec skeleton the author fills before the wrapping PR opens.
consumes: nothing — this IS the input form.
produces: flag-spec ready for the scorer to ingest.
depends-on: tracker integration that resolves the cleanup_ticket_id.
token-budget-impact: ~180 tokens when copied.
-->

# Flag spec — &lt;flag_id&gt;

## Identity
- artefact_id: ff-&lt;slug&gt;
- flag_id (== ticket slug):
- type: release | experiment | ops | permission
- dark_launch: true | false

## Ownership
- owner_email (named human, NOT a team alias):
- cleanup_ticket_id (filed in same session):
- cleanup_sla_date (typical: 30 days after planned 100% rollout):

## Ramp plan
| pct | gate (observable + threshold) |
|-----|-------------------------------|
| 1   | e.g. diff_rate &lt; 0.5 over 24h |
| 10  | e.g. diff_rate &lt; 0.5 AND error_rate at baseline |
| 50  | e.g. all clusters classified, sample &gt;= 10000 |
| 100 | e.g. sign-off recorded |

## Kill-switch
- kill_switch_tested: true | false
- kill_switch_test_run_id (CI run that flipped the flag off and verified legacy path):

## Versioning
- version: 1.0.0
- last_reviewed: YYYY-MM-DD
