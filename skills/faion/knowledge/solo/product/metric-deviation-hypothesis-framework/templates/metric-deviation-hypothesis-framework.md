<!--
purpose: Markdown skeleton for a Metric Deviation Hypothesis Framework artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/metric-deviation-hypothesis-framework.json.
token-budget-impact: ~250 tokens.
-->

# Metric Deviation Hypothesis Framework — &lt;artefact_id&gt;

- **metric_name** (string): &lt;named metric&gt;
- **baseline** (object): &lt;baseline value + window&gt;
- **deviation_magnitude** (string): &lt;σ or % vs baseline&gt;
- **time_window** (object): &lt;ISO start/end&gt;
- **hypotheses** (array): &lt;≥3 ranked causal hypotheses with detector + probability&gt;
- **next_checks** (array): &lt;ranked check list with P(falsify) and cost&gt;
- **owner** (string): &lt;named human owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
