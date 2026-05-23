<!-- purpose: Retargeting plan Markdown skeleton with the 5-tier ladder. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Retargeting Plan: [campaign]

## Spend share
[20-30]% of total ad spend

## Segments (intent ladder)
| # | Name | Depth | Freq cap / wk | Message stage |
|---|------|-------|---------------|---------------|
| 1 | visitors_30d | 1 | 3 | reminder |
| 2 | blog_readers_30d | 2 | 4 | educate |
| 3 | product_viewers_30d | 3 | 5 | benefits |
| 4 | pricing_viewers_14d | 4 | 6 | social_proof |
| 5 | cart_abandoners_7d | 5 | 7 | urgency |

## Exclusions
- purchasers_90d
- subscribers

## Sequencing
Visitors → product → pricing → cart: rotate message after 5 impressions or 7 days, whichever first.
