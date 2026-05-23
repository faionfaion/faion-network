<!-- purpose: Three-tier audience spec Markdown skeleton. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Meta Audience Spec: [campaign]

## Core (cold)
- Interests: [list]
- Demo / behavior: [list]
- Size estimate: [500K-2M]

## Custom (warm)
- Sources: site_visitors_30d, video_75pct, lead-form_opens, ig_engagers

## Lookalike (scale)
- Source: [purchasers_180d / signups_90d]
- Source size: [≥1000]
- Pct: [1% | 2-3% | 5-10%]

## Exclusions
- current_customers
- subscribers
- recent_converters

## Advantage+ Audience?
[allowed | disabled] — gate: budget ≥ $100/day AND broad appeal
