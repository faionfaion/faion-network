---
slug: vector-db-setup-prod
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Deploy vector databases to production using Docker Compose (single-node), Kubernetes StatefulSets or Helm (multi-node), or managed cloud services; covers persistence, health checks, resource limits, high availability, backup/recovery, and the pre/post-deployment checklists required before serving live traffic.
content_id: "ffe203c994b76636"
tags: [vector-database, kubernetes, production, docker-compose, terraform]
---
# Vector Database Production Deployment

## Summary

**One-sentence:** Deploy vector databases to production using Docker Compose (single-node), Kubernetes StatefulSets or Helm (multi-node), or managed cloud services; covers persistence, health checks, resource limits, high availability, backup/recovery, and the pre/post-deployment checklists required before serving live traffic.

**One-paragraph:** Deploy vector databases to production using Docker Compose (single-node), Kubernetes StatefulSets or Helm (multi-node), or managed cloud services; covers persistence, health checks, resource limits, high availability, backup/recovery, and the pre/post-deployment checklists required before serving live traffic.

## Applies If (ALL must hold)

- Deploying a vector database to serve real traffic (RAG pipeline, semantic search, recommendations).
- Migrating from a development Docker setup to a hardened production environment.
- Setting up Kubernetes StatefulSets or Helm releases for any major vector engine.
- Provisioning managed cloud vector services (Qdrant Cloud, Weaviate Cloud, Zilliz, Pinecone Serverless) with VPC and auth.
- Establishing disaster recovery with backup schedules and tested restore procedures.

## Skip If (ANY kills it)

- Still evaluating database engines — stand up dev instances first (see vector-db-setup-dev).
- Fully managed RAG without an ops team — use Pinecone Serverless or Weaviate Cloud; no infra required.
- Prototype with fewer than 100K vectors — the complexity overhead exceeds the benefit.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ml-engineer/`
