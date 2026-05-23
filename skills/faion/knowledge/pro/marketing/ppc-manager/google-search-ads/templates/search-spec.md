<!-- purpose: Search campaign spec Markdown skeleton. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Google Search Spec

## Ad groups (1 intent = 10-20 keywords)
| # | Name | Intent | KW count | RSA count |
|---|------|--------|----------|-----------|
| 1 | brand-search | branded | 12 | 3 |

## Match-type mix
- [x] broad (with smart bidding)
- [x] phrase
- [x] exact

## Extensions floor
- sitelinks ≥4
- callouts ≥4
- structured snippets (≥1 category)

## QS gate
- min QS: 7
- remediation: <7 days
