<!--
purpose: Markdown skeleton for a MVP Instrumentation Checklist artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/mvp-instrumentation-checklist.json.
token-budget-impact: ~250 tokens.
-->

# MVP Instrumentation Checklist — <artefact_id>

- **product_name** (string): <named_product>
- **acquire** (object): <event_name + dashboard_segment>
- **activate** (object): <event_name + dashboard_segment>
- **retain** (object): <event_name + dashboard_segment>
- **revenue** (object): <event_name + dashboard_segment>
- **dashboard_url** (string): <public_url>
- **launch_gated** (boolean): <true means checklist gates launch event>
- **owner** (string): <named_human_owner>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
