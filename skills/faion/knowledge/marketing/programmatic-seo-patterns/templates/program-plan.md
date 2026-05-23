<!-- purpose: Programmatic-SEO program plan Markdown skeleton. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Programmatic SEO Program

## Data source
- Provider: [internal_db / API / feed]
- Refresh cadence: [days]
- Quality %: ≥80

## Intent → Template map
| Intent | Template id |
|--------|--------------|
| comparison | tpl-vs |
| listing | tpl-list |
| location | tpl-loc |

## Thin-content threshold
- min_words: 300
- min_data_points: 2
- schema_required: true

## Indexability tiers
- tier_1 (full): indexed + sitemap
- tier_2 (partial): indexed
- tier_3 (sparse): noindex

## Internal-link graph
- sibling: 5 category-siblings per page
- parent: 1 category-parent per page

## Owner
[email]
