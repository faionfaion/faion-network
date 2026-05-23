<!--
purpose: Markdown skeleton for a User Interviews artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/user-interviews.json.
token-budget-impact: ~250 tokens.
-->

# User Interviews — &lt;artefact_id&gt;

- **session_id** (string): &lt;stable id&gt;
- **respondent** (object): &lt;Pnnn + cold/warm flag&gt;
- **script_used** (string): &lt;path to Mom Test script&gt;
- **transcript_path** (string): &lt;path to diarized transcript&gt;
- **behavioural_ask_outcome** (string): &lt;yes-with-evidence | no | pending&gt;
- **insights** (array): &lt;≥1 insight with frequency_count ≥1 and citation&gt;
- **owner** (string): &lt;named researcher&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
