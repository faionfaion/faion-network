<!-- purpose: PMax spec Markdown skeleton with asset groups + signals + negatives. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Performance Max Spec

## Conversion floor
monthly_conversions: [≥30]

## Asset groups (≥3)
| # | Name | Theme | Audience signal(s) | Brand-safe? |
|---|------|-------|--------------------|-------------|
| 1 | ag-saas-tools | saas-tools | customer_match + remarketing | yes |

## Brand negatives
- [brand]
- [brand-variant]

## Value priority
| Event | Value |
|-------|-------|
| Purchase | 1.0 |
| Lead | 0.3 |

## Reporting
Flag 'Other' bucket spend > 30% as opacity alert.
