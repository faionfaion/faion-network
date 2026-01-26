# AWS Skills

> **Entry point:** `/faion-net` -- invoke for automatic routing.

AWS infrastructure and cloud operations skill for the faion-devops-engineer domain.

## Overview

Comprehensive AWS CLI operations and cloud infrastructure management covering compute, storage, serverless, containers, databases, infrastructure as code, identity management, and monitoring.

## Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and navigation |
| [checklist.md](checklist.md) | Well-Architected Framework checklists |
| [examples.md](examples.md) | AWS CLI command examples |
| [templates.md](templates.md) | CloudFormation/Terraform templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for AWS tasks |

## AWS Well-Architected Framework (2025-2026)

The framework provides architectural best practices across six pillars:

| Pillar | Focus |
|--------|-------|
| Operational Excellence | Automate changes, respond to events, define standards |
| Security | Protect data, systems, assets through risk assessments |
| Reliability | Recover from failures, meet demand, mitigate disruptions |
| Performance Efficiency | Use resources efficiently, maintain efficiency as demand changes |
| Cost Optimization | Avoid unnecessary costs, understand spending |
| Sustainability | Minimize environmental impact of running workloads |

### Key Design Principles

1. **Stop guessing capacity** -- Use cloud to provision exact resources needed
2. **Test at production scale** -- Run realistic load tests
3. **Automate experimentation** -- Use IaC to deploy/test/iterate quickly
4. **Allow evolutionary architectures** -- Design with loosely coupled components
5. **Drive architectures using data** -- Use monitoring and metrics for decisions

## Service Categories

| Category | Services |
|----------|----------|
| Compute | EC2, Lambda, ECS, EKS, Fargate |
| Storage | S3, EBS, EFS, Glacier |
| Database | RDS, Aurora, DynamoDB, ElastiCache |
| Networking | VPC, Route 53, CloudFront, ALB/NLB |
| Security | IAM, KMS, Secrets Manager, Security Hub |
| Monitoring | CloudWatch, CloudTrail, X-Ray |
| IaC | CloudFormation, CDK |

## Cost Optimization Strategies (2025)

| Strategy | Savings |
|----------|---------|
| Reserved Instances / Savings Plans | Up to 72% |
| Spot Instances | Up to 90% |
| Graviton Instances | Up to 40% better price-performance |
| Right-sizing | 10-30% typical |
| Auto Scaling | Variable based on usage patterns |

### AWS Cost Tools

| Tool | Purpose |
|------|---------|
| Cost Explorer | Visualize and analyze costs |
| Compute Optimizer | Right-sizing recommendations |
| Trusted Advisor | Find unused resources |
| Budgets | Set spending alerts |
| Savings Plans | Commit to usage for discounts |

## Security Best Practices (2025-2026)

### IAM Security

| Practice | Priority |
|----------|----------|
| Use federation with IdP | Critical |
| Use temporary credentials (IAM roles) | Critical |
| Require MFA | Critical |
| Apply least-privilege permissions | Critical |
| Rotate access keys regularly | High |
| Protect root user credentials | Critical |

### Core Security Measures

| Measure | Implementation |
|---------|----------------|
| Encryption at rest | S3, EBS, RDS, DynamoDB via KMS |
| Encryption in transit | TLS 1.2+, HTTPS everywhere |
| Logging | CloudTrail, VPC Flow Logs, S3 access logs |
| Monitoring | Security Hub, GuardDuty, Inspector |
| Secrets management | Secrets Manager, Parameter Store |

### Shared Responsibility Model

| AWS Responsibility | Customer Responsibility |
|-------------------|------------------------|
| Physical security | IAM configuration |
| Hardware maintenance | Security groups |
| Network infrastructure | Data encryption |
| Hypervisor security | Application security |

## Quick Start

```bash
# Configure AWS CLI
aws configure

# Verify identity
aws sts get-caller-identity

# Check region
aws configure get region
```

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-infrastructure-engineer](../../faion-infrastructure-engineer/CLAUDE.md) | Terraform, Kubernetes integration |
| [faion-cicd-engineer](../../faion-cicd-engineer/CLAUDE.md) | CI/CD pipelines |
| [faion-software-architect](../../faion-software-architect/CLAUDE.md) | Architecture decisions |

## Sources

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Well-Architected Documentation](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS Cost Optimization](https://aws.amazon.com/aws-cost-management/cost-optimization/)
- [AWS Security Best Practices](https://docs.aws.amazon.com/whitepapers/latest/aws-security-best-practices/welcome.html)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
