# Google Cloud Platform Skill

**Layer:** 3 (Technical Skill)
**Used by:** faion-devops-engineer, faion-infrastructure-engineer

## Purpose

Comprehensive Google Cloud Platform operations covering compute, storage, serverless, containers (GKE), databases, identity management (IAM), networking, and monitoring. Updated with 2025-2026 best practices.

---

## Quick Navigation

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and architecture guidance |
| [checklist.md](checklist.md) | Pre-deployment and security checklists |
| [examples.md](examples.md) | CLI commands and code examples |
| [templates.md](templates.md) | Reusable configurations and scripts |
| [llm-prompts.md](llm-prompts.md) | Prompts for GCP task automation |

---

## Core Services

### Compute

| Service | Use Case | Cost Model |
|---------|----------|------------|
| Compute Engine | VMs, persistent workloads | Per-second billing |
| GKE | Container orchestration | Per-cluster + nodes |
| GKE Autopilot | Managed Kubernetes | Per-pod resources |
| Cloud Run | Serverless containers | Per-request + CPU/memory |
| Cloud Functions | Event-driven functions | Per-invocation |

### Storage

| Service | Use Case | Storage Class |
|---------|----------|---------------|
| Cloud Storage | Object storage | Standard, Nearline, Coldline, Archive |
| Persistent Disk | Block storage for VMs | pd-standard, pd-balanced, pd-ssd |
| Filestore | Managed NFS | Basic, High Scale, Enterprise |

### Database

| Service | Type | Use Case |
|---------|------|----------|
| Cloud SQL | Managed RDBMS | PostgreSQL, MySQL, SQL Server |
| Cloud Spanner | Global relational | Mission-critical, global scale |
| Firestore | Document DB | Mobile/web apps, real-time |
| BigQuery | Data warehouse | Analytics, ML |
| Memorystore | Managed cache | Redis, Memcached |

### Networking

| Service | Purpose |
|---------|---------|
| VPC | Virtual network |
| Shared VPC | Multi-project networking |
| Private Service Connect | Private access to Google APIs |
| Cloud NAT | Outbound internet access |
| Cloud Load Balancing | Global/regional load balancing |
| Cloud CDN | Content delivery |
| Cloud Armor | DDoS protection, WAF |

---

## GKE Best Practices (2025-2026)

### Mode Selection

| Mode | When to Use |
|------|-------------|
| **Autopilot** (recommended) | Most workloads, simplified operations, pay-per-pod |
| **Standard** | GPU workloads, custom node configs, privileged containers |
| **Hybrid** | Standard cluster with Autopilot workloads (new 2025) |

### Autopilot Key Features

- **In-place Pod Resize** (GA): Change CPU/memory without restart
- **Fast-starting nodes** (GA): Rapid scaling
- **Container-optimized compute**: Dynamic node resizing
- **Automatic node provisioning**: No manual node pool management

### Standard Mode Optimization

```yaml
# Node pool best practices
node_pools:
  - name: general
    machine_type: e2-standard-4
    autoscaling:
      min_nodes: 1
      max_nodes: 10
  - name: spot-batch
    machine_type: n2-standard-8
    spot: true
    taints:
      - key: "workload"
        value: "batch"
        effect: "NoSchedule"
```

### Cost Optimization

1. **Use Spot VMs** for batch jobs, CI/CD (70-90% savings)
2. **Enable Cluster Autoscaler** with appropriate min/max
3. **Right-size pods** with resource requests/limits
4. **Use node auto-provisioning** for dynamic workloads
5. **Committed Use Discounts** for steady-state workloads

---

## Cloud Run Best Practices (2025-2026)

### Pricing Model

| Resource | Free Tier | Pricing |
|----------|-----------|---------|
| CPU | 180,000 vCPU-sec/month | $0.00002400/vCPU-sec |
| Memory | 360,000 GiB-sec/month | $0.00000250/GiB-sec |
| Requests | 2 million/month | $0.40/million |

### Configuration Guidelines

| Setting | Recommendation |
|---------|----------------|
| Min instances | 0-1 (cost) or 1+ (latency) |
| Max instances | Based on downstream capacity |
| Concurrency | 80-100 for typical web apps |
| CPU allocation | "Always on" for background tasks |
| Memory | Start at 512Mi, adjust based on metrics |

### New Features (2025)

- **GPU support** (NVIDIA L4): Serverless ML inference
- **Flexible CUDs**: Commitments apply across Cloud Run, GKE, Compute Engine
- **Multi-container support**: Sidecars for logging, proxies

### Traffic Management

```bash
# Blue-green deployment
gcloud run deploy my-service \
    --image=gcr.io/project/app:v2 \
    --no-traffic \
    --tag=green

# Gradual rollout
gcloud run services update-traffic my-service \
    --to-tags=green=10,latest=90
```

---

## IAM Best Practices (2025-2026)

### Identity Hierarchy

```
Organization
  └── Folders
      └── Projects
          └── Resources
              └── Service Accounts
```

### Workload Identity Federation (Preferred)

**Eliminates service account keys** for external workloads:

| Source | Integration |
|--------|-------------|
| AWS | AWS IAM roles |
| Azure | Azure AD |
| GitHub Actions | OIDC tokens |
| GitLab CI | OIDC tokens |
| On-premises | Active Directory, OIDC |

### Best Practices

