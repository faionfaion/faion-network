<!--
purpose: Markdown skeleton for a OKR Setting artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/okr-setting.json.
token-budget-impact: ~250 tokens.
-->

# OKR Setting — &lt;artefact_id&gt;

- **quarter** (string): &lt;yyyy-Qn&gt;
- **quarter_dates** (object): &lt;ISO start/end&gt;
- **objectives** (array): &lt;≤3 objects each with title + owner + KRs[]&gt;
- **biweekly_checkin** (object): &lt;day_of_week + time + recurrence&gt;
- **owner** (string): &lt;named owner (overall)&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
