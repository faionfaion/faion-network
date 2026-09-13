<!-- purpose: latency budget allocation skeleton — same sections and field names as content/02-output-contract.xml -->
<!-- consumes: the user-facing SLO, critical-path traces, caller-side histograms per hop, timeout and retry config, perf environment and load tool (AGENTS.md Prerequisites) -->
<!-- produces: Latency Budget Allocation spec validating against scripts/validate-latency-budget-allocation.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~700 tokens when filled -->

# Latency Budget Allocation — <system_name>

## SLO (the total budget)

- `metric`: <metric_name> — `percentile` + `threshold_ms`: <metric_target> — `measurement_point`: client | edge | load_balancer | server — `window_days`:
- Budget measured at the same point as the SLO? If not, `difference_hop_id` (DNS / TLS / CDN as its own hop):

## Composition

- `model`: sequential_sum_plus_headroom | critical_path_with_parallel_stages — `sum_of_hop_budgets_ms` + `reserve_ms` <= threshold
- Percentiles added as proof: never — `verified_against`: end-to-end histogram, measured percentile (ms), window days, request count (>= 1000)

## Hops (critical path, caller-side histograms)

| id | Service | Owner team | Histogram + labels (caller side) | Budget ms | Measured p95 ms | Reconciliation (within_budget / underwater: ticket + owner / slack_over_2x: justification) | Bucket boundary within 10% of budget (else task) | Timeout ms x attempts + backoff = worst case ms (<= budget) | Deadline propagated | Fan-out: N, stage percentile, child percentile (stricter), mitigation |
|----|---------|------------|----------------------------------|-----------|-----------------|-----------------------------------------------------------------------------------------------|-------------------------------------------------|-------------------------------------------------------------|---------------------|--------------------------------------------------------------------------|

- `reserve_ms` (unallocated headroom, its own line):

## CI gate (percentiles only)

- `command` (exact, re-runnable):
- `environment`:
- `min_requests_per_run` (>= 200):
- Thresholds: end-to-end and per hop, percentile + ms
- `on_failure`: block_merge | warn (named owner) — blocking enabled by agent: no

## Review

- `status`: draft | ready_for_review | approved (reviewer, approved on)

## Validation

Run `python scripts/validate-latency-budget-allocation.py --file <allocation.json>`. Exit 0 = valid, exit 1 = violations on stderr.
