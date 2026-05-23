<!-- purpose: Headroom Cost Model skeleton (markdown) -->
<!-- consumes: rules in content/01-core-rules.xml -->
<!-- produces: produces=report -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~500 tokens when filled in -->

# Headroom Cost Model — artefact skeleton

_Replace each placeholder with concrete content. Validate via `scripts/validate-headroom-cost-model.py`._

## Summary

_One-paragraph summary of this instance._

## Fields

- **report_period** (string): _value here_
- **resources** (array (each {name, type, provisioned, utilisation_p95_30d, headroom_pct, cost_unit_usd, monthly_cost_usd})): _value here_
- **alerts** (array (each {resource, threshold, action})): _value here_
- **quarterly_projection** (object (next_quarter_demand_delta_pct, next_quarter_cost_delta_usd)): _value here_
- **anomalies** (array (each {resource, deviation_pct, investigation_ticket})): _value here_
- **review_date** (string): _value here_
- **signoff** (object (engineering_leader, finance, date)): _value here_
