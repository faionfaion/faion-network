<!-- purpose: Spec for one dashboard -- purpose, metrics, visualizations, filters, alert rules, access. -->
<!-- consumes: decision the dashboard supports + metric definitions + data sources -->
<!-- produces: Markdown dashboard spec -->
<!-- depends-on: content/01-core-rules.xml (r2-max-7-widgets, r3-freshness-sla, r5-alert-threshold-per-widget) -->
<!-- token-budget-impact: ~300-450 tokens when loaded as context -->

# Dashboard Spec: <name>

## Purpose
[One sentence: what decision this dashboard supports]

## Audience
[Who will review this — founder, team, investor]

## Update Frequency
[Real-time / Daily / Weekly]

## Metrics
| Metric | Definition | Source | Update |
|--------|------------|--------|--------|
| <metric_1> | [How calculated] | [Tool] | [Frequency] |
| <metric_2> | [How calculated] | [Tool] | [Frequency] |

## Visualizations
1. **<chart_1>**: <type> showing [what metric over what dimension]
2. **<chart_2>**: <type> showing [what metric over what dimension]

## Filters
- Date range: [options: last 7d, 30d, 90d, custom]
- Segments: [options: by channel, plan, cohort]

## Alert Rules
- Alert when <metric> drops more than [X]% from 7-day rolling average
- Alert when <metric> misses weekly target by [X]%

## Access
- Location: <location>
- Permissions: <permissions>
