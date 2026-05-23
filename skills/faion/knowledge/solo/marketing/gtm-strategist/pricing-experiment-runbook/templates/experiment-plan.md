<!--
purpose: one-page Pricing Experiment Plan skeleton
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml plan section
depends-on: content/01-core-rules.xml
token-budget-impact: ~400 tokens when loaded as context
-->
# Pricing Experiment Plan — REPLACE-EXPERIMENT-ID

| Field | Value |
|-------|-------|
| experiment_id | REPLACE-slug-with-date |
| start_date | YYYY-MM-DD |
| end_date | YYYY-MM-DD |
| duration_days | 7-90 |
| variant_old.stripe_price_id | price_REPLACE |
| variant_new.stripe_price_id | price_REPLACE |
| audience | new_signups_only \| new_and_existing_with_grandfather \| specific_segment |
| exposure_rule | one paragraph explaining how visitors map to variants |
| success_metric_primary | e.g. trial_to_paid_conversion_pct |
| success_metric_threshold | numeric |
| significance_target | p<0.05 \| p<0.10 \| bayesian_95 |
| guardrail_metrics | refund_rate, dispute_rate, support_ticket_rate |
| currencies_in_test | usd \| eur \| ... |
| tax_behavior | inclusive \| exclusive |

## Grandfathering

- audience: REPLACE
- mechanism: 100% off coupon on new Price OR separate old Price object
- stripe_coupon_id: REPLACE
- window_months: REPLACE
- renewal_after_window: REPLACE

## Termination rules

- refund_rate > 2x baseline OR support_ticket_rate > 3x baseline → terminate, revert
- dispute_rate > 0.5% → terminate, revert
- significance not reached at 80% of plan → extend by 30 days max, then force go/no-go
- significance reached with negative MRR effect → terminate, revert, document
