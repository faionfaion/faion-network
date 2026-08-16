<!--
purpose: Markdown skeleton for a Continuous Discovery artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/continuous-discovery.json.
token-budget-impact: ~250 tokens.
-->

# Continuous Discovery — <artefact_id>

- **outcome** (string): <named outcome / KPI>
- **touchpoints** (array): <≥1/week, each with date, customer_id, summary>
- **opportunity_tree** (object): <outcome → opportunities → solutions>
- **assumption_tests** (array): <≥1 per opportunity, each falsifiable>
- **decision_log** (array): <≥1/week, each with rationale + cited touchpoint ids>
- **owner** (string): <named owner>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
