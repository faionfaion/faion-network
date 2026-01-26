# GCP Architecture Patterns

**Layer:** 3 (Technical Skill)
**Used by:** faion-devops-engineer, faion-infrastructure-engineer

## Purpose

Google Cloud Architecture Framework implementation covering landing zones, resource hierarchy, network design, and production-ready patterns for GKE, Cloud SQL, and Cloud Storage with CDN. Updated with 2025-2026 best practices.

---

## Quick Navigation

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and architecture guidance |
| [checklist.md](checklist.md) | Landing zone and architecture checklists |
| [examples.md](examples.md) | Terraform and gcloud examples |
| [templates.md](templates.md) | Landing zone and infrastructure templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for architecture tasks |

---

## Google Cloud Architecture Framework

The Well-Architected Framework provides best practices across five pillars:

| Pillar | Focus | Key Recommendations |
|--------|-------|---------------------|
| **Operational Excellence** | Deploy, operate, monitor workloads | Automate changes, manage incidents, continuous improvement |
| **Security, Privacy, Compliance** | Protect data and meet regulations | Zero trust, shift-left security, AI security, compliance |
| **Reliability** | Resilient, highly available systems | Redundancy, horizontal scaling, graceful degradation |
| **Cost Optimization** | Maximize business value | Align spending, foster cost awareness, optimize resources |
| **Performance Optimization** | Optimal resource performance | Strategic allocation, elasticity, modular design |

### Five Core Design Principles

1. **Design for Change** - Build systems enabling regular, small deployments with rapid feedback
2. **Document Architecture** - Maintain clear, useful documentation as systems evolve
3. **Simplify Design** - Use fully managed services to minimize complexity
4. **Decouple Architecture** - Separate components for independent operation and scaling
5. **Stateless Architecture** - Improve reliability and scalability through shared storage

---

## Landing Zone Design

A landing zone (cloud foundation) is a modular configuration enabling enterprise adoption of Google Cloud.

### Core Elements

| Element | Purpose |
|---------|---------|
| **Identity Provisioning** | User access, authentication, federation |
| **Resource Hierarchy** | Organization, folders, projects structure |
| **Network Architecture** | VPC design, connectivity, traffic management |
| **Security Controls** | Policies, compliance, encryption, logging |

### Additional Components

| Component | Purpose |
|-----------|---------|
| Monitoring & Logging | Cloud Monitoring, Logging, audit trails |
| Backup & DR | Data protection, cross-region replication |
| Cost Management | Budgets, billing alerts, FinOps |
| API Management | API governance, security |
| Cluster Management | GKE best practices |

### Resource Hierarchy

```
Organization
  |
  +-- Folders (by department, environment, or both)
  |     |
  |     +-- Production/
  |     |     +-- Project: prod-frontend
  |     |     +-- Project: prod-backend
  |     |     +-- Project: prod-data
  |     |
  |     +-- Staging/
  |     |     +-- Project: staging-app
  |     |
  |     +-- Development/
  |           +-- Project: dev-sandbox-team-a
  |
  +-- Shared Infrastructure/
        +-- Project: shared-vpc-host
        +-- Project: shared-monitoring
        +-- Project: shared-security
```

### Network Patterns

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| **Single VPC** | Small projects, simple networking | Low |
| **Shared VPC** | Multi-project, centralized network admin | Medium |
| **Hub-and-Spoke** | Enterprise, multiple environments | High |

---

## GKE Architecture Patterns

### Mode Selection

| Mode | When to Use | Cost Model |
|------|-------------|------------|
| **Autopilot** (recommended) | Most workloads, simplified ops | Pay-per-pod |
| **Standard** | GPU, custom configs, privileged containers | Per-cluster + nodes |
| **Hybrid** (2025) | Standard with Autopilot workloads | Mixed |

### Node Pool Strategies

| Pattern | Use Case | Node Type |
|---------|----------|-----------|
| General pool | Stateless apps, always-on services | Standard instances |
| Spot pool | Batch jobs, fault-tolerant workloads | Spot (70-90% savings) |
| GPU pool | ML inference, video processing | GPU-attached nodes |
| High-memory pool | Caching, in-memory databases | Memory-optimized |

### Cluster Topology

| Topology | Zones | HA Level | Use Case |
|----------|-------|----------|----------|
| Zonal | 1 | Low | Development, testing |
| Regional | 3 | High | Production |
| Multi-cluster | Multiple regions | Highest | Global, disaster recovery |

---

## Cloud SQL Architecture

### Availability Configurations

| Environment | Configuration | RPO | RTO |
|-------------|---------------|-----|-----|
| Development | ZONAL, no replica | Hours | Minutes |
| Staging | REGIONAL, no replica | Seconds | Minutes |
| Production | REGIONAL + read replica | 0 | Seconds |

### Sizing Guidelines

