<!--
purpose: Markdown skeleton for a Problem Validation 2026 artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/problem-validation-2026.json.
token-budget-impact: ~250 tokens.
-->

# Problem Validation 2026 — <artefact_id>

- **hypothesis** (string): <problem hypothesis under test>
- **evidence_ledger** (array): <≥10 entries sorted by tier with citation + signal_type>
- **cold_respondent_count** (integer): <count of non-network respondents (≥3 tier-1/2 required for validated)>
- **verdict** (string): <one of: validated | hypothesis | invalidated>
- **next_revalidation_due** (date): <ISO date 90 days from last_reviewed>
- **owner** (string): <named_researcher>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
