<!--
purpose: Markdown skeleton for a Backlog Management artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/backlog-management.json.
token-budget-impact: ~250 tokens.
-->

# Backlog Management — <artefact_id>

- **backlog_url** (string): <tracker_url>
- **buckets** (object): <ready/upcoming/backlog/icebox counts>
- **ready_items** (array): <items in Ready bucket with type, story, AC, estimate, source>
- **type_distribution** (object): <feature/bug/tech_debt/research counts>
- **grooming_cadence** (object): <day_of_week + duration_hours>
- **prioritisation_method** (string): <RICE | MoSCoW | stack>
- **archive_proposal_count** (integer): <items proposed for archive this grooming>
- **owner** (string): <owner_full_name>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
