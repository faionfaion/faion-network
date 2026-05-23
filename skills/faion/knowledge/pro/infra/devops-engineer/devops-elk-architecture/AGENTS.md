---
slug: devops-elk-architecture
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an ELK / EFK cluster architecture spec: node roles (master / data-hot / data-warm / coordinating), hot-warm-cold tier sizing, deployment model (ECK / Docker Compose), capacity plan.
content_id: "727514d49792025f"
complexity: medium
produces: spec
est_tokens: 4400
tags: [elk, elasticsearch, logging, observability, devops]
---

# ELK Stack Architecture and Deployment

## Summary

**One-sentence:** Produces an ELK / EFK cluster architecture spec: node roles (master / data-hot / data-warm / coordinating), hot-warm-cold tier sizing, deployment model (ECK / Docker Compose), capacity plan.

**One-paragraph:** A flat single-node Elasticsearch collapses under production log volumes. This methodology produces an architecture spec naming the stack variant (ELK / EFK / Elastic Stack with Beats), the node-role split (master / data-hot / data-warm / coordinating), the hot-warm-cold tier sizing (SSD ↔ HDD), the deployment model (Elastic Cloud on Kubernetes / Docker Compose), and a capacity plan keyed to expected log volume (GB/day) + retention. Output: spec doc + ECK / docker-compose manifest + capacity-plan spreadsheet.

**Ефективно для:**

- Централізація логів з декількох сервісів у searchable store.
- Operational dashboards troubleshooting across microservices.
- Compliance logging (GDPR/HIPAA/SOC2) з long retention.
- Alerting на log patterns / error rates.
- Security analytics (SIEM) — full-text search log events.

## Applies If (ALL must hold)

- Log volume ≥ 10 GB/day OR retention ≥ 30 days (smaller fits managed services).
- Need for full-text search across log content (not just metric labels).
- Team has capacity to operate Elasticsearch (or use ECK managed).

## Skip If (ANY kills it)

- Single small app, low volume — Loki+Grafana / Datadog / CloudWatch has lower op overhead.
- Cost-sensitive env where Loki's label-based model is sufficient.
- Pure metrics-only observability — Prometheus+Grafana covers this.
- OpenSearch preference — use the AWS fork instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Log volume estimate | GB/day + retention | log audit / app team |
| Tier budget | $/mo for hot + warm + cold storage | finance |
| Deployment substrate | K8s / Docker Compose / VMs | platform team |
| Compliance retention | regulation-driven days | GRC |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[devops-elk-beats-collection]] | Ingest agents feed the cluster |
| [[devops-elk-index-management]] | ILM policies live there |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: node-roles-split, hot-warm-cold-tiers, 3-master-nodes, capacity-plan-numeric, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for ELK arch spec + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: flat-cluster, 2-master-split-brain, no-tier-separation, undersized-heap | 800 |
| `content/04-procedure.xml` | essential | 5 steps: volume estimate → node count → role assignment → tier sizing → deploy | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on volume + budget → topology | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `estimate-volume` | haiku | Mechanical GB/day × retention math. |
| `design-topology` | sonnet | Node role + count + tier assignment. |
| `write-manifest` | sonnet | ECK manifest or docker-compose. |

## Templates

| File | Purpose |
|------|---------|
| `templates/elk-arch-spec.md` | Markdown skeleton for the ELK architecture spec |
| `templates/eck-manifest.yaml` | Sample ECK Elasticsearch CRD with role split + hot-warm tiers |
| `templates/_smoke-test.json` | Minimum spec used by validate-devops-elk-architecture.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-elk-architecture.py` | Validate the spec artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[devops-elk-beats-collection]]
- [[devops-elk-index-management]]
- [[devops-elk-logstash-pipeline]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when sizing a new ELK cluster or auditing an existing one.
