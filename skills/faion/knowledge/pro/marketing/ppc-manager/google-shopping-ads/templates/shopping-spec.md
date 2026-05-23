<!-- purpose: Shopping campaign spec Markdown skeleton. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Google Shopping Spec

## Feed health
- Health %: ≥80 (titles / GTIN / images / attributes)

## Priority tiers
| Tier | ROAS target |
|------|--------------|
| high | ≥4 |
| medium | ≥2.5 |
| clearance | ≥1.5 |

## Product groups
| # | Name | Partition by |
|---|------|--------------|
| 1 | high-margin | margin > 30% |
| 2 | clearance | tag = clearance |

## Negative keywords (sample)
free, used, torrent, jobs
