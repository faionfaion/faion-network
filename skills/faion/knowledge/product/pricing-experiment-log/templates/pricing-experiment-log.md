<!--
purpose: Markdown skeleton for a Pricing Experiment Log artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/pricing-experiment-log.json.
token-budget-impact: ~250 tokens.
-->

# Pricing Experiment Log — <artefact_id>

- **experiment_id** (string): <unique id>
- **hypothesis** (string): <falsifiable claim with numeric expectation>
- **toggle** (object): <before/after pricing config>
- **baseline** (object): <mrr + conversion% at toggle_at>
- **measurement_window** (object): <ISO start/end locked pre-toggle>
- **observed** (object): <post-window mrr + conversion%>
- **decision** (string): <keep | revert | iterate>
- **evidence_links** (array): <Stripe + dashboard URLs>
- **owner** (string): <named owner>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
