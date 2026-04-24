# GCP Architecture Basics

## Overview

Google Cloud Platform architecture fundamentals covering resource hierarchy, project organization, IAM, and billing management. Essential knowledge for building well-organized, secure, and cost-effective GCP environments.

## When to Use

- Setting up new GCP organizations or projects
- Designing resource hierarchy for enterprises
- Implementing IAM policies and access control
- Organizing billing and cost management
- Planning multi-environment deployments (dev/staging/prod)
- Establishing governance and security foundations

## Key Concepts

### GCP Resource Hierarchy

```
Organization (root)
    └── Folder (department/team)
        └── Project (workload boundary)
            └── Resources (VMs, buckets, etc.)
```

| Level | Purpose | IAM Inheritance |
|-------|---------|-----------------|
| Organization | Root node, company-wide policies | Policies flow down to all children |
| Folder | Group projects by team/env/app | Inherits org policies, adds own |
| Project | Billing boundary, API enablement | Inherits folder policies |
| Resource | Actual cloud services | Inherits project policies |

### IAM Core Principles

| Principle | Description |
|-----------|-------------|
| Least Privilege | Grant minimum permissions required |
| Role Hierarchy | Organization → Folder → Project → Resource |
| Predefined Roles | Use Google-managed roles over basic roles |
| Custom Roles | Create when predefined roles are too broad |
| Service Accounts | Use Workload Identity, avoid key files |

### Project Best Practices

| Practice | Rationale |
|----------|-----------|
| Separate environments | Dev/staging/prod in different projects |
| Consistent naming | Use standardized naming conventions |
| Labels everywhere | Enable cost tracking and organization |
| API enablement | Enable only required APIs per project |

### Billing Structure

| Component | Description |
|-----------|-------------|
| Billing Account | Pays for projects, single currency |
| Payments Profile | Links to payment method |
| Budgets | Alerts at spending thresholds |
| Cost Allocation | Labels, hierarchy-based reports |

## Architecture Framework Pillars

| Pillar | Focus Areas |
|--------|-------------|
| Operational Excellence | Monitoring, incident response, automation |
| Security | IAM, encryption, network security |
| Reliability | Availability, disaster recovery, capacity |
| Performance | Scaling, optimization, caching |
| Cost Optimization | Committed use, rightsizing, preemptible VMs |

## Related Methodologies

| Methodology | Focus |
|-------------|-------|
| [gcp-arch-patterns](../gcp-arch-patterns/) | Architecture patterns |
| [gcp-networking](../gcp-networking/) | VPC, subnets, firewall |
| [gcp-compute](../gcp-compute/) | VMs, autoscaling |
| [terraform](../terraform/) | Infrastructure as Code |


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| GCP resource hierarchy design | sonnet | Organization planning |
| Project-folder-org structure | sonnet | Governance architecture |
| Billing account setup | haiku | Administrative task |

## Sources

- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
- [GCP Resource Hierarchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy)
- [IAM Best Practices](https://cloud.google.com/iam/docs/best-practices)
- [Billing Best Practices](https://cloud.google.com/billing/docs/onboarding-checklist)
- [Landing Zone Design](https://cloud.google.com/architecture/landing-zones/decide-resource-hierarchy)

---

*GCP Architecture Basics | faion-infrastructure-engineer*
