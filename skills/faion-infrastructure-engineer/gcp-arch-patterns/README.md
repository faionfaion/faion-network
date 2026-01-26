# GCP Architecture Patterns

## Overview

Production-ready GCP architectural patterns for GKE clusters, Cloud SQL databases, Cloud Storage with CDN, microservices, and data pipelines. Covers reference architectures based on Google Cloud Architecture Framework (2025-2026).

## When to Use

- Deploying production GKE clusters (regional, private, Autopilot)
- Setting up highly available databases (Cloud SQL, AlloyDB, Spanner)
- Implementing global CDN for static assets
- Multi-zone and multi-region deployments
- Microservices architectures on GKE/Cloud Run
- Data pipeline design (batch, streaming, hybrid)
- Platform engineering with Internal Developer Platforms

## Architecture Framework Pillars

Google Cloud Architecture Framework organizes best practices into 6 pillars:

| Pillar | Focus |
|--------|-------|
| System Design | Compute, storage, database building blocks |
| Operational Excellence | Observability, incident response, automation |
| Security, Privacy, Compliance | IAM, encryption, audit logging |
| Reliability | HA, DR, fault tolerance |
| Cost Optimization | Right-sizing, committed use, Spot VMs |
| Performance Optimization | Caching, autoscaling, global LB |

## Key Patterns

### Compute Patterns

| Pattern | Service | Use Case |
|---------|---------|----------|
| Regional GKE | GKE Standard/Autopilot | Production workloads, HA |
| Private GKE | GKE + Private nodes | Security-sensitive workloads |
| Serverless containers | Cloud Run | HTTP APIs, event-driven |
| Event-driven functions | Cloud Functions | Lightweight triggers, webhooks |
| Batch processing | Cloud Batch / GKE Jobs | ML training, data processing |

### Database Patterns

| Pattern | Service | Use Case |
|---------|---------|----------|
| Regional HA | Cloud SQL (REGIONAL) | Production OLTP |
| Read replicas | Cloud SQL + replicas | Read-heavy workloads |
| Global distribution | Spanner | Multi-region consistency |
| PostgreSQL compatible | AlloyDB | High-performance analytics |
| Document store | Firestore | Mobile/web apps |

### Data Pipeline Patterns

| Pattern | Components | Use Case |
|---------|------------|----------|
| Batch ETL | Cloud Storage -> Dataflow -> BigQuery | Daily/hourly loads |
| Streaming | Pub/Sub -> Dataflow -> BigQuery | Real-time analytics |
| CDC | Datastream -> BigQuery | Database replication |
| Data lakehouse | BigLake + Iceberg | Unified analytics |
| ML pipelines | Vertex AI Pipelines | Training workflows |

### Microservices Patterns

| Pattern | Implementation | Use Case |
|---------|----------------|----------|
| Service mesh | GKE + Istio/ASM | Observability, mTLS |
| API gateway | Cloud Endpoints / Apigee | External APIs |
| Event-driven | Pub/Sub + Cloud Run | Async communication |
| BFF | Cloud Run + GraphQL | Frontend-specific APIs |
| Saga orchestration | Workflows | Distributed transactions |

## Files in This Folder

| File | Description |
|------|-------------|
| [README.md](README.md) | This overview |
| [checklist.md](checklist.md) | Pre-deployment verification checklist |
| [examples.md](examples.md) | Terraform code examples |
| [templates.md](templates.md) | Reusable Terraform modules |
| [llm-prompts.md](llm-prompts.md) | Prompts for architecture design |

## Cost Optimization Tips

| Strategy | Savings | Trade-off |
|----------|---------|-----------|
| Spot VMs for batch | 60-91% | Preemption risk |
| Committed Use Discounts | 20-57% | 1-3 year commitment |
| Sustained Use Discounts | Up to 30% | Automatic, no commitment |
| Autoscaling (GKE, Cloud Run) | Variable | Cold start latency |
| BigQuery slots (flex/enterprise) | 30-50% | Capacity planning |

## References

- [Google Cloud Architecture Center](https://cloud.google.com/architecture)
- [GKE Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)
- [Cloud SQL High Availability](https://cloud.google.com/sql/docs/postgres/high-availability)
- [Cloud CDN Best Practices](https://cloud.google.com/cdn/docs/best-practices)
- [Microservices Demo (Online Boutique)](https://github.com/GoogleCloudPlatform/microservices-demo)
- [GCP Architecture Guides GitHub](https://github.com/GCP-Architecture-Guides/)
- [Dataflow Pipelines](https://cloud.google.com/dataflow/docs/concepts/beam-programming-model)

---

*GCP Architecture Patterns | faion-infrastructure-engineer*
