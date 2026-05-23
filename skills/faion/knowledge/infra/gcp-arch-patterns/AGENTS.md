# Gcp Arch Patterns

## Summary

**One-sentence:** Production-ready GCP patterns: regional GKE, Cloud SQL HA, Cloud Run with VPC egress, Pub/Sub DLQ, Dataflow+BigQuery. Concrete commands and verifications.

**One-paragraph:** Production-ready GCP architectural patterns for GKE clusters, Cloud SQL, Cloud Storage with CDN, microservices on Cloud Run, and data pipelines (Dataflow + BigQuery). Concrete rules: regional GKE with private nodes, Workload Identity, managed Prometheus; Cloud SQL `availability_type = REGIONAL` with PITR for production; Spot VMs with taints for batch.

**Ефективно для:**

- Нова production-grade GKE кластер з Workload Identity + private nodes.
- Cloud SQL HA (REGIONAL) + PITR + read replicas для прод-БД.
- Static-assets CDN через Cloud Storage + Global HTTPS LB.
- Microservices на Cloud Run з Pub/Sub + Secret Manager.
- Data pipeline: Pub/Sub → Dataflow → BigQuery (batch + streaming).

## Applies If (ALL must hold)

- Provisioning a new production GKE cluster (regional, private, node-pool strategy).
- Setting up Cloud SQL PostgreSQL with HA, PITR, and read replicas.
- Implementing CDN for static assets via Cloud Storage + Global LB.
- Building microservices with Cloud Run, Pub/Sub, and Secret Manager.
- Designing data pipelines (batch ETL or streaming via Dataflow + BigQuery).
- Migrating from AWS to GCP equivalent services (EKS→GKE, RDS→Cloud SQL, SQS→Pub/Sub).

## Skip If (ANY kills it)

- Project hierarchy / IAM basics — use `gcp-resource-hierarchy` + `gcp-iam-design`.
- Single-service prototype without HA requirements.
- AWS architecture decisions — use the AWS methodologies.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target pattern | GKE / Cloud SQL / data-pipeline / CDN | architect |
| HA / SLO targets | RPO/RTO + uptime targets | product owner |
| Compliance constraints | data-residency / regulatory | security |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cloud-run-jobs]] | Sibling methodology that supplies context required here. |
| [[cloud-run-monitoring]] | Sibling methodology that supplies context required here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with statement + rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule id from 01-core-rules | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision tree application — needs nuance + context awareness. |
| `draft-spec` | sonnet | Light judgement on field selection + naming conventions. |
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gcp-arch-patterns.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gcp-arch-patterns.md` | Skeleton for the spec artefact this methodology produces. |
| `templates/_smoke-test.md` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-arch-patterns.py` | Validate the spec artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[cloud-run-jobs]]
- [[cloud-run-monitoring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gcp-arch-patterns vs an adjacent sibling).
