---
slug: vector-db-setup-prod
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "ffe203c994b76636"
summary: Deploys a vector DB to production — Docker Compose (single-node), Kubernetes StatefulSet/Helm (multi-node), or managed — with persistence, health-checks, resource limits, HA, backup/recovery, and a pre/post-deploy checklist.
complexity: deep
produces: config
est_tokens: 4000
tags: [vector-database, kubernetes, production, docker-compose, terraform]
---

# Vector Database Production Deployment

## Summary

**One-sentence:** Production deployment manifest — Docker Compose for single-node, K8s StatefulSet/Helm for multi-node, managed for hands-off — with persistence, health checks, resource limits, HA, backup, restore drill, and a pre/post-deploy checklist.

**One-paragraph:** Moving from dev to prod requires more than `docker run`. Persistence: bind to durable storage class (EBS gp3, Ceph RBD); resource limits: CPU + memory requests + limits to prevent neighbour kills; HA: ≥3 replicas for Milvus/Weaviate, single replica + snapshots for Qdrant; backup: snapshot to S3 every 24h with 30-day retention + restore drilled quarterly. Output: a versioned `prod-deploy.yaml` + Terraform / Helm values + ops runbook.

**Ефективно для:**

- Self-host команд що готують Qdrant / Weaviate / Milvus у K8s — стандартизує HA + backup discipline.
- Migrations dev → prod — checklist гарантує що persistence + monitoring + security вже на місці.
- DR drills — quarterly restore тест плюс runbook = real recovery confidence.
- Multi-region — Helm values для cross-region replication.

## Applies If (ALL must hold)

- Vector DB choice committed (`vector-databases` decision done)
- Production environment (real users, real data)
- Operational support exists (on-call, monitoring, backups)

## Skip If (ANY kills it)

- Dev / staging — use vector-db-setup-dev
- Fully managed DB (Pinecone) — provider handles ops; just configure tier
- Air-gapped network with manual operations — different methodology

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `cluster-topology.yaml` | YAML | infra (K8s cluster spec) |
| `storage-class-map.yaml` | YAML | available storage tiers |
| `backup-retention-policy.yaml` | YAML | compliance / DR requirements |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `vector-databases` | DB chosen |
| `vector-db-setup-dev` | Dev baseline |
| `vector-db-monitoring` | Monitoring stack |
| `vector-db-security` | Security baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: durable persistence, resource limits, HA per DB class, backup + restore drilled, pre+post deploy checklist | 1100 |
| `content/02-output-contract.xml` | essential | prod-deploy.yaml schema | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: ephemeral volume, no limits, single replica without snapshot, untested backup, no rollback | 900 |
| `content/04-procedure.xml` | essential | 6 steps: storage class → resource sizing → HA mode → backup → checklist → ship | 900 |
| `content/05-examples.xml` | essential | Worked example: Qdrant K8s StatefulSet with EBS + daily snapshot | 600 |
| `content/06-decision-tree.xml` | essential | Routes by DB kind + scale → deploy mode (compose / statefulset / managed) | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `helm_values_drafting` | sonnet | Schema synthesis |
| `runbook_drafting` | opus | Cross-system thinking |
| `prod_deploy_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/qdrant-statefulset.yaml` | K8s StatefulSet for Qdrant |
| `templates/backup-cronjob.yaml` | K8s CronJob for snapshot |
| `templates/prod-deploy.schema.yaml` | Schema |
| `templates/_smoke-test.yaml` | Minimum-viable spec |
| `templates/deploy-checklist.md` | Pre+post deploy checklist |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vector-db-setup-prod.py` | Lint prod-deploy.yaml | Pre-commit |

## Related

- [[vector-databases]] · [[vector-db-setup-dev]] · [[vector-db-monitoring]] · [[vector-db-security]] · [[vector-db-index-tuning]]
- external: [Qdrant K8s](https://github.com/qdrant/qdrant-helm) · [Milvus on K8s](https://milvus.io/docs/install_cluster-helm.md)

## Decision tree

See `content/06-decision-tree.xml`. Routes by DB kind + scale + ops profile to {single-node compose, StatefulSet/Helm, managed}.
