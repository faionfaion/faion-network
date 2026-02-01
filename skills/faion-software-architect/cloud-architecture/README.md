# Cloud Architecture

Best practices for designing, deploying, and operating cloud-native applications and infrastructure.

## Overview

Cloud architecture encompasses the design and implementation of applications, services, and infrastructure in cloud environments. Modern cloud architecture emphasizes scalability, reliability, security, cost optimization, and sustainability.

### Key Principles

| Principle | Description |
|-----------|-------------|
| **Design for failure** | Assume components will fail; build redundancy and recovery mechanisms |
| **Decouple components** | Use loose coupling, async communication, and event-driven patterns |
| **Implement elasticity** | Scale resources up and down based on demand |
| **Think parallel** | Prefer horizontal over vertical scaling |
| **Keep data close** | Minimize latency by co-locating compute and data |
| **Automate everything** | Use IaC, CI/CD, and policy-as-code |
| **Secure by design** | Implement zero trust, least privilege, and defense in depth |

## Well-Architected Framework

The Well-Architected Framework provides a consistent approach for evaluating architectures across six pillars.

### The Six Pillars

| Pillar | Focus | Key Questions |
|--------|-------|---------------|
| **Operational Excellence** | Run and monitor systems, continuously improve | How do you manage and automate changes? How do you respond to events? |
| **Security** | Protect data, systems, and assets | How do you manage identities? How do you detect security events? |
| **Reliability** | Recover from failures, meet demand | How do you handle change management? How do you design for fault tolerance? |
| **Performance Efficiency** | Use resources efficiently | How do you select appropriate resources? How do you monitor performance? |
| **Cost Optimization** | Avoid unnecessary costs | How do you govern usage? How do you optimize over time? |
| **Sustainability** | Minimize environmental impact | How do you maximize utilization? How do you reduce downstream impact? |

### General Design Principles

- **Stop guessing capacity** - Use cloud elasticity to provision exact resources needed
- **Test at production scale** - Run realistic load tests without upfront investment
- **Automate architectural experimentation** - Use IaC to deploy, test, and iterate quickly
- **Allow evolutionary architectures** - Design loosely coupled components that adapt to change
- **Drive architectures using data** - Use metrics and monitoring to inform decisions
- **Improve through game days** - Simulate production events to test resilience

## Cloud Provider Comparison

### Market Overview (2025-2026)

| Provider | Market Share | Primary Strengths |
|----------|--------------|-------------------|
| **AWS** | ~31% | Largest service catalog, global reach, mature ecosystem |
| **Azure** | ~25% | Microsoft integration, enterprise focus, hybrid cloud |
| **GCP** | ~11% | AI/ML leadership, Kubernetes expertise, data analytics |

### Provider Selection Matrix

| Criterion | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| **Service breadth** | Largest | Large | Growing |
| **Enterprise integration** | Good | Excellent (Microsoft) | Good |
| **AI/ML capabilities** | SageMaker, Bedrock | Azure AI, OpenAI | Vertex AI, TPUs |
| **Kubernetes** | EKS | AKS | GKE (most mature) |
| **Data analytics** | Redshift, Athena | Synapse, Fabric | BigQuery |
| **Global network** | Extensive | Extensive | Premium tier |
| **Sustainability** | 100% renewable by 2025 | Carbon negative by 2030 | 90%+ carbon-free |
| **Pricing model** | Complex, flexible | Microsoft discounts | Sustained use discounts |
| **Learning curve** | Steeper | Moderate | Moderate |

### When to Choose Each Provider

**Choose AWS when:**
- Need broadest service selection
- Building multi-region global applications
- Require mature, battle-tested services
- Government/regulated workloads (GovCloud)

**Choose Azure when:**
- Heavy Microsoft ecosystem (AD, Office 365, Windows)
- Enterprise hybrid cloud requirements
- Strong .NET development team
- European data sovereignty requirements

**Choose GCP when:**
- AI/ML is core to product
- Big data and analytics focus
- Kubernetes-first strategy
- Cost-effective data egress needed

## Multi-Cloud Strategy

### Why Multi-Cloud?

| Benefit | Description |
|---------|-------------|
| **Avoid vendor lock-in** | Reduce dependency on single provider |
| **Best-of-breed** | Use each provider's strengths |
| **Regulatory compliance** | Meet data sovereignty requirements |
| **Disaster recovery** | Cross-provider redundancy |
| **Cost optimization** | Leverage competitive pricing |
| **Geographic reach** | Access regions not available in single provider |

### Multi-Cloud Challenges

| Challenge | Mitigation |
|-----------|------------|
| **Complexity** | Use abstraction layers (Kubernetes, Terraform) |
| **Skills gap** | Train teams or specialize by provider |
| **Data gravity** | Architect for data locality from start |
| **Networking** | Use dedicated interconnects, mesh patterns |
| **Security** | Unified IAM, policy-as-code |
| **Cost tracking** | Implement FinOps practices |

### Multi-Cloud Patterns

