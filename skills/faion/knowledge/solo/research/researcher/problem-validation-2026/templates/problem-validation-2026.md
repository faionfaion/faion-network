<!--
purpose: Markdown skeleton for a Problem Validation 2026 artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/problem-validation-2026.json.
token-budget-impact: ~250 tokens.
-->

# Problem Validation 2026 — &lt;artefact_id&gt;

- **hypothesis** (string): &lt;problem hypothesis under test&gt;
- **evidence_ledger** (array): &lt;≥10 entries sorted by tier with citation + signal_type&gt;
- **cold_respondent_count** (integer): &lt;count of non-network respondents (≥3 tier-1/2 required for validated)&gt;
- **verdict** (string): &lt;one of: validated | hypothesis | invalidated&gt;
- **next_revalidation_due** (date): &lt;ISO date 90 days from last_reviewed&gt;
- **owner** (string): &lt;named researcher&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
