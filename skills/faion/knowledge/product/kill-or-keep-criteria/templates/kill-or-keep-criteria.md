<!--
purpose: Markdown skeleton for a Kill Or Keep Criteria artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/kill-or-keep-criteria.json.
token-budget-impact: ~250 tokens.
-->

# Kill Or Keep Criteria — <artefact_id>

- **project_name** (string): <named side-project>
- **mrr_snapshot** (number): <current MRR in USD>
- **traffic_snapshot** (number): <current monthly visits>
- **joy_score** (integer): <1-10 last-7-days self-rating>
- **opportunity_cost_candidate** (string): <named alternative bet>
- **evidence_links** (object): <URL/ticket per floor>
- **verdict** (string): <kill | keep (binary)>
- **next_action** (string): <concrete action attached to verdict>
- **template_version** (string): <kill-criteria-template version pinned>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
