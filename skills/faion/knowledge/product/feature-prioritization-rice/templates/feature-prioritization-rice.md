<!--
purpose: Markdown skeleton for a Feature Prioritization RICE artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/feature-prioritization-rice.json.
token-budget-impact: ~250 tokens.
-->

# Feature Prioritization RICE — <artefact_id>

- **scoring_round_id** (string): <round id (e.g. 2026-Q2)>
- **reach_unit** (string): <named unit>
- **effort_unit** (string): <named unit>
- **impact_anchors** (array): <3 cited examples>
- **rows** (array): <feature objects with reach, impact, confidence, effort, source, rice_score>
- **cut_line** (number): <score threshold>
- **owner** (string): <named owner>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
