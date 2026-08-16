# Kibana Queries, Dashboards, and Alerting

## Summary

**One-sentence:** Generates an ELK ops baseline (KQL query bank, Elasticsearch DSL aggregations, Watcher/Kibana alerting rules, dashboard inventory, kibana.yml hardening) for log-driven observability.

**One-paragraph:** Generates an ELK ops baseline (KQL query bank, Elasticsearch DSL aggregations, Watcher/Kibana alerting rules, dashboard inventory, kibana.yml hardening) for log-driven observability. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Operational dashboards (error rate, P99 latency, log volume) поверх ELK.
- Структурне розслідування інцидентів через KQL filters (рівень, service, env).
- Alerting на missing heartbeat logs та error-rate spikes (Watcher / Kibana Rules).
- Аудит kibana.yml для production (encryption keys, SSL, session TTL).

## Applies If (ALL must hold)

- Stack is ELK (Elasticsearch + Kibana) and remains the viewer of record for logs.
- Dashboards or alerts will be maintained over time (≥3 months horizon).
- At least one log shipper (Beats / Logstash / OTEL collector) is already feeding indices.

## Skip If (ANY kills it)

- Real-time sub-second metrics — Prometheus + Grafana is the better tool.
- Logs flow only to a non-Elastic store (Loki, Datadog) without ELK hybrid.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Log index pattern | list of `logs-*` indices | Platform team |
| Critical service registry | YAML (service → SLO) | SRE team |
| Notification channels | table (Slack / PagerDuty webhook) | SRE team |
| Role model | table (team → index permissions) | Platform team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-devops-elk-queries-alerting` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-instance.json` | JSON instance of a filled config artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-elk-queries-alerting.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-elk-architecture]]
- [[devops-elk-index-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config-instance.json`

```json
{
  "kql_query_bank": [
    {
      "name": "errors_by_service",
      "kql": "level: ERROR AND service: *"
    },
    {
      "name": "slow_post",
      "kql": "duration_ms > 5000 AND http.method: POST"
    }
  ],
  "alerts": [
    {
      "name": "high_error_rate",
      "rule_type": "es_query",
      "threshold": 100,
      "channel": "slack:#alerts"
    },
    {
      "name": "missing_heartbeat",
      "rule_type": "es_query",
      "threshold": 1,
      "channel": "pagerduty:platform"
    }
  ],
  "dashboards": [
    {
      "name": "service-ops",
      "path": "git@github.com:acme/kibana-dashboards.git"
    }
  ],
  "kibana_yml_hardening": {
    "encryption_key_set": true,
    "ssl_enabled": true,
    "session_idle_timeout": "1h"
  },
  "rbac": [
    {
      "role": "dev-api",
      "indices": [
        "logs-api-*"
      ]
    }
  ],
  "owner": "sre@acme.io",
  "last_reviewed": "2026-05-23"
}
```
