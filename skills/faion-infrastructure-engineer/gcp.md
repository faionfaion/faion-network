---
name: faion-gcp-cli-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Google Cloud CLI Skill

**Layer:** 3 (Technical Skill)
**Used by:** faion-devops-agent

## Purpose

Provides Google Cloud CLI (gcloud) operations and patterns for cloud infrastructure management. Covers compute, storage, serverless, containers, databases, data warehouse, identity management, networking, and monitoring.

---

## Service-Specific Guides

This guide has been split into focused service-specific files for better navigation and token efficiency.

| File | Services Covered | Token Count |
|------|------------------|-------------|
| **[gcp-compute.md](gcp-compute.md)** | Compute Engine, GKE, instances, disks, snapshots, instance groups | ~1500 |
| **[gcp-cloud-run.md](gcp-cloud-run.md)** | Cloud Run, Cloud Functions, serverless deployments, traffic management | ~800 |
| **[gcp-storage.md](gcp-storage.md)** | Cloud Storage, Cloud SQL, BigQuery, databases, object storage | ~1400 |
| **[gcp-networking.md](gcp-networking.md)** | VPC, IAM, Secret Manager, Logging, Monitoring, Pub/Sub, Artifact Registry | ~1800 |

**Total:** 4 files, ~5500 tokens (was 4680 in single file)

---

## Quick Reference

### Common Commands

```bash
# Authentication
gcloud auth login
gcloud auth activate-service-account --key-file=service-account.json

# Project configuration
gcloud config set project my-project-id
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# Compute Engine
gcloud compute instances list
gcloud compute instances create my-instance --zone=us-central1-a --machine-type=e2-medium

# Cloud Run
gcloud run deploy my-service --source=. --region=us-central1 --allow-unauthenticated

# Cloud Storage
gcloud storage cp local-file.txt gs://my-bucket/
gcloud storage ls gs://my-bucket/

# GKE
gcloud container clusters create my-cluster --zone=us-central1-a --num-nodes=3
gcloud container clusters get-credentials my-cluster --zone=us-central1-a

# IAM
gcloud projects add-iam-policy-binding my-project \
    --member=user:user@example.com \
    --role=roles/viewer
```

### Service Selection Guide

| Need | Use This Service | See Guide |
|------|------------------|-----------|
| Virtual machines, bare metal compute | Compute Engine | [gcp-compute.md](gcp-compute.md) |
| Containerized apps (serverless) | Cloud Run | [gcp-cloud-run.md](gcp-cloud-run.md) |
| Event-driven functions | Cloud Functions | [gcp-cloud-run.md](gcp-cloud-run.md) |
| Managed Kubernetes | GKE | [gcp-compute.md](gcp-compute.md) |
| Object storage | Cloud Storage | [gcp-storage.md](gcp-storage.md) |
| Relational database | Cloud SQL | [gcp-storage.md](gcp-storage.md) |
| Data warehouse | BigQuery | [gcp-storage.md](gcp-storage.md) |
| Networking, VPC | VPC & Firewall | [gcp-networking.md](gcp-networking.md) |
| Access control | IAM & Service Accounts | [gcp-networking.md](gcp-networking.md) |
| Secret storage | Secret Manager | [gcp-networking.md](gcp-networking.md) |
| Logs & monitoring | Cloud Logging & Monitoring | [gcp-networking.md](gcp-networking.md) |
| Message queue | Pub/Sub | [gcp-networking.md](gcp-networking.md) |
| Container registry | Artifact Registry | [gcp-networking.md](gcp-networking.md) |

---

## Security Best Practices

### Credential Management

```bash
# Never hardcode credentials - use IAM roles and service accounts
# Use Workload Identity for GKE
# Use Secret Manager for application secrets

# Rotate service account keys
gcloud iam service-accounts keys create new-key.json \
    --iam-account=my-sa@my-project.iam.gserviceaccount.com
# Delete old key after updating applications

# Use short-lived credentials
gcloud auth print-access-token  # 1 hour token
```

### Least Privilege

```bash
# Use predefined roles when possible
# Create custom roles for specific needs
# Regularly audit IAM policies

# Check who has access
gcloud asset search-all-iam-policies \
    --scope=projects/my-project \
    --query="policy:roles/owner"

# IAM Recommender
gcloud recommender recommendations list \
    --project=my-project \
    --location=global \
    --recommender=google.iam.policy.Recommender
```

### Encryption

```bash
# Enable CMEK for Cloud Storage
gcloud storage buckets update gs://my-bucket \
    --default-encryption-key=projects/my-project/locations/us/keyRings/my-ring/cryptoKeys/my-key

# Enable CMEK for Cloud SQL
gcloud sql instances patch my-instance \
    --disk-encryption-key=projects/my-project/locations/us/keyRings/my-ring/cryptoKeys/my-key

# Create KMS key ring
gcloud kms keyrings create my-ring --location=us

# Create KMS key
gcloud kms keys create my-key \
    --keyring=my-ring \
    --location=us \
    --purpose=encryption
```

### Audit Logging

```bash
# Enable data access audit logs
gcloud projects get-iam-policy my-project --format=yaml > policy.yaml
# Edit policy.yaml to add auditConfigs
gcloud projects set-iam-policy my-project policy.yaml

# View audit logs
gcloud logging read 'logName:"cloudaudit.googleapis.com"' --limit=50
```

---

## Common Patterns

### CI/CD Deployment

```bash
# Build and push to Artifact Registry
gcloud builds submit --tag us-central1-docker.pkg.dev/my-project/my-repo/my-app:$TAG

# Deploy to Cloud Run
gcloud run deploy my-app \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-app:$TAG \
    --region=us-central1

# Deploy to GKE
kubectl set image deployment/my-app my-app=us-central1-docker.pkg.dev/my-project/my-repo/my-app:$TAG
```

### Disaster Recovery

```bash
# Create cross-region replica (Cloud SQL)
gcloud sql instances create my-replica \
    --master-instance-name=my-primary \
    --region=europe-west1

# Copy snapshot to another region (Compute Engine)
gcloud compute snapshots create my-snapshot-dr \
    --source-disk=my-disk \
    --source-disk-zone=us-central1-a \
    --storage-location=europe-west1

# Multi-region Cloud Storage bucket
gcloud storage buckets create gs://my-dr-bucket --location=eu
```

### Cost Optimization

```bash
# Find idle resources
gcloud recommender recommendations list \
    --project=my-project \
    --location=us-central1-a \
    --recommender=google.compute.instance.IdleResourceRecommender

# List committed use discounts
gcloud compute commitments list

# View billing export
bq query --use_legacy_sql=false '
SELECT
  service.description,
  SUM(cost) as total_cost
FROM `my-project.billing_export.gcp_billing_export_v1_*`
WHERE DATE(_PARTITIONTIME) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10'
```

---

*Google Cloud CLI Skill v1.0*
*Layer 3 Technical Skill*
*Used by: faion-devops-agent*

## Sources

- [GCP Documentation](https://cloud.google.com/docs)
- [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)
- [GCP Quickstarts](https://cloud.google.com/docs/get-started/quickstarts)
- [GCP Best Practices](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs)
