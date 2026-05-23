<!--
purpose: Markdown skeleton for a Outcome Based Roadmaps artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/outcome-based-roadmaps.json.
token-budget-impact: ~250 tokens.
-->

# Outcome Based Roadmaps — &lt;artefact_id&gt;

- **quarter** (string): &lt;yyyy-Qn&gt;
- **outcomes** (array): &lt;≤3 outcome objects with target metrics + opportunities[]&gt;
- **solutions** (array): &lt;linked to opportunities with confidence + delivery_window_month_range&gt;
- **public_url** (string): &lt;stakeholder-facing URL&gt;
- **quarter_review** (object): &lt;shipped/slipped lists + adjustments&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
