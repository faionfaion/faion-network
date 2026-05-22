<!--
purpose: Markdown skeleton for a latency waterfall report
consumes: per-segment percentiles, budget table
produces: human-readable companion to the JSON report
depends-on: content/01-core-rules.xml
token-budget-impact: ~400 tokens when rendered
-->
# Latency Waterfall — {{feature}}

| Field | Value |
|---|---|
| Window | {{start}} → {{end}} |
| Samples | {{n_samples}} |
| SLA | p95 ≤ {{sla_value_ms}} ms |
| Cache hit rate | {{cache_hit_rate}} |
| Owner | {{owner}} |

## Segments

| Segment | p50 ms | p95 ms | Budget ms | Status |
|---|---|---|---|---|
| ttfb | {{ttfb_p50}} | {{ttfb_p95}} | {{ttfb_budget}} | {{ttfb_status}} |
| prefill_cold | {{pc_p50}} | {{pc_p95}} | {{pc_budget}} | {{pc_status}} |
| prefill_hit | {{ph_p50}} | {{ph_p95}} | {{ph_budget}} | {{ph_status}} |
| decode | {{dec_p50}} | {{dec_p95}} | {{dec_budget}} | {{dec_status}} |
| tool_* | {{tool_p50}} | {{tool_p95}} | {{tool_budget}} | {{tool_status}} |
| post_process | {{pp_p50}} | {{pp_p95}} | {{pp_budget}} | {{pp_status}} |

## Recommendation

Biggest over budget: `{{biggest_over_budget_segment}}`

{{recommendation}}
