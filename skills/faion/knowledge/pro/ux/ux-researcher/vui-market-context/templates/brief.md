<!-- purpose: VUI market brief skeleton with scoped stats + 5-platform comparison -->
<!-- consumes: vui_market_brief.json (data[] + platforms[]) -->
<!-- produces: publishable markdown brief for stakeholder/investor deck -->
<!-- depends-on: content/02-output-contract.xml schema -->
<!-- token-budget-impact: ~800 tokens rendered -->

# VUI Market Context — {{ product_name }} Q{{ quarter }} {{ year }}

_Refreshed: {{ refreshed_at }}. Model: {{ model }}._

## Adoption stats (sourced)

| Metric | Value | Year | Geo | Denominator | Source |
|--------|-------|------|-----|-------------|--------|
{{# for row in data }}
| {{ row.metric }} | {{ row.value }} | {{ row.year }} | {{ row.geo }} | {{ row.denominator }} | {{ row.source_url }} |
{{/ for }}

## Platform comparison (per target geo)

| Platform | Reach in {{ geo1 }} | Reach in {{ geo2 }} | SDK health |
|----------|---------------------|---------------------|------------|
{{# for p in platforms }}
| {{ p.name }} | {{ p.reach_by_geo[geo1] }} | {{ p.reach_by_geo[geo2] }} | {{ p.sdk_health }} |
{{/ for }}

## Recommendation

{{ recommendation_paragraph }}

_Re-validate when refreshed_at > 90 days from today._
