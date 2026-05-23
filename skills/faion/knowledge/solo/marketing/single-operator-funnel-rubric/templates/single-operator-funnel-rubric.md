<!--
purpose: Markdown skeleton for a Single Operator Funnel Rubric artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/single-operator-funnel-rubric.json.
token-budget-impact: ~250 tokens.
-->

# Single Operator Funnel Rubric — &lt;artefact_id&gt;

- **week_iso** (string): &lt;ISO week tag (e.g., 2026-W22)&gt;
- **operator** (string): &lt;named single owner of the rubric&gt;
- **stages** (array): &lt;exactly 4 entries: visit, signup, paid, retained&gt;
- **broken_stage** (enum): &lt;one of visit|signup|paid|retained&gt;
- **next_action** (string): &lt;single committed investigation for next week&gt;
- **time_spent_min** (integer): &lt;≤20 minutes&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
