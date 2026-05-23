<!-- __faion_header_v1__ -->
<!-- purpose: Performance spec skeleton with SLO targets + headroom + cache topology + load-test gate. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: spec; depends-on: content/01-core-rules.xml#r1-numeric-slos-only -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Performance spec skeleton with SLO targets + headroom + cache topology + load-test gate.","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#r1-numeric-slos-only","token_budget_impact":"~150 tokens when loaded"}} -->
# Performance Spec

## SLO Targets
- p50: <ms>
- p95: <ms>
- p99: <ms>
- Availability: <%>
- Error budget: <%> per 30d

## Baseline
- Current p95: <ms> at <RPS>
- Headroom: <%>

## Cache Topology
- CDN: <what is cached, TTL>
- Application cache (Redis): <keys, TTL, eviction>
- DB-level cache: <materialised views, query cache>

## Database Optimisation
- Indexes: <columns>
- Partitioning: <table, key>
- Read replicas: <yes/no, lag tolerance>

## Load-test Gate
- Tool: k6 / vegeta / locust
- Scenarios: smoke, baseline, stress, soak
- Thresholds matching SLO above.
