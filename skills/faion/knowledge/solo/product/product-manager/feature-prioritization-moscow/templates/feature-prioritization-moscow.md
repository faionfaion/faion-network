<!--
purpose: Markdown skeleton for a Feature Prioritization MoSCoW artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/feature-prioritization-moscow.json.
token-budget-impact: ~250 tokens.
-->

# Feature Prioritization MoSCoW — &lt;artefact_id&gt;

- **cycle_id** (string): &lt;sprint / release id&gt;
- **capacity** (number): &lt;story points or hours&gt;
- **buckets** (object): &lt;must / should / could / wont arrays&gt;
- **tiebreaker_rule** (string): &lt;named rule&gt;
- **must_cap_pct** (number): &lt;0-60&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
