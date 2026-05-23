# purpose: vector-DB decision record skeleton
# consumes: workload characteristics + bench evidence
# produces: markdown record matching 02-output-contract schema
# depends-on: content/01-core-rules.xml r1-r5
# token-budget-impact: zero at runtime

# Vector DB Decision Record

Owner: <name>
Date: YYYY-MM-DD

## Choice
- DB: qdrant
- Deployment: self-host

## Index
- Type: hnsw
- dim: 3072
- distance: cosine

## Bench Evidence
- recall@10: 0.96
- p95 latency: 18 ms
- qps target: 240

## Filter Pushdown Verified
- Yes (server-side; payload index built on `source`, `page`).
