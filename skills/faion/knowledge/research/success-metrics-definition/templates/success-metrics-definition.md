<!--
purpose: Markdown skeleton for a Success Metrics Definition artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/success-metrics-definition.json.
token-budget-impact: ~250 tokens.
-->

# Success Metrics Definition — &lt;artefact_id&gt;

- **north_star** (object): &lt;metric + business outcome link + owner&gt;
- **aarrr_kpis** (array): &lt;≤5 KPIs partitioned across acquisition/activation/retention/referral/revenue&gt;
- **baselines** (object): &lt;current value per KPI&gt;
- **targets** (object): &lt;target value + window per KPI&gt;
- **vanity_excluded** (array): &lt;vanity metrics explicitly excluded&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
