<!--
purpose: Markdown skeleton for a Pricing Experiment Log artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/pricing-experiment-log.json.
token-budget-impact: ~250 tokens.
-->

# Pricing Experiment Log — &lt;artefact_id&gt;

- **experiment_id** (string): &lt;unique id&gt;
- **hypothesis** (string): &lt;falsifiable claim with numeric expectation&gt;
- **toggle** (object): &lt;before/after pricing config&gt;
- **baseline** (object): &lt;mrr + conversion% at toggle_at&gt;
- **measurement_window** (object): &lt;ISO start/end locked pre-toggle&gt;
- **observed** (object): &lt;post-window mrr + conversion%&gt;
- **decision** (string): &lt;keep | revert | iterate&gt;
- **evidence_links** (array): &lt;Stripe + dashboard URLs&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
