<!--
purpose: Markdown skeleton for a Daily Ship Rubric artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/daily-ship-rubric.json.
token-budget-impact: ~250 tokens.
-->

# Daily Ship Rubric — &lt;artefact_id&gt;

- **date** (date): &lt;ISO date&gt;
- **operator** (string): &lt;named human&gt;
- **backlog_item** (string): &lt;task id&gt;
- **gates** (object): &lt;5 binary gates: spec/code/tests/deploy/customer_visible&gt;
- **verdict** (string): &lt;ship | no-ship&gt;
- **note** (string): &lt;≤200 char free-text&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
