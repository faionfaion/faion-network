<!-- purpose: Monthly optimization plan Markdown skeleton. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Google Ads Optimization Plan: [month]

## Bidding strategy
[manual_cpc | maximize_conversions | target_cpa $X | target_roas X | maximize_conversion_value]
Rationale: [conv volume bucket]

## Weekly actions
| Lever | Trigger | Owner |
|-------|---------|-------|
| negative_sweep | search_term_cost > $5 | ops |
| qs_remediation | qs < 5 | ops + creative |

## Monthly actions
| Lever | Trigger | Owner |
|-------|---------|-------|
| budget_rebalance_quartile | ROAS quartile delta > 20% | ops |
| bidding_strategy_review | conv volume bucket changed | manager |

## Change log
(append-only, timestamp + change + rationale + owner)
