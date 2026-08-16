<!--
purpose: Markdown skeleton for a OKR Setting artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/okr-setting.json.
token-budget-impact: ~250 tokens.
-->

# OKR Setting — <artefact_id>

- **quarter** (string): <yyyy-Qn>
- **quarter_dates** (object): <ISO start/end>
- **objectives** (array): <≤3 objects each with title + owner + KRs[]>
- **biweekly_checkin** (object): <day_of_week + time + recurrence>
- **owner** (string): <named owner (overall)>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
