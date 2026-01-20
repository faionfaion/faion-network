# DevOps References

## Overview

Technical reference documentation for DevOps tools and practices. Each file provides comprehensive patterns, commands, and best practices for its respective technology.

---

## Files

### docker.md (~1140 lines)

Container development and deployment best practices.

**Contents:**
- Dockerfile patterns and base image selection
- Multi-stage builds for optimized images
- Docker Compose for multi-container apps
- Layer caching and optimization
- Security: non-root users, secrets, scanning
- Networking: bridge, host, overlay modes
- Volumes and storage management
- Registry operations and tagging

### kubernetes.md (~960 lines)

Kubernetes operations with kubectl, Helm, and Kustomize.

**Contents:**
- kubectl resource management commands
- Deployment, Service, ConfigMap, Secret manifests
- Namespace and RBAC operations
- Helm chart creation and management
- Kustomize overlays and patches
- Pod debugging and troubleshooting
- Resource requests/limits and QoS
- Ingress and networking configuration

### terraform.md (~1090 lines)

Infrastructure as Code with Terraform.

**Contents:**
- HCL syntax: resources, data sources, variables, outputs
- Expressions: conditionals, loops, dynamic blocks
- Module design and composition patterns
- State management: remote backends, locking
- Workspace-based environment separation
- Multi-provider configurations
- Testing with Terratest
- Import and state manipulation

### aws.md (~1480 lines)

AWS CLI operations and cloud infrastructure patterns.

**Contents:**
- CLI configuration and profile management
- EC2: instances, AMIs, security groups
- S3: bucket operations, sync, policies
- Lambda: deployment, invocation, layers
- IAM: users, roles, policies, MFA
- VPC: subnets, routing, NAT, peering
- ECR/ECS: container registry and orchestration
- CloudFormation and CDK basics

### gcp.md (~1400 lines)

Google Cloud CLI (gcloud) operations and infrastructure patterns.

**Contents:**
- gcloud CLI configuration and authentication
- Compute Engine: instances, disks, images, snapshots
- Cloud Storage: buckets, objects, lifecycle, IAM
- Cloud Functions: HTTP/event triggers, deployment
- Cloud Run: container deployment, traffic management
- GKE: clusters, node pools, upgrades
- Cloud SQL: PostgreSQL/MySQL instances, users
- BigQuery: datasets, tables, queries, loading
- IAM: service accounts, roles, policies
- VPC: networks, subnets, firewalls, load balancing
- Secret Manager: secrets, versions, access
- Pub/Sub: topics, subscriptions
- Artifact Registry: Docker repositories

### platform-engineering.md

Internal Developer Platforms (IDP), self-service infrastructure, golden paths, developer portals.

### gitops.md

Git as single source of truth, ArgoCD, Flux, progressive delivery, multi-cluster management.

### aiops.md

AI-powered operations, anomaly detection, auto-remediation, self-healing systems.

### dora-metrics.md

Four key DevOps metrics: deployment frequency, lead time, change failure rate, time to restore.

### finops.md

Cloud cost optimization, AI workload costs, FinOps practices, cost per unit of work.

### security-as-code.md

Policy as Code with OPA, Gatekeeper, Kyverno, DevSecOps practices.

---

## Usage

Load relevant reference files when working on specific technologies:

| Task | Reference |
|------|-----------|
| Writing Dockerfiles | docker.md |
| Kubernetes deployments | kubernetes.md |
| Infrastructure provisioning | terraform.md |
| AWS service configuration | aws.md |
| Google Cloud configuration | gcp.md |
| Platform Engineering / IDP | platform-engineering.md |
| GitOps / ArgoCD / Flux | gitops.md |
| AIOps / Self-healing | aiops.md |
| DevOps Metrics | dora-metrics.md |
| Cloud Costs | finops.md |
| Security Policies | security-as-code.md |

---

*Total: 11 reference files*
