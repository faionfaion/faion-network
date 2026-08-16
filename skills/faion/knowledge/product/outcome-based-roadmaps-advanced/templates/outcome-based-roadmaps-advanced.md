<!--
purpose: Markdown skeleton for a Outcome Based Roadmaps Advanced artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/outcome-based-roadmaps-advanced.json.
token-budget-impact: ~250 tokens.
-->

# Outcome Based Roadmaps Advanced — <artefact_id>

- **horizon** (object): <ISO start/end across ≥2 quarters>
- **swim_lanes** (array): <per-product lanes ≥2>
- **outcomes_by_quarter** (object): <quarter → outcomes[]>
- **dependency_edges** (array): <from/to/type/rationale objects>
- **confidence_decay_applied** (boolean): <true means decay applied unless cited>
- **quarter_reviews** (array): <per closed quarter review entry>
- **owner** (string): <named owner>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
