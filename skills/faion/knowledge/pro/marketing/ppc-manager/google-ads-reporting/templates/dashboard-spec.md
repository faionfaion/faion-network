<!-- purpose: Dashboard spec Markdown skeleton with 3 views + alerts. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Google Ads Dashboard Spec

## Column preset
Impr, Clicks, CTR, Avg CPC, Cost, Conv, Conv rate, CPA, Conv value, ROAS, IS, QS

## Views
- operator_weekly (every column, every breakdown)
- executive_monthly (KPI summary + top-5 actions)
- stakeholder_summary (1-page: KPI + RAG status)

## Alerts
| Metric | Op | Threshold |
|--------|----|-----------|
| CPA | > | target +20% |
| IS | < | 70% |
| conv_rate | < | target -15% |
| daily_spend | > | forecast +25% |

## Segments (mandatory)
- device / network / location / time / audience

## Action queue (top-5)
| # | Lever | Expected impact | Owner |
|---|-------|------------------|-------|
