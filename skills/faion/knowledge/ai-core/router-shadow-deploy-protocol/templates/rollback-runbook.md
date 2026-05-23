<!--
purpose: step-by-step rollback procedure for router cut-over regression
consumes: rollback flag + git revision of last-good gateway config
produces: report (rollback execution log)
depends-on: feature-flag infra + gateway config in git
token-budget-impact: 0 at runtime
-->

# Rollback Runbook: router cut-over

## Trigger conditions
- Any user-visible metric breaches acceptance-contract floor for >5 minutes post-cut-over
- Cost dashboard shows >2x baseline for >15 minutes
- Schema parity drops below 1.00 in live traffic

## Steps (target: <15 minutes)

1. **Acknowledge** in PagerDuty.
2. **Verify breach** with `kubectl logs gateway` + Grafana panel ID 4.
3. **Flip flag**: `faion-cli flag set router_v2_enabled=false --env prod` (15s propagation).
4. **Confirm traffic** routed back to `router-v1` via gateway metrics.
5. **Capture state**: snapshot `shadow-log` table for forensic review.
6. **Stand-down**: post in #ops "router rollback complete at <time>".
7. **Post-mortem ticket** filed within 24h.

## Post-rollback
- Do NOT re-promote without a new shadow window
- Reuse the same `shadow-report.yaml` lineage; add a v2 entry with the failure root cause
