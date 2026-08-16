<!--
purpose: Markdown skeleton for a Success Metrics Definition artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/success-metrics-definition.json.
token-budget-impact: ~250 tokens.
-->

# Success Metrics Definition — <artefact_id>

- **north_star** (object): <metric + business outcome link + owner>
- **aarrr_kpis** (array): <≤5 KPIs partitioned across acquisition/activation/retention/referral/revenue>
- **baselines** (object): <current value per KPI>
- **targets** (object): <target value + window per KPI>
- **vanity_excluded** (array): <vanity metrics explicitly excluded>
- **owner** (string): <owner_full_name>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