| Pattern | Use Case | Implementation |
|---------|----------|----------------|
| **Workload distribution** | Different workloads on different clouds | API Gateway + routing |
| **Disaster recovery** | Primary on one, DR on another | Async replication |
| **Data residency** | EU data on Azure, US on AWS | Regional routing |
| **Cost arbitrage** | Spot instances across providers | Workload orchestration |
| **Feature leverage** | GCP for ML, AWS for compute | Service mesh integration |

## Landing Zones

A landing zone is a well-architected, scalable, and secure cloud foundation that provides a baseline for your organization's cloud adoption.

### Landing Zone Components

| Component | Description |
|-----------|-------------|
| **Identity & Access** | Centralized IAM, federation, MFA, SSO |
| **Network topology** | Hub-and-spoke or mesh VPC design |
| **Security controls** | Guardrails, policies, compliance automation |
| **Logging & monitoring** | Centralized logs, SIEM integration |
| **Cost management** | Budgets, alerts, tagging policies |
| **Resource organization** | Account/subscription/project structure |
| **Automation** | IaC templates, CI/CD pipelines |
| **Governance** | Policies, standards, approval workflows |

### Provider Landing Zone Solutions

| Provider | Solution | Features |
|----------|----------|----------|
| **AWS** | Control Tower | Multi-account, guardrails, Account Factory |
| **Azure** | Cloud Adoption Framework | Enterprise-scale, landing zones, blueprints |
| **GCP** | Cloud Foundation Toolkit | Organization, folders, security blueprint |

### Landing Zone for AI/ML Workloads

Modern landing zones must accommodate AI workloads:

- **GPU instances** - Provision GPU-optimized VMs (AWS P5, Azure NDv5, GCP A3)
- **High-throughput storage** - Low-latency access for large datasets
- **Data pipelines** - Versioning, lineage, governance frameworks
- **Private endpoints** - Ensure data never traverses public internet
- **Cost controls** - ML workloads can be expensive; implement budgets

## Network Architecture

### VPC Design Principles

| Principle | Description |
|-----------|-------------|
| **Use custom mode** | Better integration with existing IP schemes |
| **Plan IP addressing** | Prevent overlaps, allow for growth |
| **Separate environments** | Distinct VPCs for dev/staging/prod |
| **Public/private separation** | Isolate backend from internet-facing |
| **Use IaC** | Define networking as code |
| **Enable flow logs** | Monitor traffic for security |

### VPC Architecture Patterns

**Hub-and-Spoke:**
```
                    ┌─────────────┐
                    │   Hub VPC   │
                    │ (Transit GW)│
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐
    │  Prod VPC   │ │ Staging VPC │ │   Dev VPC   │
    └─────────────┘ └─────────────┘ └─────────────┘
```

**Shared VPC (GCP) / VPC Sharing:**
```
    ┌─────────────────────────────────┐
    │         Host Project            │
    │       (Shared VPC)              │
    └──────────────┬──────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───┴───┐    ┌─────┴────┐   ┌─────┴────┐
│Service│    │ Service  │   │ Service  │
│Project│    │ Project  │   │ Project  │
└───────┘    └──────────┘   └──────────┘
```

### Subnet Design

| Subnet Type | Purpose | Example CIDR |
|-------------|---------|--------------|
| **Public** | Load balancers, bastion hosts, NAT | 10.0.1.0/24 |
| **Private (App)** | Application servers, containers | 10.0.2.0/24 |
| **Private (Data)** | Databases, caches | 10.0.3.0/24 |
| **Private (Internal)** | Internal services | 10.0.4.0/24 |

### Multi-Region Design

```
                    Global Load Balancer
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
      ┌────────┐      ┌────────┐      ┌────────┐
      │Region A│      │Region B│      │Region C│
      │(Primary)      │(Secondary)    │(Secondary)
      └────┬───┘      └────┬───┘      └────┬───┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                    Database Replication
```

**Strategies:**
- **Active-Passive** - One primary, others standby (lower cost)
- **Active-Active** - All serve traffic, sync data (higher availability)

## Security Architecture

### Zero Trust Principles

| Principle | Implementation |
|-----------|----------------|
| **Never trust, always verify** | Authenticate every request |
| **Least privilege** | Minimal permissions, JIT access |
| **Assume breach** | Limit blast radius, detect anomalies |
| **Explicit verification** | MFA, device posture, location |
| **Microsegmentation** | Network isolation between workloads |

### Security Layers

| Layer | Controls |
|-------|----------|
| **Identity** | MFA, SSO, PAM, RBAC, JIT access |
| **Network** | VPC, security groups, WAF, DDoS protection |
| **Data** | Encryption at rest/transit, key management |
| **Application** | SAST/DAST, dependency scanning, secrets management |
| **Infrastructure** | Hardened images, patch management, CIS benchmarks |
| **Monitoring** | SIEM, threat detection, audit logs |

### Security Group Design

```
Internet → ALB (443) → App (8080) → DB (5432)
            │            │            │
          sg-web       sg-app       sg-db
          (public)     (private)    (private)
```

## Cost Optimization (FinOps)

### FinOps Framework

FinOps operates through three phases:

