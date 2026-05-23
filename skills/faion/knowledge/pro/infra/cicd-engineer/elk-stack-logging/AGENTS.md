---
slug: elk-stack-logging
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an ELK (or OpenSearch) deployment recipe (Elasticsearch + Logstash/Vector + Kibana + Filebeat/Vector agents) with ILM, security, and dashboards for production observability.
content_id: "48da6c9dab76cf9d"
complexity: deep
produces: config
est_tokens: 4500
tags: ["elasticsearch", "logstash", "kibana", "logging", "observability"]
---
# ELK / OpenSearch Centralized Logging

## Summary

**One-sentence:** Generates an ELK (or OpenSearch) deployment recipe (Elasticsearch + Logstash/Vector + Kibana + Filebeat/Vector agents) with ILM, security, and dashboards for production observability.

**One-paragraph:** ELK / OpenSearch Centralized Logging — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a config that the downstream agent can verify with the included validator.

**Ефективно для:**

- Multi-service production environment producing > 10GB of logs per day requiring centralized search.
- Existing point-in-time logs (journald per host) need correlated query across hosts/services.
- Compliance regime requires retained, searchable logs with access control.

## Applies If (ALL must hold)

- Multi-service production environment producing > 10GB of logs per day requiring centralized search.
- Existing point-in-time logs (journald per host) need correlated query across hosts/services.
- Compliance regime requires retained, searchable logs with access control.

## Skip If (ANY kills it)

- Single-host deployment where journald + grep is sufficient.
- Already on a managed observability platform (Datadog, NewRelic) covering log needs.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal / spec | text / Markdown | user |
| Domain context | XML | `pro/infra/cicd-engineer/AGENTS.md` |
| Inventory of in-scope resources | list / JSON | infra catalog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[docker-optimization]] | Sibling methodology — shared vocabulary and patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (ilm-required, security-enabled, structured-logs-only, trace-id-correlation, agent-mtls-or-token, kibana-saved-dashboards, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the config + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-elk-stack-logging` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/elasticsearch.yml` | Elasticsearch config skeleton with security + ILM |
| `templates/ilm-policy.json` | ILM policy skeleton (hot/warm/cold/delete) |
| `templates/filebeat.yml` | Filebeat config skeleton with mTLS and structured-log shipping |
| `templates/backup-config.example.json` | Filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-elk-stack-logging.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[docker-optimization]]
- [[dora-metrics]]
- [[cicd-tls-validation-gate]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
