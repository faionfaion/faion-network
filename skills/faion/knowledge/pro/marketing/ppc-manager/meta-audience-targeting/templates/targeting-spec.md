<!-- purpose: Granular targeting spec Markdown skeleton. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Meta Granular Targeting Spec

## Interest stacks (OR, 2-3 themes)
| # | Themes (OR) | Size estimate |
|---|-------------|---------------|
| 1 | SaaS / Developer Tools / DevOps | 1.2M |

## Behavioral filters (iOS-safe)
- tech_early_adopters
- engaged_shoppers

## Advantage+ Audience
enabled: [yes/no]
rationale: [broad / niche]

## Exclusion matrix
| Stage | Excludes |
|-------|----------|
| TOFU | current_customers, recent_converters |
| MOFU | purchasers_30d |
| BOFU | converters_7d |

## Dynamic creative
enabled: [yes/no — only on broad / Advantage+]
