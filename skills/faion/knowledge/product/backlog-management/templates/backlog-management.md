<!--
purpose: Markdown skeleton for a Backlog Management artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/backlog-management.json.
token-budget-impact: ~250 tokens.
-->

# Backlog Management — &lt;artefact_id&gt;

- **backlog_url** (string): &lt;tracker URL&gt;
- **buckets** (object): &lt;ready/upcoming/backlog/icebox counts&gt;
- **ready_items** (array): &lt;items in Ready bucket with type, story, AC, estimate, source&gt;
- **type_distribution** (object): &lt;feature/bug/tech_debt/research counts&gt;
- **grooming_cadence** (object): &lt;day_of_week + duration_hours&gt;
- **prioritisation_method** (string): &lt;RICE | MoSCoW | stack&gt;
- **archive_proposal_count** (integer): &lt;items proposed for archive this grooming&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
