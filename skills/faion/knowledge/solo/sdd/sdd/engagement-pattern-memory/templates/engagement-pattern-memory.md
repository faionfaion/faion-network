<!--
purpose: Markdown skeleton for a Engagement Pattern Memory artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/engagement-pattern-memory.json.
token-budget-impact: ~250 tokens.
-->

# Engagement Pattern Memory — &lt;artefact_id&gt;

- **engagement_id** (string): &lt;client / repo identifier&gt;
- **memory_file_path** (string): &lt;path to memory.md&gt;
- **repo_conventions** (object): &lt;linting / naming / commit format&gt;
- **reviewer_preferences** (object): &lt;per-named-reviewer preferences&gt;
- **deploy_quirks** (array): &lt;non-obvious deploy gotchas&gt;
- **recurring_traps** (array): &lt;≥1 trap with detector + fix&gt;
- **glossary** (object): &lt;client-specific terms&gt;
- **resolved_questions** (array): &lt;questions + resolution dates&gt;
- **owner** (string): &lt;named contractor&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
