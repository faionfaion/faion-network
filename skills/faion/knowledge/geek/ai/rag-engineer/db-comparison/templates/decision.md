<!-- purpose: vector-DB decision record skeleton -->
<!-- consumes: year-1 scale + query pattern + hosting policy + score matrix -->
<!-- produces: signed decision.md plus paired decision.json -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: small -->

# Vector DB Decision — `<project-name>`

- **decision_version:** 1.0.0
- **decision_owner:** `<role:person>`
- **last_reviewed:** `<YYYY-MM-DD>`
- **year_one_vectors:** `<int>`

## Chosen

`<chroma | qdrant | weaviate | pgvector | pinecone | milvus>`

## Score matrix

| candidate | scale_fit | hosting_fit | hybrid_search | payload_filter_perf | multi_tenant | existing_postgres | team_familiarity | weighted_total |
|-----------|----------:|------------:|--------------:|--------------------:|-------------:|------------------:|-----------------:|---------------:|
| `<db-1>`  | 0..3 | 0..3 | 0..3 | 0..3 | 0..3 | 0..3 | 0..3 | `<float>` |
| `<db-2>`  | 0..3 | 0..3 | 0..3 | 0..3 | 0..3 | 0..3 | 0..3 | `<float>` |

## Fallbacks

1. `<db>` — trigger: `<condition>`
2. `<db>` — trigger: `<condition>`

## Migration plan

`<phases + data export path + cut-over date>`

## Prior decisions

- `<link or commit hash>`
