<!--
purpose: Markdown skeleton for a Code Review Cycle artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/code-review-cycle.json.
token-budget-impact: ~250 tokens.
-->

# Code Review Cycle — &lt;artefact_id&gt;

- **pr_id** (string): &lt;PR or branch id&gt;
- **prescreen_findings** (array): &lt;AI pre-screen list&gt;
- **reviewer_findings** (array): &lt;parallel reviewer findings&gt;
- **merged_findings** (array): &lt;deduplicated unified list&gt;
- **block_count** (integer): &lt;count of BLOCK findings&gt;
- **reflexion_writeback** (array): &lt;{file, entry} pairs written to memory&gt;
- **verdict** (string): &lt;merge-ready | block-on-human&gt;
- **owner** (string): &lt;named human reviewer&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
