<!--
purpose: Markdown skeleton for a Feature Prioritization MoSCoW artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/feature-prioritization-moscow.json.
token-budget-impact: ~250 tokens.
-->

# Feature Prioritization MoSCoW — <artefact_id>

- **cycle_id** (string): <sprint / release id>
- **capacity** (number): <story points or hours>
- **buckets** (object): <must / should / could / wont arrays>
- **tiebreaker_rule** (string): <named rule>
- **must_cap_pct** (number): <0-60>
- **owner** (string): <named owner>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
