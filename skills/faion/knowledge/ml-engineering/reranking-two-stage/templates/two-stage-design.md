# purpose: two-stage retrieval design record skeleton
# consumes: bench evidence + latency budget + recall target
# produces: markdown record matching 02-output-contract schema
# depends-on: content/01-core-rules.xml r1-r5
# token-budget-impact: zero at runtime; doc only

# Two-Stage Retrieval Design

Owner: <name>
Date: YYYY-MM-DD

## Stage 1 — Recall
- Type: ann (bi-encoder)
- Pool size: 50
- Recall@pool target: 0.85

## Stage 2 — Precision
- Type: cross-encoder
- Top-K: 5
- Precision@5 target: 0.75

## Latency Budget
- Total: <ms>
- Stage 1: ~50ms
- Stage 2: 100-300ms

## Fallback
- On stage-2 failure → stage-1 top-K with degraded flag.

## Bench Evidence
- recall@50: <x>
- precision@5: <y>
- p95 latency: <ms>