1. **Avoid service account keys** - Use Workload Identity Federation
2. **Use predefined roles** - Avoid primitive roles (Owner, Editor, Viewer)
3. **Apply least privilege** - Grant minimum required permissions
4. **Create custom roles** - For specific, narrow permissions
5. **Use IAM Conditions** - Time-based, resource-based restrictions
6. **Enable audit logging** - Data access logs for sensitive APIs
7. **Regular access reviews** - Use IAM Recommender

### GKE Workload Identity

```yaml
# Kubernetes ServiceAccount with GCP binding
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-ksa
  annotations:
    iam.gke.io/gcp-service-account: my-gsa@project.iam.gserviceaccount.com
```

---

## Networking Best Practices (2025-2026)

### VPC Design

| Pattern | Use Case |
|---------|----------|
| **Single VPC** | Small projects, simple networking |
| **Shared VPC** | Multi-project, centralized network management |
| **Hub-and-Spoke** | Enterprise, multiple environments |

### Shared VPC Benefits

- Centralized network administration
- Consistent security policies
- Simplified IP address management
- Budget separation via service projects

### Private Service Connect

**Replaces VPC Peering for Google APIs:**

| Feature | Private Google Access | Private Service Connect |
|---------|----------------------|------------------------|
| IP addressing | Uses Google IPs | Your own internal IPs |
| Control | Limited | Granular endpoint control |
| Routing | Implicit | Explicit |

### IP Planning

| Resource | Recommended Range |
|----------|------------------|
| VPC | /16 (65,536 IPs) |
| Subnet | /20-/24 based on region |
| GKE Pods | /18-/20 (secondary range) |
| GKE Services | /24 (secondary range) |

### Security

1. **VPC Service Controls** - Data exfiltration prevention
2. **Cloud Armor** - DDoS protection, WAF rules
3. **Firewall policies** - Hierarchical, organization-wide
4. **VPC Flow Logs** - Network monitoring, troubleshooting

---

## Cost Optimization Strategies

### Resource-Level

| Strategy | Savings | Effort |
|----------|---------|--------|
| Spot/Preemptible VMs | 60-91% | Low |
| Committed Use Discounts (1yr) | 17% | Low |
| Committed Use Discounts (3yr) | 30%+ | Low |
| Right-sizing | 20-40% | Medium |
| Scheduling (stop dev VMs) | 50%+ | Medium |

### Service-Level

| Service | Optimization |
|---------|--------------|
| GKE | Autopilot, spot nodes, HPA/VPA |
| Cloud Run | Min instances=0, right-size memory |
| Cloud SQL | Right-size, stop dev instances |
| Cloud Storage | Lifecycle policies, appropriate class |
| BigQuery | Partitioning, clustering, slots |

### Monitoring

```bash
# Find idle resources
gcloud recommender recommendations list \
    --project=my-project \
    --location=us-central1-a \
    --recommender=google.compute.instance.IdleResourceRecommender
```

---

## Upcoming Changes (2026)

| Date | Change |
|------|--------|
| Jan 28, 2026 | Vertex AI Agent Engine: Sessions, Memory Bank, Code Execution start billing |
| Mar 17, 2026 | BigQuery Data Transfer: Additional IAM permissions required |

---

## Quick Reference

### Environment Setup

```bash
# Authentication
gcloud auth login
gcloud auth application-default login

# Configuration
gcloud config set project PROJECT_ID
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# Disable prompts (CI/CD)
export CLOUDSDK_CORE_DISABLE_PROMPTS=1
```

### Common Commands

```bash
# GKE
gcloud container clusters get-credentials CLUSTER --zone ZONE

# Cloud Run
gcloud run services list
gcloud run deploy SERVICE --image IMAGE --region REGION

# IAM
gcloud projects get-iam-policy PROJECT
gcloud iam service-accounts list
```

---

## Related Files

- [checklist.md](checklist.md) - Pre-deployment checklists
- [examples.md](examples.md) - CLI command reference
- [templates.md](templates.md) - Configuration templates
- [llm-prompts.md](llm-prompts.md) - AI automation prompts

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Run terraform plan, docker build, kubectl get commands | haiku | Mechanical CLI operations |
| Review Dockerfile for best practices | sonnet | Code review, security patterns |
| Debug pod crashes, container networking issues | sonnet | Diagnosis and error analysis |
| Design multi-region failover architecture | opus | Complex distributed systems decisions |
| Write Helm values for production rollout | sonnet | Configuration and templating |
| Create monitoring strategy for microservices | opus | System-wide observability design |
| Troubleshoot Kubernetes pod evictions under load | sonnet | Performance debugging and analysis |

---

## Sources

- [GKE Cost Optimization - CAST AI](https://cast.ai/blog/gke-cost-optimization/)
- [Cloud Run Pricing 2025 - Cloudchipr](https://cloudchipr.com/blog/cloud-run-pricing)
- [VPC Design Best Practices - Google Cloud](https://docs.cloud.google.com/architecture/best-practices-vpc-design)
- [Workload Identity Federation - Google Cloud](https://cloud.google.com/iam/docs/workload-identity-federation)
- [GKE Autopilot Overview - Google Cloud](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview)
- [Private Service Connect - Google Cloud](https://cloud.google.com/vpc/docs/private-service-connect)
- [Service Account Best Practices - Google Cloud](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts)

---

*GCP Skill v2.0 | Updated: 2026-01*
*Layer 3 Technical Skill*