| Workload | Instance Tier | Storage Type |
|----------|---------------|--------------|
| Light (< 100 connections) | db-f1-micro to db-g1-small | pd-standard |
| Medium (100-500 connections) | db-custom-2-7680 | pd-ssd |
| Heavy (> 500 connections) | db-custom-4-16384+ | pd-ssd |

---

## Cloud Storage + CDN

### Storage Classes

| Class | Use Case | Min Duration | Cost |
|-------|----------|--------------|------|
| STANDARD | Frequently accessed | None | $$$ |
| NEARLINE | < 1/month access | 30 days | $$ |
| COLDLINE | < 1/quarter access | 90 days | $ |
| ARCHIVE | < 1/year access | 365 days | Lowest |

### CDN Configuration

| Setting | Recommendation |
|---------|----------------|
| Cache mode | CACHE_ALL_STATIC for static content |
| Default TTL | 3600 seconds (1 hour) |
| Max TTL | 86400 seconds (1 day) |
| Negative caching | Enabled for error pages |
| Serve while stale | Enabled for high availability |

---

## IP Address Planning

| Resource | Recommended Range | Notes |
|----------|------------------|-------|
| VPC | /16 | 65,536 IPs per VPC |
| Subnet | /20 to /24 | Based on region and workload |
| GKE Pods | /18 to /20 | Secondary range |
| GKE Services | /24 | Secondary range |
| Master CIDR | /28 | Private cluster control plane |

### Example IP Plan (Multi-Environment)

| Environment | VPC CIDR | Subnet | Pods | Services |
|-------------|----------|--------|------|----------|
| Production | 10.0.0.0/16 | 10.0.0.0/20 | 10.0.16.0/14 | 10.0.32.0/20 |
| Staging | 10.1.0.0/16 | 10.1.0.0/20 | 10.1.16.0/14 | 10.1.32.0/20 |
| Development | 10.2.0.0/16 | 10.2.0.0/20 | 10.2.16.0/14 | 10.2.32.0/20 |

---

## Security Architecture

### Identity and Access

| Best Practice | Implementation |
|---------------|----------------|
| Workload Identity | Replace SA keys with WIF |
| Least privilege | Use predefined roles, avoid primitive |
| IAM Conditions | Time-based, resource-based restrictions |
| Audit logging | Enable data access logs |
| Regular reviews | Use IAM Recommender |

### Network Security

| Control | Purpose |
|---------|---------|
| Private clusters | No public node IPs |
| VPC Service Controls | Data exfiltration prevention |
| Cloud Armor | DDoS, WAF protection |
| Hierarchical firewall | Organization-wide policies |
| VPC Flow Logs | Network monitoring |

### Data Security

| Layer | Implementation |
|-------|----------------|
| At rest | Default encryption, CMEK for compliance |
| In transit | TLS 1.2+, Private Service Connect |
| In use | Confidential Computing (sensitive workloads) |

---

## Cost Optimization Patterns

### Compute Savings

| Strategy | Savings | Effort |
|----------|---------|--------|
| Spot/Preemptible VMs | 60-91% | Low |
| Committed Use (1yr) | 17% | Low |
| Committed Use (3yr) | 30%+ | Low |
| Right-sizing | 20-40% | Medium |
| Scheduling (stop dev) | 50%+ | Medium |

### Service-Specific

| Service | Optimization |
|---------|--------------|
| GKE | Autopilot, spot nodes, HPA/VPA |
| Cloud Run | min=0, right-size memory, CUDs |
| Cloud SQL | Right-size, stop dev instances |
| Cloud Storage | Lifecycle policies, autoclass |

---

## Related Files

- [checklist.md](checklist.md) - Landing zone and architecture checklists
- [examples.md](examples.md) - Terraform and gcloud examples
- [templates.md](templates.md) - Reusable infrastructure templates
- [llm-prompts.md](llm-prompts.md) - AI automation prompts

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [gcp](../gcp/README.md) | GCP services reference |
| [terraform](../terraform/README.md) | Infrastructure as Code |
| [kubernetes](../kubernetes/README.md) | Container orchestration |

---

## Sources

- [Google Cloud Architecture Framework](https://docs.cloud.google.com/architecture/framework)
- [Landing Zone Design](https://docs.cloud.google.com/architecture/landing-zones)
- [GKE Best Practices](https://docs.cloud.google.com/kubernetes-engine/docs/best-practices)
- [Cloud SQL High Availability](https://cloud.google.com/sql/docs/postgres/high-availability)
- [Cloud CDN Best Practices](https://cloud.google.com/cdn/docs/best-practices)
- [VPC Design Best Practices](https://docs.cloud.google.com/architecture/best-practices-vpc-design)

---

*GCP Architecture Patterns v2.0 | Updated: 2026-01*
*Layer 3 Technical Skill*
