<!-- purpose: post-migration cleanup checklist skeleton — same sections and field names as content/02-output-contract.xml -->
<!-- consumes: cutover deploy record, reconciliation report, legacy read counter, flag service export, shim list, cloud inventory, docs search, alert rules (AGENTS.md Prerequisites) -->
<!-- produces: Post Migration Cleanup checklist validating against scripts/validate-post-migration-cleanup.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~800 tokens when filled -->

# Post-Migration Cleanup — <project_name> (<system_name>)

## Migration

- Legacy component: — new component: — `cutover_date` (first day at 100% on the new path):
- `parity_window`: start, end, days (>= 7, includes a full weekly cycle) — `delivery_cycle_days` (<= 30) — `cleanup_deadline` (<= one cycle after the window closes):

## Dual write (delete from code, only after parity)

- `reconciliation_report_url`: — consecutive days at zero mismatches (>= 7): — mismatches: 0
- Legacy write removed by: code deletion — `deletion_pr_url`:

## Legacy read path (delete at zero traffic)

- `counter_name`: — zero for days (>= 7, includes the batch / month-end window): — `evidence_url`: — `deletion_pr_url`:

## Migration flags (key deleted from the flag service, branches collapsed)

| Flag key | Removal PR | Key deleted from flag service | Branches collapsed |
|----------|------------|-------------------------------|--------------------|

## Compatibility shims

| Shim | Kind (adapter / column_alias / endpoint_proxy / event_schema_translator / redirect) | Consumers | Disposition (deleted_in_this_cleanup: PR / retained: removal date or consumer counter) |
|------|--------------------------------------------------------------------------------------|-----------|----------------------------------------------------------------------------------------|

## Schema drop (separate change from the code deletion)

- Objects: — `snapshot.url` + `retention_until` (on or after the next review):
- Reference scan: command, repositories scanned, query log searched, hits: 0 — `drop_change_url`:

## Docs and runbooks

- `search_command`: — hits before: — hits after outside `archive_location`: 0

## Alerts, dashboards, SLOs, synthetic checks

| Name | Kind | Disposition (retargeted: new target / deleted: change URL) |
|------|------|------------------------------------------------------------|

## Infrastructure

| Resource | Kind | Decommission date | Monthly cost removed | Still running? (reason, end date) |
|----------|------|-------------------|----------------------|-----------------------------------|

## Deferred items (anything not deleted by the deadline)

| Item | Ticket | Owner |
|------|--------|-------|

## Review

- `status`: draft | ready_for_review | approved — reviewer <reviewer_name> read the snapshot URL and the scan result on: — drop or decommission executed by agent: no

## Validation

Run `python scripts/validate-post-migration-cleanup.py --file <cleanup.json>`. Exit 0 = valid, exit 1 = violations on stderr.
