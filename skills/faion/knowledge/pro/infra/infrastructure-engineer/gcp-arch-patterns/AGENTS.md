# GCP Architecture Patterns

## Summary

Production-ready GCP architectural patterns for GKE clusters, Cloud SQL, Cloud Storage with CDN, microservices on Cloud Run, and data pipelines (Dataflow + BigQuery). The concrete rule is: always use regional GKE clusters with private nodes, Workload Identity, and managed Prometheus; always set Cloud SQL `availability_type = REGIONAL` with PITR for production; always use Spot VMs with taints for batch workloads.

## Why

GCP's defaults favor availability over security — public IPs, zonal databases, no Workload Identity. Following these patterns eliminates the most common production failures: single-AZ database outages, secret leaks via node metadata, and cold-start latency from under-sized node pools.

## When To Use

- Deploying production GKE clusters (regional, private, node pool strategy)
- Setting up Cloud SQL PostgreSQL with HA, PITR, and read replicas
- Implementing CDN for static assets via Cloud Storage + Global LB
- Building microservices with Cloud Run, Pub/Sub, and Secret Manager
- Designing data pipelines (batch ETL or streaming with Dataflow + BigQuery)
- Migrating from AWS to GCP equivalent services

## When NOT To Use

- GCP project hierarchy, IAM, and billing basics — use `gcp-arch-basics`
- GCP Compute Engine (VMs, instance groups) — use `gcp-compute`
- GCP networking (VPC, firewall, Cloud NAT) — use `gcp-networking`
- GCP Cloud Storage lifecycle and CMEK — use `gcp-storage`
- AWS architecture decisions — use `aws-architecture-services`

## Content

| File | What's inside |
|------|---------------|
| `content/01-gke-patterns.xml` | Regional cluster rules, node pool strategies, security config (Workload Identity, Binary Authorization, SnapStart) |
| `content/02-database-patterns.xml` | Cloud SQL HA config, read replica, AlloyDB vs Spanner decision, backup rules |
| `content/03-microservices-data.xml` | Cloud Run patterns, Pub/Sub with DLQ, Dataflow streaming, BigQuery partitioning rules |
| `content/04-checklist.xml` | Pre-deployment checklist: GKE, Cloud SQL, CDN, networking, security, monitoring |

## Templates

| File | Purpose |
|------|---------|
| `templates/gke-module-variables.tf` | GKE module variables with node pool object type |
| `templates/gke-module-main.tf` | Regional private GKE cluster with all security settings |
| `templates/cloudsql-module-main.tf` | Cloud SQL HA with PITR, insights, flags, read replica |
| `templates/cloudrun-services.tf` | Multi-service Cloud Run deployment with Workload Identity |
