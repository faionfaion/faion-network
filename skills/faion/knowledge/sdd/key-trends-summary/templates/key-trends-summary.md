<!--
purpose: Markdown skeleton for a Key Trends Summary 2025-2026 artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/key-trends-summary.json.
token-budget-impact: ~250 tokens.
-->

# Key Trends Summary 2025-2026 — <artefact_id>

- **report_id** (string): <stable id>
- **trends** (array): <exactly 6 trends with name + source + implication>
- **loaded_at** (datetime): <ISO datetime>
- **next_refresh_due** (date): <loaded_at + 90 days>
- **audience** (array): <named roles>
- **owner** (string): <named author>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
