<!--
purpose: Markdown skeleton for a Solo Content Calendar Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/solo-content-calendar-template.json.
token-budget-impact: ~250 tokens.
-->

# Solo Content Calendar Template — <artefact_id>

- **operator** (string): <named_accountable_owner>
- **rows** (array): <exactly 12 rows with week_iso + pain_ref + asset_type + channel + status>
- **primary_channel** (enum): <seo|newsletter|x|linkedin|build-in-public>
- **quarterly_review_date** (date): <ISO date for retirement audit>
- **friday_gate_enabled** (boolean): <must be true>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
