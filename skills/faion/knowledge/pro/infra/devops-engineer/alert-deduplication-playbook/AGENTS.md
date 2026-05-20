---
slug: alert-deduplication-playbook
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "2092bb0a890ecdf1"
summary: A 6-step playbook for on-call alert dedup — noise audit, fingerprint design, page-vs-ticket routing, suppression windows, paging SLOs, and quarterly review.
tags: [oncall, alerts, dedup, noise-audit, devops, pro, infra]
---
# Alert Deduplication Playbook

## Summary

**One-sentence:** A 6-step playbook for on-call alert deduplication — audit current noise, design alert fingerprints, route page-vs-ticket, configure suppression windows, set paging SLOs, and review quarterly — that turns a noisy alerting stack into a high-signal page channel.

**One-paragraph:** Alert fatigue is the #1 on-call complaint. `prometheus-monitoring` covers metric collection; this methodology fills the dedup / routing gap. The playbook: (1) export 30 days of alert history and classify into actionable / informational / noise; (2) design a fingerprint per alert family so duplicates collapse into the same incident; (3) split routing: page-worthy → on-call rotation, informational → ticket queue, noise → silence with quarterly re-evaluation; (4) configure suppression windows tied to remediation time; (5) set paging SLOs (e.g. &lt; 8 pages per week per rotation); (6) quarterly review. Output: a documented `alert-routing.yaml` and a measurable drop in pages-per-week.

## Applies If (ALL must hold)

- Team has an active alerting stack (Prometheus + AlertManager, Datadog, PagerDuty, OpsGenie, incident.io).
- Pages-per-week per on-call rotation is &gt;= 15 (the threshold above which dedup yields meaningful relief).
- Team controls the alert routing config (not locked behind a separate platform team).
- A 30-day alert history is queryable.

## Skip If (ANY kills it)

- Pages-per-week &lt; 5 — overhead exceeds the win; focus on alert quality instead.
- Team is in mid-migration to a new alerting stack — defer until post-migration.
- Pre-existing dedup work has been done in the last 90 days — re-run only if signal degraded.
- Team has no on-call rotation — dedup is moot.

## Prerequisites

- 30-day alert history export (CSV / JSON / DB query).
- Alert routing config writable by the team.
- An incident management tool (incident.io / FireHydrant / native AlertManager).
- A defined paging SLO target (default: &lt; 8 pages / week / rotation).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/prometheus-monitoring` | Metric source; this methodology operates downstream. |
| `pro/infra/devops-engineer/oncall-rotation-design` (if present) | Rotation structure feeds into paging SLOs. |
| `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps` | Per-alert runbooks complement dedup. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: noise-audit first, fingerprint discipline, page-vs-ticket gate, suppression with expiry, paging SLO | ~1100 |
| `content/02-output-contract.xml` | essential | alert-routing.yaml shape, audit-report shape, SLO dashboard | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: silenced alerts forgotten, fingerprint collision, oncall burnout | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|--------------|
| `noise-classify` | sonnet | Per-alert judgement: actionable / informational / noise |
| `fingerprint-design` | sonnet | Bounded judgement: which labels collapse to one fingerprint |
| `routing-rules-draft` | sonnet | Structured rule composition for alert-routing.yaml |
| `slo-trend-narrative` | sonnet | Synthesis of quarterly trends |

## Templates

| File | Purpose |
|------|---------|
| `templates/alert-routing.yaml` | Authoritative routing config: page vs ticket vs silenced + fingerprint per alert family |
| `templates/audit-report.md` | Quarterly audit-report template |
| `templates/slo-dashboard.json` | Grafana / Datadog dashboard JSON for paging SLO |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/noise-audit.py` | Read 30-day history; classify and emit per-alert recommendation | Quarterly + on demand |
| `scripts/fingerprint-validate.py` | Verify each alert family has a unique fingerprint definition | Before merging routing changes |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodologies: `prometheus-monitoring`, `oncall-rotation-design`, `observability-stack`
- external: [PagerDuty Alert Fatigue research](https://www.pagerduty.com/resources/learn/) · [Google SRE workbook Ch.8](https://sre.google/workbook/) · [AlertManager docs](https://prometheus.io/docs/alerting/latest/alertmanager/)
