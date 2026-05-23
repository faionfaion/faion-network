<!-- purpose: Egress Cost Hidden Budget Guide skeleton (markdown) -->
<!-- consumes: rules in content/01-core-rules.xml -->
<!-- produces: produces=report -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~500 tokens when filled in -->

# Egress Cost Hidden Budget Guide — artefact skeleton

_Replace each placeholder with concrete content. Validate via `scripts/validate-egress-cost-hidden-budget-guide.py`._

## Summary

_One-paragraph summary of this instance._

## Fields

- **report_period** (string): _value here_
- **sources** (array (each {name, type, monthly_gb, cost_usd, attributed_feature})): _value here_
- **budgets** (array (each {region, monthly_cap_usd, alert_at_80pct, freeze_at_100pct})): _value here_
- **worst_case_model** (object (peak_multiplier, projected_gb, projected_cost)): _value here_
- **nat_gw_alternatives_review** (array (each {nat_gw_id, alternative, est_savings_usd)): _value here_
- **review_date** (string): _value here_
