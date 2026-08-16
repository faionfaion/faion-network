<!--
purpose: Markdown skeleton for a Daily Ship Rubric artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/daily-ship-rubric.json.
token-budget-impact: ~250 tokens.
-->

# Daily Ship Rubric — <artefact_id>

- **date** (date): <iso_date>
- **operator** (string): <named_human>
- **backlog_item** (string): <task_id>
- **gates** (object): <5 binary gates: spec/code/tests/deploy/customer_visible>
- **verdict** (string): <ship_no_ship>
- **note** (string): <≤200 char free-text>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
