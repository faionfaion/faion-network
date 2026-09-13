<!--
purpose: Canonical skeleton for the `dual-write-shadow-read-template` migration runbook — one section per rule in content/01-core-rules.xml.
consumes: Entity types with keys and version fields, the write and read paths, the feature-flag system, the parity and reconciliation dashboards, the named approvers.
produces: A committed runbook at .product/dual-write-shadow-read-template/<migration>.md plus its JSON form validated by scripts/validate-dual-write-shadow-read-template.py.
depends-on: templates/header.yaml, content/02-output-contract.xml, scripts/validate-dual-write-shadow-read-template.py.
token-budget-impact: ~1200 tokens to fill end-to-end.
-->
---
version: 0.1.0
migration_name: <migration_name>
old_store: <old_store>
new_store: <new_store>
read_from_new_approver: <read_from_new_approver>
write_to_old_off_approver: <write_to_old_off_approver>
---

# Migration

- migration_name: <migration_name>
- kind: postgres-major-upgrade | monolith-to-service-split | schema-rewrite | datastore-swap | other
- old_store: <old_store> (system of record until read_from_new_on)
- new_store: <new_store>

# Entity types and gates

Written before shadow mode starts (r-cutover-gate-numeric); parity exclusions per entity (r-shadow-read-parity-diff).

| Entity | Primary key | Version field | Parity-excluded fields | mismatch_ratio_max | window_hours | min_comparisons |
|---|---|---|---|---|---|---|
| <entity> | <key> | row_version \| updated_at \| lsn | <auto timestamps, surrogate ids> | <ratio under 1> | <hours> | <count> |

# Dual write

- upsert_kind: version-guarded-upsert; compare_and_set_on_version: true
- outside_old_store_transaction: true; failure_fails_user_request: false
- retry_queue: <durable queue>; failure_metric: dual_write_failures_total; alert_threshold: <n>

# Reconciliation

- job_name: <key-walk job>; cadence: every-5-minutes | hourly | every-6-hours | daily | weekly
- max_repairs_per_run: <n>; metric: reconciliation_repairs_total; declared_before_dual_write: true

# Backfill

- starts_after_dual_write: true; uses_same_upsert: true
- per_partition_counts_match: true; checksum_match: true; completed_before_shadow_parity: true; partitions: <n>

# Shadow read

- comparator: normalising; returns_old_store_result: true
- candidate_timeout_ms: <at or under old p99>; old_store_p99_ms: <measured>
- exceptions_swallowed_and_counted: true
- sampling_flag: <runtime flag>; sampling_percent_initial: <under 100>
- mismatch_metric: shadow_read_mismatch_ratio; mismatch_samples_retained: true

# Flags and rollback

| Stage | Flag name |
|---|---|
| dual_write_on | <flag> |
| shadow_read_on | <flag> |
| read_from_new_on | <flag> |
| write_to_old_off | <flag> |

- runtime_flippable: true
- reverse_order: write_to_old_off, read_from_new_on, shadow_read_on, dual_write_on
- retention_window_days: <n>; read_flipback_rehearsed_before_write_off: true

# Cutover

- gate_declared_before_shadow: true
- gate_evaluation_url: <dashboard over the declared window, required once reads are flipped>
- read_from_new_flipped: true | false
- read_from_new_approver: <read_from_new_approver>
- write_to_old_off_approver: <write_to_old_off_approver>

# Evidence

- <reconciliation dashboard>
- <backfill verification run>
- <gate evaluation at cutover>
- <flip-back rehearsal record>
