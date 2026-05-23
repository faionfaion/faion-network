<!--
purpose: Markdown skeleton for a Pattern Memory artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/pattern-memory.json.
token-budget-impact: ~250 tokens.
-->

# Pattern Memory — &lt;artefact_id&gt;

- **pattern_id** (string): &lt;stable id (PM-001..)&gt;
- **title** (string): &lt;pattern name&gt;
- **confidence** (number): &lt;0.5..0.95&gt;
- **contexts_used** (array): &lt;≥2 with citation&gt;
- **rationale** (string): &lt;why it works&gt;
- **synced_to_claude_md** (boolean): &lt;true when confidence ≥0.8&gt;
- **occurrence_count** (integer): &lt;≥2&gt;
- **owner** (string): &lt;named author&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
