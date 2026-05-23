---
slug: alert-deduplication-playbook
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an alert-routing.yaml + audit report that turns a noisy alerting stack into a high-signal page channel under a paging SLO.
content_id: "d3e28d41149d3daf"
complexity: deep
produces: playbook-step
est_tokens: 4500
tags: [oncall, alerts, dedup, noise-audit, devops]
---
# Alert Deduplication Playbook

## Summary

**One-sentence:** Produces an alert-routing.yaml + audit report that turns a noisy alerting stack into a high-signal page channel under a paging SLO.

**One-paragraph:** Alert fatigue is the #1 on-call complaint. `prometheus-monitoring` covers metric collection; this methodology fills the dedup + routing gap. The playbook: export 30 days of alert history and classify into actionable / informational / noise; design a fingerprint per family so duplicates collapse; split routing into page-worthy / ticket / silenced; configure suppression with expiry; set paging SLOs; review quarterly. Output: an `alert-routing.yaml` and a measurable drop in pages-per-week.

**Ефективно для:**

- >=15 pages/week/rotation — alert dedup приносить вимірне полегшення для on-call.
- коли prometheus-monitoring покриває collection, а dedup/routing gap залишається.
- 30-day alert history queryable + team controls routing config.
- paging SLO target <=8 pages/week треба моніторити quarterly.

## Applies If (ALL must hold)

- Team has an active alerting stack (Prometheus + AlertManager, Datadog, PagerDuty, OpsGenie, incident.io).
- Pages-per-week per on-call rotation is >= 15 (the threshold above which dedup yields meaningful relief).
- Team controls the alert routing config (not locked behind a separate platform team).
- A 30-day alert history is queryable.

## Skip If (ANY kills it)

- Pages-per-week < 5 — overhead exceeds the win; focus on alert quality instead.
- Team is in mid-migration to a new alerting stack — defer until post-migration.
- Pre-existing dedup work has been done in the last 90 days — re-run only if signal degraded.
- Team has no on-call rotation — dedup is moot.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 30-day alert history export | CSV / JSON / DB query | alerting platform |
| Alert routing config | writable repo | team |
| Incident management tool | incident.io / FireHydrant / AlertManager | team |
| Paging SLO target | number | engineering lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/prometheus-monitoring` | metric source; this methodology operates downstream |
| `pro/infra/devops-engineer/oncall-rotation-design` | rotation structure feeds into paging SLOs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes r1-noise-audit-first) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `noise-classify` | sonnet | Per-alert judgement: actionable / informational / noise |
| `fingerprint-design` | sonnet | Bounded judgement: which labels collapse to one fingerprint |
| `routing-rules-draft` | sonnet | Structured rule composition for alert-routing.yaml |
| `slo-trend-narrative` | sonnet | Synthesis of quarterly trends |

## Templates

| File | Purpose |
|------|---------|
| `templates/alert-routing.yaml` | Authoritative routing config with fingerprints |
| `templates/audit-report.md` | Quarterly audit report skeleton |
| `templates/slo-dashboard.json` | Grafana / Datadog paging-SLO dashboard JSON |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-alert-deduplication-playbook.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[prometheus-monitoring]]
- [[alert-noise-budget]]
- [[oncall-rotation-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Alert Deduplication Playbook methodology when in doubt about scope or fit.
