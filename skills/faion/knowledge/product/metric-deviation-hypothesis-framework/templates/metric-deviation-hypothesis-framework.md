<!--
purpose: Markdown skeleton for a Metric Deviation Hypothesis Framework artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/metric-deviation-hypothesis-framework.json.
token-budget-impact: ~250 tokens.
-->

# Metric Deviation Hypothesis Framework — <artefact_id>

- **metric_name** (string): <named metric>
- **baseline** (object): <baseline value + window>
- **deviation_magnitude** (string): <σ or % vs baseline>
- **time_window** (object): <ISO start/end>
- **hypotheses** (array): <≥3 ranked causal hypotheses with detector + probability>
- **next_checks** (array): <ranked check list with P(falsify) and cost>
- **owner** (string): <named human owner>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
