<!-- purpose: Display campaign spec Markdown skeleton. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Google Display Spec

## Audiences (≥3 tiers)
- in_market: [topic]
- affinity: [topic]
- remarketing: [list, size]
- custom_intent: [URL/keyword set] (optional)

## Placement exclusions
- [x] mobile_apps_excluded
- [x] low_quality_list_applied

## Creative set (≥3 formats)
- responsive_display
- native
- image_300x250 / 728x90 / 320x50

## Frequency cap
per_day: 5
per_week: 15

## KPIs
- CPA ceiling: $X (upper-funnel attribution)
- CPM floor: $X (cost-of-reach benchmark)
