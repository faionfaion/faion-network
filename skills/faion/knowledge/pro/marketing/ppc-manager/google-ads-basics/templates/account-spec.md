<!-- purpose: Google Ads account setup spec Markdown skeleton. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Google Ads Account Spec

## Campaign types
[ ] search
[ ] shopping
[ ] performance_max (only if ≥30 conv/mo)
[ ] display
[ ] video

## Ad groups (1 theme = 10-20 keywords)
| # | Name | Theme | Keyword count |
|---|------|-------|---------------|
| 1 | brand-search | brand | 12 |

## Conversion tracking
- Events: Purchase, SignUp, ...
- GA4 imported: yes

## Extensions (min 3)
- sitelinks (≥4)
- callouts (≥4)
- structured_snippets

## Billing + roles
- Payment method verified
- Roles: admin / manager / read-only
