<!--
purpose: Markdown skeleton for a Feature Prioritization RICE artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/feature-prioritization-rice.json.
token-budget-impact: ~250 tokens.
-->

# Feature Prioritization RICE — &lt;artefact_id&gt;

- **scoring_round_id** (string): &lt;round id (e.g. 2026-Q2)&gt;
- **reach_unit** (string): &lt;named unit&gt;
- **effort_unit** (string): &lt;named unit&gt;
- **impact_anchors** (array): &lt;3 cited examples&gt;
- **rows** (array): &lt;feature objects with reach, impact, confidence, effort, source, rice_score&gt;
- **cut_line** (number): &lt;score threshold&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
