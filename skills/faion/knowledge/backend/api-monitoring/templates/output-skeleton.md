<!-- purpose: minimal API Monitoring artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: config artefact validated by scripts/validate-api-monitoring.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# API Monitoring — Artefact

| Field | Value |
|-------|-------|
| artefact_id | api-monitoring-YYYY-MM-DD |
| owner | named human (no group terms) |
| last_touched | ISO-8601 timestamp |
| template_version | 1.1.0 |
| status | draft \| ready_for_review \| approved \| archived |

## Inputs

- Triggering activity: [from AGENTS.md Applies If list]
- Source-of-truth refs: [list URLs / design-file ids / dashboard snapshots]

## Methodology fields

| Field | Purpose |
|-------|---------|
| api_id | service id or repo slug |
| metrics_backend | prometheus|datadog|grafana-cloud|cloud-native |
| red_metrics | {rate_metric, errors_metric, duration_metric} naming conventions |
| structured_log_fields | minimum required fields [ts, level, request_id, route, status, latency_ms] |
| liveness_probe | path responding 200 only when the process is alive |
| readiness_probe | path responding 200 only when ready to serve traffic |
| slos | list of {journey, sli_definition, target, window, error_budget} |
| alert_rules | list of {name, expr, for_minutes, severity, runbook_url} |
| evidence | list of {source, citation} pairs anchoring SLOs and alert thresholds |
| status | draft|ready_for_review|approved|archived |

## Evidence

| Source | Citation |
|--------|----------|
| https://example.com/source-1 | verbatim quote |

## Self-check

- [ ] template_version pinned to 1.1.0
- [ ] owner is single named human (no team/us/tbd)
- [ ] every non-trivial field has ≥1 evidence row
- [ ] status is not approved unless a named reviewer signed off
- [ ] `scripts/validate-api-monitoring.py --file artefact.json` exits 0
