<!--
purpose: Markdown skeleton for a Kill Criteria Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/kill-criteria-template.json.
token-budget-impact: ~250 tokens.
-->

# Kill Criteria Template — &lt;artefact_id&gt;

- **bet_name** (string): &lt;named bet / product&gt;
- **launch_date** (date): &lt;ISO date of launch event&gt;
- **primary_metric** (string): &lt;single metric (MRR | MAU | signups | joy_score)&gt;
- **primary_metric_threshold** (number): &lt;numeric floor — below this triggers kill&gt;
- **baseline_snapshot** (object): &lt;current value of primary metric at write time&gt;
- **review_dates** (array): &lt;calendared review dates (≥1)&gt;
- **owner** (string): &lt;named human owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
