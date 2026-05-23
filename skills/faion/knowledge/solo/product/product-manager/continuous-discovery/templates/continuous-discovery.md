<!--
purpose: Markdown skeleton for a Continuous Discovery artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/continuous-discovery.json.
token-budget-impact: ~250 tokens.
-->

# Continuous Discovery — &lt;artefact_id&gt;

- **outcome** (string): &lt;named outcome / KPI&gt;
- **touchpoints** (array): &lt;≥1/week, each with date, customer_id, summary&gt;
- **opportunity_tree** (object): &lt;outcome → opportunities → solutions&gt;
- **assumption_tests** (array): &lt;≥1 per opportunity, each falsifiable&gt;
- **decision_log** (array): &lt;≥1/week, each with rationale + cited touchpoint ids&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
