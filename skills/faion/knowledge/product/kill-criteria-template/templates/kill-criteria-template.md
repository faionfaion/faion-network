<!--
purpose: Markdown skeleton for a Kill Criteria Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/kill-criteria-template.json.
token-budget-impact: ~250 tokens.
-->

# Kill Criteria Template — <artefact_id>

- **bet_name** (string): <named bet / product>
- **launch_date** (date): <ISO date of launch event>
- **primary_metric** (string): <single metric (MRR | MAU | signups | joy_score)>
- **primary_metric_threshold** (number): <numeric floor — below this triggers kill>
- **baseline_snapshot** (object): <current value of primary metric at write time>
- **review_dates** (array): <calendared review dates (≥1)>
- **owner** (string): <named human owner>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
