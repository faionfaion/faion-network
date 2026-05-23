<!--
purpose: Markdown skeleton for a Mistake Memory artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/mistake-memory.json.
token-budget-impact: ~250 tokens.
-->

# Mistake Memory — &lt;artefact_id&gt;

- **mistake_id** (string): &lt;stable id (MM-001..)&gt;
- **severity** (string): &lt;low | medium | high | critical&gt;
- **what_happened** (string): &lt;≤500 chars&gt;
- **five_whys** (array): &lt;≥3 levels&gt;
- **prevention** (string): &lt;concrete action&gt;
- **ci_rule_created** (boolean): &lt;true on second occurrence&gt;
- **occurrence_count** (integer): &lt;≥1&gt;
- **owner** (string): &lt;named author&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
