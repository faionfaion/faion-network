# AWS Architecture Foundations

Core AWS architectural patterns, Well-Architected Framework, multi-account strategy, VPC design, IAM, security foundations, and monitoring for production-grade infrastructure.

## Well-Architected Framework (6 Pillars)

| Pillar | Focus | Key Practices |
|--------|-------|---------------|
| Operational Excellence | Automation, monitoring, improvement | IaC, runbooks, observability |
| Security | IAM, encryption, network security | Zero trust, least privilege, MFA |
| Reliability | Fault tolerance, recovery, scaling | Multi-AZ, cell-based architecture |
| Performance Efficiency | Right-sizing, caching, serverless | Compute optimization, monitoring |
| Cost Optimization | Reserved capacity, spot instances | Savings Plans, right-sizing |
| Sustainability | Resource efficiency, managed services | Energy efficiency, carbon footprint |

## Multi-Account Strategy

### Recommended OU Structure

```
Root
├── Security OU
│   ├── Log Archive Account
│   ├── Security Tooling Account
│   └── Security Read-Only Account
├── Infrastructure OU
│   ├── Network Account (Transit Gateway, VPC)
│   ├── Shared Services Account
│   └── Identity Account (IAM Identity Center)
├── Sandbox OU
│   └── Developer Sandbox Accounts
├── Workloads OU
│   ├── Production OU
│   │   ├── Prod Account 1
│   │   └── Prod Account 2
│   └── Non-Production OU
│       ├── Dev Account
│       ├── Staging Account
│       └── Test Account
├── Policy Staging OU
│   └── SCP Test Accounts
└── Suspended OU
    └── Decommissioned Accounts
```

### Design Principles

| Principle | Description |
|-----------|-------------|
| Account per workload | Isolate blast radius, quotas, billing |
| Environment separation | Prod/staging/dev in separate accounts |
| Security controls at OU level | Apply SCPs to OUs, not accounts |
| Shallow OU hierarchy | Max 3-4 levels recommended |
| No workloads in management account | Keep management account clean |

## Landing Zone Components

### AWS Control Tower (v4.0+)

- Pre-packaged multi-account setup
- Account Factory for provisioning
- Guardrails (preventive + detective)
- Centralized logging and monitoring
- IAM Identity Center integration

### Landing Zone Accelerator (LZA)

- Extends Control Tower capabilities
- 35+ AWS services integration
- Compliance frameworks support
- IaC-based customization
- GitOps-driven governance

## Core Services by Category

| Category | Services |
|----------|----------|
| Compute | EC2, ECS, EKS, Lambda, Fargate |
| Storage | S3, EBS, EFS, FSx |
| Database | RDS, Aurora, DynamoDB, ElastiCache |
| Networking | VPC, ALB/NLB, CloudFront, Route 53, Transit Gateway |
| Security | IAM, KMS, Secrets Manager, WAF, Security Hub |
| Monitoring | CloudWatch, X-Ray, CloudTrail, Config |
| Governance | Organizations, Control Tower, Service Catalog |

## VPC Architecture

### Three-Tier Design

| Tier | Subnets | Purpose | Resources |
|------|---------|---------|-----------|
| Public | /24 per AZ | Internet-facing | ALB, NAT GW, Bastion |
| Private | /24 per AZ | Application workloads | ECS, EKS, EC2 |
| Database | /24 per AZ | Data layer | RDS, ElastiCache |

### Multi-AZ Best Practices

- Minimum 3 AZs for production
- One NAT Gateway per AZ in production
- Single NAT Gateway for dev/staging (cost optimization)
- VPC Flow Logs enabled for security auditing
- DNS hostnames and support enabled

## Security Foundations

### Identity and Access

| Practice | Implementation |
|----------|----------------|
| Federated access | IAM Identity Center + IdP |
| Least privilege | Scoped policies, no `*` resources |
| MFA everywhere | All users, root accounts |
| No root access | Enable root access management |
| Roles over keys | IRSA for EKS, instance profiles |

### Network Security

| Control | Purpose |
|---------|---------|
| Private subnets | Workloads not internet-exposed |
| Security groups | Instance-level firewall |
| NACLs | Subnet-level protection |
| VPC Flow Logs | Traffic auditing |
| PrivateLink | Private AWS service access |
| WAF | Application-layer protection |

### Encryption

| Data State | Solution |
|------------|----------|
| At rest | KMS (EBS, S3, RDS encryption) |
| In transit | TLS 1.2+, ACM certificates |
| Secrets | Secrets Manager, rotation |
| Keys | Customer-managed KMS keys |

## Cost Optimization

### Compute Savings

| Option | Savings | Use Case |
|--------|---------|----------|
| Reserved Instances | 72% | Predictable baseline |
| Savings Plans | 66% | Flexible commitment |
| Spot Instances | 90% | Fault-tolerant workloads |
| Right-sizing | 20-40% | Match instance to usage |

### Storage Optimization

- S3 Intelligent Tiering for variable access
- Lifecycle policies for archival
- Delete unused EBS snapshots
- Glacier Deep Archive for compliance

### Network Optimization

- CloudFront for reduced data transfer
- VPC Endpoints to avoid NAT costs
- Consolidated NAT in dev environments

## Monitoring and Observability

### Core Services

| Service | Purpose |
|---------|---------|
| CloudWatch | Metrics, logs, dashboards, alarms |
| X-Ray | Distributed tracing |
| CloudTrail | API auditing (organization-wide) |
| Config | Resource configuration tracking |
| Security Hub | Security posture dashboard |

### Key Metrics

- EKS: Pod CPU/memory utilization
- RDS: CPU, connections, IOPS
- ALB: Request count, latency, 5xx errors
- Lambda: Invocations, duration, errors

## Related Methodologies

| Methodology | Focus |
|-------------|-------|
| [aws-networking/](../aws-networking/) | VPC, subnets, Transit Gateway |
| [aws-ec2-ecs/](../aws-ec2-ecs/) | Compute services |
| [aws-lambda/](../aws-lambda/) | Serverless functions |
| [aws-s3-storage/](../aws-s3-storage/) | Storage patterns |
| [terraform/](../terraform/) | IaC for AWS |

## Sources

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Well-Architected Framework Docs](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [Multi-Account Strategy Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html)
- [AWS Organizations Best Practices](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices.html)
- [AWS Control Tower Landing Zone](https://docs.aws.amazon.com/prescriptive-guidance/latest/designing-control-tower-landing-zone/introduction.html)
- [Landing Zone Accelerator](https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/solution-overview.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
