# GCP Infrastructure

**Google Cloud Platform Infrastructure Best Practices (2025-2026)**

---

## Overview

| Category | Services | Key Features |
|----------|----------|--------------|
| Compute | Compute Engine, GKE, Instance Groups | VMs, Kubernetes, autoscaling |
| Serverless | Cloud Run, Cloud Functions | Containers, event-driven |
| Networking | VPC, Cloud NAT, Load Balancing, Cloud Armor | Private networks, global LB |
| IAM | Roles, Service Accounts, Workload Identity | Zero-trust, least privilege |
| Storage | Cloud Storage, Cloud SQL, BigQuery | Object, relational, analytics |
| Operations | Cloud Logging, Monitoring, Secret Manager | Observability, secrets |

## Shared Responsibility Model

| Google Manages | Customer Manages |
|----------------|------------------|
| Physical infrastructure | IAM configuration |
| Host OS/hypervisor | Data classification |
| Default encryption | Application security |
| Network infrastructure | Workload configuration |
| Global data centers | Service account keys |

## Security Framework (2025-2026)

### Core Principles

| Principle | Implementation |
|-----------|----------------|
| Least Privilege | Predefined roles, custom roles, IAM Recommender |
| Zero Trust | VPC Service Controls, context-aware access |
| Defense in Depth | VPC-SC + Firewall + Cloud Armor + IAM |
| Keyless Auth | Workload Identity Federation (no service account keys) |
| Encryption | CMEK with Cloud KMS, automatic rotation |

### VPC Service Controls (VPC-SC)

VPC-SC defines security perimeters around sensitive GCP resources:

```
Perimeter Boundary
├── Cloud Storage buckets
├── BigQuery datasets
├── Cloud SQL instances
└── Other API resources
```

**Key practices:**
- Mandatory dry-run phase before enforcement
- Layer with firewalls, Cloud Armor, and IAM
- Stream audit logs to SIEM (Splunk, Chronicle)
- Use IaC (Terraform) for consistent deployment

## gcloud CLI Configuration

### Installation

```bash
# Install gcloud CLI (Linux)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Via apt (Debian/Ubuntu)
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
    sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt update && sudo apt install google-cloud-cli

# Verify
gcloud version
```

### Authentication

```bash
# Interactive login
gcloud auth login

# Service account (CI/CD)
gcloud auth activate-service-account --key-file=service-account.json

# Application default credentials (local dev)
gcloud auth application-default login

# List accounts
gcloud auth list
```

### Configuration Management

```bash
# Set defaults
gcloud config set project my-project-id
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# Named configurations
gcloud config configurations create production
gcloud config configurations activate production
gcloud config configurations list

# View current
gcloud config list
```

### Environment Variables

```bash
# Project
export CLOUDSDK_CORE_PROJECT="my-project-id"

# Region/Zone
export CLOUDSDK_COMPUTE_REGION="us-central1"
export CLOUDSDK_COMPUTE_ZONE="us-central1-a"

# Service account
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Disable prompts (CI/CD)
export CLOUDSDK_CORE_DISABLE_PROMPTS=1
```

## Service Selection Guide

| Need | Service | Guide |
|------|---------|-------|
| VMs, persistent workloads | Compute Engine | [gcp-compute.md](../gcp-compute.md) |
| Managed Kubernetes | GKE | [gcp-compute.md](../gcp-compute.md) |
| Containerized apps (serverless) | Cloud Run | [gcp-cloud-run.md](../gcp-cloud-run.md) |
| Event-driven functions | Cloud Functions (Gen2) | [gcp-cloud-run.md](../gcp-cloud-run.md) |
| Object storage | Cloud Storage | [gcp-storage.md](../gcp-storage.md) |
| Relational database | Cloud SQL / AlloyDB | [gcp-storage.md](../gcp-storage.md) |
| Data warehouse | BigQuery | [gcp-storage.md](../gcp-storage.md) |
| VPC, networking | VPC, Firewall | [gcp-networking.md](../gcp-networking.md) |
| Access control | IAM, Service Accounts | [gcp-networking.md](../gcp-networking.md) |
| Secrets | Secret Manager | [gcp-networking.md](../gcp-networking.md) |
| Container registry | Artifact Registry | [gcp-networking.md](../gcp-networking.md) |

## Deployment Patterns

### CI/CD Pipeline

```bash
# Build and push to Artifact Registry
gcloud builds submit \
    --tag us-central1-docker.pkg.dev/my-project/my-repo/my-app:$TAG

# Deploy to Cloud Run
gcloud run deploy my-app \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-app:$TAG \
    --region=us-central1 \
    --service-account=my-app@my-project.iam.gserviceaccount.com

# Deploy to GKE
kubectl set image deployment/my-app \
    my-app=us-central1-docker.pkg.dev/my-project/my-repo/my-app:$TAG
```

### Disaster Recovery

```bash
# Cross-region Cloud SQL replica
gcloud sql instances create my-replica \
    --master-instance-name=my-primary \
    --region=europe-west1

# Cross-region snapshot
gcloud compute snapshots create my-snapshot-dr \
    --source-disk=my-disk \
    --source-disk-zone=us-central1-a \
    --storage-location=europe-west1

# Multi-region storage
gcloud storage buckets create gs://my-dr-bucket --location=eu
```

## Cost Optimization

```bash
# Find idle resources
gcloud recommender recommendations list \
    --project=my-project \
    --location=us-central1-a \
    --recommender=google.compute.instance.IdleResourceRecommender

# IAM Recommender (remove unused permissions)
gcloud recommender recommendations list \
    --project=my-project \
    --location=global \
    --recommender=google.iam.policy.Recommender

# List committed use discounts
gcloud compute commitments list

# Billing analysis
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

## Related References

| Document | Description |
|----------|-------------|
| [checklist.md](checklist.md) | Security and operational checklists |
| [examples.md](examples.md) | Compute, IAM, networking examples |
| [templates.md](templates.md) | Terraform templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for GCP tasks |
| [gcp-compute.md](../gcp-compute.md) | Compute Engine, GKE |
| [gcp-cloud-run.md](../gcp-cloud-run.md) | Cloud Run, Cloud Functions |
| [gcp-storage.md](../gcp-storage.md) | Cloud Storage, Cloud SQL, BigQuery |
| [gcp-networking.md](../gcp-networking.md) | VPC, IAM, Secret Manager |

## Sources

- [GCP Documentation](https://cloud.google.com/docs)
- [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)
- [GCP Best Practices](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations)
- [GCP Security Best Practices 2026](https://fidelissecurity.com/cybersecurity-101/best-practices/google-cloud-platform-gcp-security/)
- [GCP Security Checklist 2026](https://www.sentinelone.com/cybersecurity-101/cloud-security/gcp-security-checklist/)
- [VPC Service Controls at Enterprise Scale](https://www.infoq.com/articles/preventing-data-exfiltration-google-cloud/)
- [Production-Ready GCP with Terraform 2025](https://dev.to/livingdevops/build-production-ready-google-cloud-infrastructure-with-terraform-in-2025-1jj7)

---

*GCP Infrastructure | faion-infrastructure-engineer*
