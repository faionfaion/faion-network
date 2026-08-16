<!--
purpose: Markdown skeleton for a Mistake Memory artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/mistake-memory.json.
token-budget-impact: ~250 tokens.
-->

# Mistake Memory — <artefact_id>

- **mistake_id** (string): <stable id (MM-001..)>
- **severity** (string): <low | medium | high | critical>
- **what_happened** (string): <≤500 chars>
- **five_whys** (array): <≥3 levels>
- **prevention** (string): <concrete action>
- **ci_rule_created** (boolean): <true on second occurrence>
- **occurrence_count** (integer): <≥1>
- **owner** (string): <named author>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
