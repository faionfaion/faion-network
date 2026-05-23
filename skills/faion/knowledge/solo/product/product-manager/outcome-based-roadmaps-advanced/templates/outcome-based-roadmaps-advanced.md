<!--
purpose: Markdown skeleton for a Outcome Based Roadmaps Advanced artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/outcome-based-roadmaps-advanced.json.
token-budget-impact: ~250 tokens.
-->

# Outcome Based Roadmaps Advanced — &lt;artefact_id&gt;

- **horizon** (object): &lt;ISO start/end across ≥2 quarters&gt;
- **swim_lanes** (array): &lt;per-product lanes ≥2&gt;
- **outcomes_by_quarter** (object): &lt;quarter → outcomes[]&gt;
- **dependency_edges** (array): &lt;from/to/type/rationale objects&gt;
- **confidence_decay_applied** (boolean): &lt;true means decay applied unless cited&gt;
- **quarter_reviews** (array): &lt;per closed quarter review entry&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
