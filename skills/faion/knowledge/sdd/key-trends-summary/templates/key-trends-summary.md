<!--
purpose: Markdown skeleton for a Key Trends Summary 2025-2026 artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/key-trends-summary.json.
token-budget-impact: ~250 tokens.
-->

# Key Trends Summary 2025-2026 — &lt;artefact_id&gt;

- **report_id** (string): &lt;stable id&gt;
- **trends** (array): &lt;exactly 6 trends with name + source + implication&gt;
- **loaded_at** (datetime): &lt;ISO datetime&gt;
- **next_refresh_due** (date): &lt;loaded_at + 90 days&gt;
- **audience** (array): &lt;named roles&gt;
- **owner** (string): &lt;named author&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
