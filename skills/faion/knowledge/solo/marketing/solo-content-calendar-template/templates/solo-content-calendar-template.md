<!--
purpose: Markdown skeleton for a Solo Content Calendar Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/solo-content-calendar-template.json.
token-budget-impact: ~250 tokens.
-->

# Solo Content Calendar Template — &lt;artefact_id&gt;

- **operator** (string): &lt;named accountable owner&gt;
- **rows** (array): &lt;exactly 12 rows with week_iso + pain_ref + asset_type + channel + status&gt;
- **primary_channel** (enum): &lt;seo|newsletter|x|linkedin|build-in-public&gt;
- **quarterly_review_date** (date): &lt;ISO date for retirement audit&gt;
- **friday_gate_enabled** (boolean): &lt;must be true&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
