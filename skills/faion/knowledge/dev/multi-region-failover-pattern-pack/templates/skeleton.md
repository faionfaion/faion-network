<!--
purpose: Canonical skeleton for the `multi-region-failover-pattern-pack` — pattern choice, DNS / database / object-store mechanics, dependency list, drill checklist with last result, and failback.
consumes: Agreed RPO/RTO per tier, 30-day replication metrics, object-store replication config, the dependency inventory, and the last live drill.
produces: A committed pack at .product/multi-region-failover-pattern-pack/<workload>.md, mirrored as JSON for scripts/validate-multi-region-failover-pattern-pack.py.
depends-on: templates/header.yaml, content/02-output-contract.xml, scripts/validate-multi-region-failover-pattern-pack.py.
token-budget-impact: ~1200 tokens to fill end-to-end.
-->
---
version: 0.1.0
workload: <workload_name>
owner: <owner>
rpo_minutes: <rpo_minutes>
rto_minutes: <rto_minutes>
---

# Workload

- name: <workload_name>
- tier: <tier>
- business_owner: <business_owner>
- owner: <owner>
- primary_region: <primary_region>
- secondary_region: <secondary_region>

# Inputs

- rpo_minutes: <rpo_minutes>
- rto_minutes: <rto_minutes>

# Pattern

- chosen: <pattern>
- achievable_rpo_minutes: <achievable_rpo_minutes>
- achievable_rto_minutes: <achievable_rto_minutes>
- secondary_capacity: mode <pre-provisioned | scale-up>, percent_of_primary <n>, scale_up_minutes <n if scale-up>, quotas_verified <true after the quota request for full load is approved>

# DNS

- mechanism: <dns_mechanism>
- ttl_seconds: <60 or less on failover records>
- health_check: endpoint <URL>, interval_seconds <n>, failure_threshold <n>
- observed_propagation_seconds: <from the last drill>
- ttl_ignoring_clients: <client> -> fallback <global-load-balancer | anycast | client-side-retry-to-secondary>

# Database

- engine: <db_engine>
- replication: <replication>
- p99_lag_seconds_30d: <p99_lag_seconds>
- promotion_procedure: <runbook reference and command>
- fencing: <how the old primary stops accepting writes before promotion>
- single_writer_enforcement: <how only one writer endpoint can exist>

# Object store

- provider: <provider>
- replication_enabled: true
- versioning: true
- backlog_metric: <metric name>
- replication_time_alert: <alert and threshold>
- existing_objects_backfilled: <true | false>
- backfill_job: <job id and date when backfilled>

# Dependencies

One line per dependency on the failover path; a bypass is required when not reachable from the secondary.

- <name> kind <identity-provider | secrets-manager | ci-cd | dns-provider | certificate-issuance | payments | email | cloud-control-plane | other> reachable_from_secondary <true | false> bypass <text when false>

# Drill

Checklist (at least five steps: freeze, fence, promote, flip DNS, scale, synthetic transaction, record manual steps):

- <step>

- mechanics_last_changed_at: <mechanics_last_changed_at>
- last: date <YYYY-MM-DD>, scope_services <names>, traffic_percent <n>, measured_rto_minutes <n>, measured_rpo_minutes <n>, manual_steps <each step that needed a human>; or null

# Failback

- trigger: <condition that starts failback>
- rpo_minutes: <n>
- rto_minutes: <n>
- reconciliation_step: <how writes accepted in the secondary get home>
- procedure: <runbook reference>

# Decision

<decision_statement>

# Evidence

- <drill_report_url>
- <replication dashboard, quota request, backfill job>

# Review

- cadence: <review_cadence>
- next_review_at: <next_review_date>
