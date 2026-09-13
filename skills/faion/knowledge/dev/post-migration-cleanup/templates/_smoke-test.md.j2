<!-- purpose: filled-in canonical cleanup checklist for calibration (orders_v1 to orders_v2) -->
<!-- consumes: nothing — this is a hand-filled fixture -->
<!-- produces: checklist instance that MUST validate via scripts/validate-post-migration-cleanup.py -->
<!-- depends-on: templates/output.md, content/02-output-contract.xml -->
<!-- token-budget-impact: ~1000 tokens -->

# Post Migration Cleanup — Smoke Test Fixture

The valid example from `content/02-output-contract.xml`; `scripts/validate-post-migration-cleanup.py --self-test` runs it.

```json
{
  "migration": {
    "name": "orders-service: orders_v1 schema to orders_v2",
    "legacy_component": "orders_v1 (Postgres schema + /v1/orders endpoint)",
    "new_component": "orders_v2 schema + /v2/orders",
    "cutover_date": "2026-04-01",
    "parity_window": {
      "start": "2026-04-03",
      "end": "2026-04-10",
      "days": 8,
      "includes_full_weekly_cycle": true
    },
    "delivery_cycle_days": 14,
    "cleanup_deadline": "2026-04-24"
  },
  "dual_write": {
    "reconciliation_report_url": "https://reports.acme.example/orders-reconciliation/2026-04-03_2026-04-10",
    "consecutive_days_zero_mismatch": 8,
    "mismatches": 0,
    "legacy_write_removed_by": "code_deletion",
    "deletion_pr_url": "https://github.com/acme/orders-service/pull/8812"
  },
  "legacy_read_path": {
    "counter_name": "orders_v1_reads_total",
    "zero_for_days": 9,
    "includes_batch_window": true,
    "evidence_url": "https://grafana.acme.example/d/orders/v1-reads?from=2026-04-03&to=2026-04-12",
    "deletion_pr_url": "https://github.com/acme/orders-service/pull/8820"
  },
  "flags": [
    {
      "key": "orders.dual_write",
      "removal_pr_url": "https://github.com/acme/orders-service/pull/8812",
      "key_deleted_from_flag_service": true,
      "branches_collapsed": true
    },
    {
      "key": "orders.read_from_v2",
      "removal_pr_url": "https://github.com/acme/orders-service/pull/8820",
      "key_deleted_from_flag_service": true,
      "branches_collapsed": true
    },
    {
      "key": "orders.v2_shadow_compare",
      "removal_pr_url": "https://github.com/acme/orders-service/pull/8821",
      "key_deleted_from_flag_service": true,
      "branches_collapsed": true
    }
  ],
  "shims": [
    {
      "name": "/v1/orders -> /v2/orders proxy",
      "kind": "endpoint_proxy",
      "consumers": [
        "mobile-app <= 4.12 (2.1% of sessions)"
      ],
      "disposition": "retained",
      "removal_date": "2026-07-01",
      "consumer_counter": "orders_v1_proxy_requests_total{client=\"mobile\"}"
    },
    {
      "name": "orders.customer_ref column alias",
      "kind": "column_alias",
      "consumers": [],
      "disposition": "deleted_in_this_cleanup",
      "deletion_pr_url": "https://github.com/acme/orders-service/pull/8824"
    }
  ],
  "schema_drop": {
    "objects": [
      "schema orders_v1",
      "index orders_v1_customer_idx"
    ],
    "separate_change_from_code_deletion": true,
    "snapshot": {
      "url": "s3://acme-backups/orders_v1-2026-04-12.dump",
      "retention_until": "2026-10-01"
    },
    "reference_scan": {
      "command": "gh search code 'orders_v1' --owner acme; grep -c orders_v1 /var/log/postgresql/slow.log",
      "repositories_scanned": 41,
      "query_log_searched": true,
      "hits": 0
    },
    "drop_change_url": "https://github.com/acme/orders-service/pull/8830"
  },
  "docs": {
    "search_command": "grep -ril 'orders_v1\\|/v1/orders' docs/ runbooks/ adr/",
    "hits_before": 14,
    "hits_after_outside_archive": 0,
    "archive_location": "docs/archive/orders-v1/"
  },
  "observability": [
    {
      "name": "OrdersV1WriteErrors",
      "kind": "alert",
      "disposition": "deleted",
      "target_or_change_url": "https://github.com/acme/monitoring/pull/2210"
    },
    {
      "name": "Orders overview",
      "kind": "dashboard",
      "disposition": "retargeted",
      "target_or_change_url": "orders_v2_* metrics, https://github.com/acme/monitoring/pull/2211"
    },
    {
      "name": "orders-latency-slo",
      "kind": "slo",
      "disposition": "retargeted",
      "target_or_change_url": "http_request_duration_seconds{route=\"/v2/orders\"}"
    }
  ],
  "infrastructure": [
    {
      "resource": "orders-v1-reader replica (RDS)",
      "kind": "database",
      "decommission_date": "2026-04-15",
      "monthly_cost_removed": 420,
      "still_running": false
    },
    {
      "resource": "orders-v1-sync SQS queue",
      "kind": "queue",
      "decommission_date": "2026-04-14",
      "monthly_cost_removed": 12,
      "still_running": false
    },
    {
      "resource": "iam role orders-v1-writer",
      "kind": "iam_role",
      "decommission_date": "2026-04-14",
      "monthly_cost_removed": 0,
      "still_running": false
    },
    {
      "resource": "orders-v1.internal DNS record",
      "kind": "dns_record",
      "monthly_cost_removed": 0,
      "still_running": true,
      "reason": "mobile-app <= 4.12 resolves it for the proxy shim until the shim's removal date",
      "end_date": "2026-07-01"
    }
  ],
  "deferred_items": [
    {
      "item": "delete /v1/orders proxy shim and orders-v1.internal DNS record",
      "ticket_url": "https://jira.acme.example/browse/ORD-1188",
      "owner": "dana@acme.example"
    }
  ],
  "review": {
    "status": "ready_for_review",
    "reviewer": "kim@acme.example",
    "drop_or_decommission_executed_by_agent": false
  }
}
```
