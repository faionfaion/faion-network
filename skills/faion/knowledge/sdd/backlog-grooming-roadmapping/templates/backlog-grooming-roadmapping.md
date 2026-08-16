<!--
purpose: Markdown skeleton for a Backlog Grooming and Roadmapping artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/backlog-grooming-roadmapping.json.
token-budget-impact: ~250 tokens.
-->

# Backlog Grooming and Roadmapping — <artefact_id>

- **backlog_items** (array): <≥10 with score + rationale + status>
- **p0_items** (array): <≤3>
- **scoring_framework** (string): <RICE | MoSCoW>
- **now_items** (array): <currently in flight>
- **next_items** (array): <next horizon>
- **later_items** (array): <later horizon>
- **last_groomed_at** (datetime): <ISO datetime>
- **owner** (string): <named PM>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
