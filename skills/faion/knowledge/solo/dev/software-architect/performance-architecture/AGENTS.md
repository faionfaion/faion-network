# Performance Architecture

## Summary

Design systems to meet explicit SLO targets (p50/p95/p99, throughput, error rate, availability) by addressing all five layers: client, CDN/edge, load balancer, application, and data. Run a measurement-first loop: profiler agent reads APM/traces → analyzer identifies bottleneck layer → designer proposes change with predicted p95 improvement → validator runs a load test that proves or disproves the prediction. Never optimize without a captured baseline.

## Why

Performance problems are layer-specific: a missing index looks identical to a connection-pool exhaustion in aggregate metrics. Without layer attribution, agents rewrite cold code paths because they look messy, not because they are hot. SLOs from user-impact analysis (not industry tables) give falsifiable targets; p99 is where users churn, not mean latency.

## When To Use

- Defining SLOs and error budgets at design time, before performance becomes a customer complaint.
- Pre-launch capacity planning for a feature expected to receive measurable traffic.
- Performance regression triage: structured layer-by-layer narrowing.
- Cost optimization driven by tail latency or compute waste.
- Pre-IPO/audit scenarios requiring documented performance commitments.

## When NOT To Use

- Pure prototypes — premature optimization slows delivery without buying reliability.
- Pages/APIs with no production traffic yet — measure first.
- Hot-fixing a single slow query — use profiling tools directly, not a full architecture loop.

## Content

| File | What's inside |
|------|---------------|
| `content/01-slos-and-layers.xml` | SLO tier table, five performance layers with targets, error budget calculation, capacity planning formulas. |
| `content/02-scalability.xml` | Horizontal vs vertical scaling, data partitioning, K8s HPA, connection pooling sizing formula, async processing patterns. |
| `content/03-database-and-cdn.xml` | Query optimization rules, indexing strategy by type, message queue selection matrix, CDN/edge function use cases, asset optimization techniques. |
| `content/04-antipatterns.xml` | N+1 queries, sync external calls, over-fetching, missing connection pooling, premature optimization — each with detection and fix. |

## Templates

| File | Purpose |
|------|---------|
| `templates/k6-load-test.js` | k6 script with steady + spike scenarios, p95/p99 thresholds, and randomized key distribution. |