| Phase | Activities |
|-------|------------|
| **Inform** | Cost visibility, allocation, tagging, showback/chargeback |
| **Optimize** | Right-sizing, reserved instances, spot, waste elimination |
| **Operate** | Governance, automation, continuous improvement |

### Cost Optimization Strategies

| Strategy | Savings | Best For |
|----------|---------|----------|
| **Right-sizing** | 20-40% | Over-provisioned resources |
| **Reserved Instances** | 30-70% | Predictable, steady workloads |
| **Spot/Preemptible** | 60-90% | Fault-tolerant, batch jobs |
| **Savings Plans** | 20-40% | Flexible commitment discounts |
| **Auto-scaling** | Variable | Variable workloads |
| **Scheduling** | Up to 75% | Non-production environments |
| **Storage tiering** | 50-80% | Infrequently accessed data |

### Tagging Strategy

| Tag Key | Purpose | Example |
|---------|---------|---------|
| `Environment` | Identify environment | prod, staging, dev |
| `Team` | Cost allocation | platform, data, ml |
| `Project` | Track by project | user-auth, payments |
| `CostCenter` | Financial tracking | CC-12345 |
| `Owner` | Accountability | team@company.com |
| `Lifecycle` | Resource management | temporary, permanent |

## Common Patterns

### Three-Tier Architecture

```
┌─────────────────────────────────────────┐
│            Presentation Tier            │
│         (Load Balancer + CDN)           │
├─────────────────────────────────────────┤
│            Application Tier             │
│         (Auto-scaling Group)            │
├─────────────────────────────────────────┤
│              Data Tier                  │
│     (Database + Cache + Storage)        │
└─────────────────────────────────────────┘
```

### Serverless Architecture

```
API Gateway → Lambda → DynamoDB
                │
                ▼
           S3 (files)
```

### Microservices on Kubernetes

```
┌─────────────────────────────────────────┐
│            Kubernetes Cluster           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │Service A│  │Service B│  │Service C│ │
│  └────┬────┘  └────┬────┘  └────┬────┘ │
│       │            │            │      │
│  ┌────┴────────────┴────────────┴────┐ │
│  │       Service Mesh (Istio)        │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Disaster Recovery

| Strategy | RTO | RPO | Cost | Use Case |
|----------|-----|-----|------|----------|
| **Backup & Restore** | Hours | Hours | Low | Non-critical workloads |
| **Pilot Light** | Minutes | Minutes | Medium | Core systems ready |
| **Warm Standby** | Seconds | Seconds | High | Critical applications |
| **Active-Active** | Zero | Zero | Highest | Mission-critical |

**RTO:** Recovery Time Objective (acceptable downtime)
**RPO:** Recovery Point Objective (acceptable data loss)

## Storage Options

| Service | Use Case | Providers |
|---------|----------|-----------|
| Object storage | Files, backups, static assets | S3, Cloud Storage, Blob |
| Block storage | VM disks, databases | EBS, Persistent Disk, Managed Disk |
| File storage | Shared file systems | EFS, Filestore, Azure Files |
| Relational DB | Structured data, ACID | RDS, Cloud SQL, Azure SQL |
| NoSQL | Flexible schema, scale | DynamoDB, Firestore, Cosmos DB |
| Cache | Low-latency access | ElastiCache, Memorystore, Redis Cache |
| Data warehouse | Analytics, BI | Redshift, BigQuery, Synapse |

## LLM Usage Tips

### When Working with LLMs

1. **Provide context** - Share existing infrastructure, constraints, and requirements
2. **Be specific about providers** - Name specific services (e.g., "AWS Lambda" not "serverless")
3. **Include scale requirements** - RPS, data volume, growth projections
4. **Mention compliance** - GDPR, HIPAA, SOC2, PCI-DSS requirements
5. **Request alternatives** - Ask for trade-offs between options
6. **Validate output** - LLMs may not know latest service features

### Prompt Patterns for Cloud Architecture

- "Design a {workload type} architecture for {scale} using {provider}"
- "Compare {option A} vs {option B} for {use case} considering {constraints}"
- "Review this Terraform for {security|cost|reliability} issues"
- "Create a migration plan from {source} to {target}"
- "Optimize this architecture for {cost|performance|reliability}"

## External References

### AWS
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [AWS Control Tower](https://aws.amazon.com/controltower/)

### Azure
- [Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/)
- [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/)
- [Cloud Adoption Framework](https://learn.microsoft.com/azure/cloud-adoption-framework/)

### GCP
- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
- [Cloud Architecture Center](https://cloud.google.com/architecture)
- [Landing Zone Design](https://cloud.google.com/architecture/landing-zones)

### FinOps
- [FinOps Foundation](https://www.finops.org/)
- [FOCUS Specification](https://focus.finops.org/)

### Security
- [NIST SP 800-207 Zero Trust](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [Cloud Security Alliance](https://cloudsecurityalliance.org/)


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related

- [serverless-architecture/](../serverless-architecture/) - Serverless patterns
- [reliability-architecture/](../reliability-architecture/) - Reliability design
- [security-architecture/](../security-architecture/) - Security patterns
- [observability-architecture/](../observability-architecture/) - Monitoring and observability
