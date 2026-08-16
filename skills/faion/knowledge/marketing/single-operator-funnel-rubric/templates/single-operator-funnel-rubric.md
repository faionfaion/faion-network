<!--
purpose: Markdown skeleton for a Single Operator Funnel Rubric artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/single-operator-funnel-rubric.json.
token-budget-impact: ~250 tokens.
-->

# Single Operator Funnel Rubric — <artefact_id>

- **week_iso** (string): <ISO week tag (e.g., 2026-W22)>
- **operator** (string): <named single owner of the rubric>
- **stages** (array): <exactly 4 entries: visit, signup, paid, retained>
- **broken_stage** (enum): <one of visit|signup|paid|retained>
- **next_action** (string): <single committed investigation for next week>
- **time_spent_min** (integer): <≤20 minutes>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
