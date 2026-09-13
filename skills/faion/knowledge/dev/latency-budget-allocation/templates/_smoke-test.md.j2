<!-- purpose: filled-in canonical allocation for calibration (checkout p95 800 ms) -->
<!-- consumes: nothing — this is a hand-filled fixture -->
<!-- produces: allocation instance that MUST validate via scripts/validate-latency-budget-allocation.py -->
<!-- depends-on: templates/output.md, content/02-output-contract.xml -->
<!-- token-budget-impact: ~1000 tokens -->

# Latency Budget Allocation — Smoke Test Fixture

The valid example from `content/02-output-contract.xml`; `scripts/validate-latency-budget-allocation.py --self-test` runs it.

```json
{
  "slo": {
    "name": "checkout p95 at the edge",
    "metric": "checkout_request_duration_seconds",
    "percentile": "p95",
    "threshold_ms": 800,
    "measurement_point": "edge",
    "window_days": 28,
    "budget_measurement_point_matches": true
  },
  "composition": {
    "model": "critical_path_with_parallel_stages",
    "sum_of_hop_budgets_ms": 700,
    "percentiles_added_as_proof": false,
    "verified_against": {
      "end_to_end_histogram": "checkout_request_duration_seconds{point=\"edge\"}",
      "measured_percentile_ms": 742,
      "window_days": 28,
      "request_count": 4180000
    }
  },
  "hops": [
    {
      "id": "hop-edge-to-gateway",
      "service": "cdn + api-gateway",
      "owner_team": "platform",
      "metric": {
        "histogram": "gateway_upstream_duration_seconds",
        "labels": {
          "route": "/checkout"
        }
      },
      "measured_side": "caller",
      "budget_ms": 80,
      "measured_p95_ms": 61,
      "reconciliation": "within_budget",
      "bucket_boundary_within_10pct_of_budget": true,
      "timeout_and_retry": {
        "timeout_ms": 80,
        "max_attempts": 1,
        "backoff_ms": 0,
        "worst_case_ms": 80,
        "worst_case_within_budget": true
      },
      "deadline_propagated": true
    },
    {
      "id": "hop-checkout-svc",
      "service": "checkout-service",
      "owner_team": "checkout",
      "metric": {
        "histogram": "http_client_duration_seconds",
        "labels": {
          "caller": "api-gateway",
          "callee": "checkout-service"
        }
      },
      "measured_side": "caller",
      "budget_ms": 120,
      "measured_p95_ms": 98,
      "reconciliation": "within_budget",
      "bucket_boundary_within_10pct_of_budget": true,
      "timeout_and_retry": {
        "timeout_ms": 100,
        "max_attempts": 1,
        "backoff_ms": 0,
        "worst_case_ms": 100,
        "worst_case_within_budget": true
      },
      "deadline_propagated": true
    },
    {
      "id": "hop-inventory-fanout",
      "service": "inventory-shards",
      "owner_team": "inventory",
      "metric": {
        "histogram": "grpc_client_duration_seconds",
        "labels": {
          "caller": "checkout-service",
          "callee": "inventory-shard"
        }
      },
      "measured_side": "caller",
      "budget_ms": 250,
      "measured_p95_ms": 212,
      "reconciliation": "within_budget",
      "bucket_boundary_within_10pct_of_budget": true,
      "timeout_and_retry": {
        "timeout_ms": 110,
        "max_attempts": 2,
        "backoff_ms": 10,
        "worst_case_ms": 230,
        "worst_case_within_budget": true
      },
      "deadline_propagated": true,
      "fan_out": {
        "n": 12,
        "stage_percentile": "p95",
        "child_percentile": "p999",
        "mitigation": "hedged_requests"
      }
    },
    {
      "id": "hop-pricing",
      "service": "pricing-service",
      "owner_team": "pricing",
      "metric": {
        "histogram": "http_client_duration_seconds",
        "labels": {
          "caller": "checkout-service",
          "callee": "pricing-service"
        }
      },
      "measured_side": "caller",
      "budget_ms": 150,
      "measured_p95_ms": 176,
      "reconciliation": "underwater",
      "improvement_ticket": "https://jira.acme.example/browse/PRICE-812",
      "improvement_owner": "pricing",
      "bucket_boundary_within_10pct_of_budget": false,
      "bucket_change_task": "https://jira.acme.example/browse/OBS-301 add 0.15s bucket",
      "timeout_and_retry": {
        "timeout_ms": 140,
        "max_attempts": 1,
        "backoff_ms": 0,
        "worst_case_ms": 140,
        "worst_case_within_budget": true
      },
      "deadline_propagated": true
    },
    {
      "id": "hop-payment-auth",
      "service": "payment-gateway (external)",
      "owner_team": "payments",
      "metric": {
        "histogram": "http_client_duration_seconds",
        "labels": {
          "caller": "checkout-service",
          "callee": "psp"
        }
      },
      "measured_side": "caller",
      "budget_ms": 100,
      "measured_p95_ms": 38,
      "reconciliation": "slack_over_2x",
      "slack_justification": "PSP contract allows 250 ms p95 on peak days; 100 ms is the floor we can defend without a second provider",
      "bucket_boundary_within_10pct_of_budget": true,
      "timeout_and_retry": {
        "timeout_ms": 90,
        "max_attempts": 1,
        "backoff_ms": 0,
        "worst_case_ms": 90,
        "worst_case_within_budget": true
      },
      "deadline_propagated": true
    }
  ],
  "reserve_ms": 100,
  "ci_gate": {
    "command": "k6 run --vus 40 --duration 3m perf/checkout.js --out json=perf/out.json && perf/check-thresholds.py perf/out.json budget.json",
    "environment": "perf-staging (same instance sizes as production, seeded dataset perf-2026-06)",
    "min_requests_per_run": 5000,
    "statistic": "percentile",
    "thresholds": [
      {
        "hop_id": "end-to-end",
        "percentile": "p95",
        "threshold_ms": 800
      },
      {
        "hop_id": "hop-checkout-svc",
        "percentile": "p95",
        "threshold_ms": 120
      },
      {
        "hop_id": "hop-inventory-fanout",
        "percentile": "p95",
        "threshold_ms": 250
      },
      {
        "hop_id": "hop-pricing",
        "percentile": "p95",
        "threshold_ms": 150
      }
    ],
    "on_failure": "block_merge",
    "blocking_enabled_by_agent": false
  },
  "review": {
    "status": "ready_for_review",
    "reviewer": "checkout-lead@acme.example"
  }
}
```
