<!--
purpose: Markdown skeleton for a MVP Instrumentation Checklist artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/mvp-instrumentation-checklist.json.
token-budget-impact: ~250 tokens.
-->

# MVP Instrumentation Checklist — &lt;artefact_id&gt;

- **product_name** (string): &lt;named product&gt;
- **acquire** (object): &lt;event_name + dashboard_segment&gt;
- **activate** (object): &lt;event_name + dashboard_segment&gt;
- **retain** (object): &lt;event_name + dashboard_segment&gt;
- **revenue** (object): &lt;event_name + dashboard_segment&gt;
- **dashboard_url** (string): &lt;public URL&gt;
- **launch_gated** (boolean): &lt;true means checklist gates launch event&gt;
- **owner** (string): &lt;named human owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
