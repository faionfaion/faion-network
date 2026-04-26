# GCP

## Summary

GCP production deployments: use Autopilot mode for GKE (pay-per-pod, no node management) unless GPU workloads or privileged containers are required; use Workload Identity Federation to eliminate service account keys for all external workloads (GitHub Actions, GitLab CI, AWS); use Private Service Connect instead of VPC Peering for Google-managed service access. Never assign primitive IAM roles (Owner, Editor, Viewer) to service accounts.

## Why

Service account keys are the leading cause of GCP credential exposure — Workload Identity Federation eliminates them by mapping external OIDC tokens directly to IAM principals. Autopilot reduces operational overhead by 60-80% vs Standard mode: no node pool sizing, no OS patching, no kubelet config. Spot VMs (formerly Preemptible) save 60-91% on batch and CI workloads with minimal code changes.

## When To Use

- Deploying containerized workloads on GKE (prefer Autopilot)
- Running serverless containers with Cloud Run
- Authenticating GitHub Actions or other OIDC providers to GCP without long-lived keys
- Multi-project GCP organization requiring Shared VPC and centralized networking
- BigQuery/analytics workloads requiring data warehouse integration

## When NOT To Use

- Multi-cloud architecture requiring vendor-neutral IaC — use Terraform + cloud-agnostic abstractions instead of GCP-specific tools (Deployment Manager, Cloud Build)
- Workloads requiring Windows Server containers — GKE has limited Windows node support
- Very small workload (&lt; $50/month projected) where the Autopilot per-pod pricing exceeds a minimal VM — Cloud Run or a single e2-micro may be more cost-effective
- Team has no GCP IAM expertise — incorrect organization-level IAM bindings are hard to audit and undo

## Content

| File | What's inside |
|------|---------------|
| `content/01-gke-cloudrun.xml` | GKE Autopilot vs Standard decision, node pool patterns, Cloud Run configuration, Spot VM usage |
| `content/02-iam-networking.xml` | Workload Identity Federation setup, service account best practices, VPC design, Shared VPC, Private Service Connect |

## Templates

| File | Purpose |
|------|---------|
| `templates/gke-autopilot.tf` | Terraform GKE Autopilot cluster with Workload Identity and private networking |
| `templates/cloud-run-deploy.sh` | Cloud Run blue-green deploy script with traffic splitting |
| `templates/workload-identity-sa.yaml` | K8s ServiceAccount annotation for GKE Workload Identity binding |
| `templates/prompt-cost-review.txt` | LLM prompt for GCP cost optimization review |
