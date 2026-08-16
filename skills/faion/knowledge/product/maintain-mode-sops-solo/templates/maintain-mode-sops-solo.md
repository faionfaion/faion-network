<!--
purpose: Markdown skeleton for a Maintain Mode SOPs Solo artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/maintain-mode-sops-solo.json.
token-budget-impact: ~250 tokens.
-->

# Maintain Mode SOPs Solo — <artefact_id>

- **product_name** (string): <named product>
- **weekly_check** (object): <tasks + duration>
- **monthly_reconcile** (object): <tasks + duration>
- **quarterly_upgrade** (object): <tasks + duration>
- **on_call_rule** (object): <trigger + max_response_window_hours>
- **sunset_trigger** (string): <MRR / churn condition>
- **owner** (string): <named human owner>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
