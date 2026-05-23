<!--
purpose: Markdown skeleton for a Kill Or Keep Criteria artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/kill-or-keep-criteria.json.
token-budget-impact: ~250 tokens.
-->

# Kill Or Keep Criteria — &lt;artefact_id&gt;

- **project_name** (string): &lt;named side-project&gt;
- **mrr_snapshot** (number): &lt;current MRR in USD&gt;
- **traffic_snapshot** (number): &lt;current monthly visits&gt;
- **joy_score** (integer): &lt;1-10 last-7-days self-rating&gt;
- **opportunity_cost_candidate** (string): &lt;named alternative bet&gt;
- **evidence_links** (object): &lt;URL/ticket per floor&gt;
- **verdict** (string): &lt;kill | keep (binary)&gt;
- **next_action** (string): &lt;concrete action attached to verdict&gt;
- **template_version** (string): &lt;kill-criteria-template version pinned&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
