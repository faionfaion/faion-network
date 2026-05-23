<!--
purpose: Markdown skeleton for a Single Interview Fast Loop Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/single-interview-fast-loop-template.json.
token-budget-impact: ~250 tokens.
-->

# Single Interview Fast Loop Template — &lt;artefact_id&gt;

- **loop_id** (string): &lt;stable id&gt;
- **decision_under_test** (string): &lt;the one decision the loop informs&gt;
- **must_asks** (array): &lt;3–5 past-tense questions&gt;
- **interview_at** (datetime): &lt;ISO datetime&gt;
- **synthesis_due_at** (datetime): &lt;interview_at + ≤36h&gt;
- **synthesis_outcome** (string): &lt;decide-yes | decide-no | park | re-interview&gt;
- **citation_path** (string): &lt;path to transcript in research repo&gt;
- **owner** (string): &lt;named researcher&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
