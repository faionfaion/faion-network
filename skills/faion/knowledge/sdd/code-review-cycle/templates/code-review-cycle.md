<!--
purpose: Markdown skeleton for a Code Review Cycle artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/code-review-cycle.json.
token-budget-impact: ~250 tokens.
-->

# Code Review Cycle — <artefact_id>

- **pr_id** (string): <PR or branch id>
- **prescreen_findings** (array): <AI pre-screen list>
- **reviewer_findings** (array): <parallel reviewer findings>
- **merged_findings** (array): <deduplicated unified list>
- **block_count** (integer): <count of BLOCK findings>
- **reflexion_writeback** (array): <{file, entry} pairs written to memory>
- **verdict** (string): <merge-ready | block-on-human>
- **owner** (string): <named human reviewer>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
