---
id: aws-architecture
name: "AWS Architecture"
domain: OPS
skill: faion-devops-engineer
category: "devops"
version: "2.0.0"
updated: "2026-01"
---

# AWS Architecture

## Overview

AWS (Amazon Web Services) provides comprehensive cloud infrastructure services. This methodology covers architectural patterns, service selection, and best practices for building production-grade applications on AWS following the Well-Architected Framework.

## When to Use

- Building new cloud-native applications
- Migrating on-premises workloads to cloud
- Designing scalable microservices architectures
- Implementing disaster recovery solutions
- Optimizing existing AWS infrastructure
- Building serverless applications
- Designing multi-tier web applications

## Key Concepts

### AWS Well-Architected Framework (6 Pillars)

| Pillar | Focus Areas | Key Practices |
|--------|-------------|---------------|
| Operational Excellence | Automation, monitoring, continuous improvement | IaC, runbooks, observability |
| Security | IAM, encryption, network security, compliance | Least privilege, encryption at rest/transit |
| Reliability | Fault tolerance, recovery, scaling | Multi-AZ, auto-scaling, chaos engineering |
| Performance Efficiency | Right-sizing, caching, serverless | Graviton, caching layers, CDN |
| Cost Optimization | Reserved capacity, spot instances, rightsizing | Savings plans, cost allocation tags |
| Sustainability | Resource efficiency, managed services | Efficient regions, managed services |

### Core Services by Category

| Category | Services | Use Case |
|----------|----------|----------|
| Compute | EC2, ECS, EKS, Lambda, Fargate | Workload processing |
| Storage | S3, EBS, EFS, FSx | Data persistence |
| Database | RDS, Aurora, DynamoDB, ElastiCache | Structured/unstructured data |
| Networking | VPC, ALB/NLB, CloudFront, Route 53 | Traffic management |
| Security | IAM, KMS, Secrets Manager, WAF | Access & encryption |
| Monitoring | CloudWatch, X-Ray, CloudTrail | Observability |
| Serverless | Lambda, API Gateway, Step Functions, EventBridge | Event-driven apps |
| AI/ML | Bedrock, SageMaker, Kendra | AI-powered applications |

### Architecture Patterns

| Pattern | Services | Use Case |
|---------|----------|----------|
| Three-Tier | ALB + ECS/EKS + RDS | Traditional web apps |
| Serverless API | API Gateway + Lambda + DynamoDB | REST/GraphQL APIs |
| Event-Driven | EventBridge + Lambda + SQS | Async processing |
| Microservices | EKS + Service Mesh + RDS | Complex applications |
| Data Lake | S3 + Glue + Athena + Redshift | Analytics |
| GenAI RAG | Bedrock + Kendra + Lambda | AI assistants |

## 2025-2026 Best Practices

### Compute Selection

| Workload | Recommendation |
|----------|----------------|
| General compute | Graviton (ARM64) instances |
| Containers | Fargate for simplicity, EKS for control |
| Short tasks (<15min) | Lambda |
| Batch processing | Batch with Spot instances |
| ML inference | Inferentia/Graviton |

### Architecture Decisions

| Decision | Recommendation |
|----------|----------------|
| Baseline HA | Multi-AZ for all production |
| DR strategy | Multi-region for business-critical |
| Container runtime | Fargate unless specific EKS needs |
| Database | Aurora Serverless v2 for variable load |
| Caching | ElastiCache Serverless or CloudFront |
| Event routing | EventBridge for decoupling |

### Serverless-First Approach

Prefer serverless for:
- APIs (API Gateway + Lambda)
- Event processing (EventBridge + Lambda)
- Data processing (Glue, Athena)
- Storage (S3, DynamoDB)

Benefits: 60-80% cost reduction, auto-scaling, zero server management

### Governance as Code

- Validate architecture in CI/CD pipelines
- Enforce subnet associations, security groups, NACLs
- Use AWS Config rules for compliance
- Implement Service Control Policies (SCPs)

## Quick Decision Guide

```
Need serverless?
├── Yes → Lambda + API Gateway + DynamoDB
└── No → Containers?
    ├── Yes → EKS (complex) or ECS/Fargate (simple)
    └── No → EC2 (legacy/specific requirements)

Database selection:
├── Relational → Aurora Serverless v2
├── Key-value → DynamoDB
├── Cache → ElastiCache Serverless
├── Document → DocumentDB
└── Graph → Neptune

Event processing:
├── Async → SQS + Lambda
├── Real-time → Kinesis Data Streams
├── Event routing → EventBridge
└── Orchestration → Step Functions
```

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and quick reference |
| [checklist.md](checklist.md) | Architecture review checklist |
| [examples.md](examples.md) | Implementation examples (Terraform) |
| [templates.md](templates.md) | Reusable templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for AWS architecture |

## Related Methodologies

| Methodology | Path |
|-------------|------|
| Terraform | [../terraform.md](../terraform.md) |
| Kubernetes | [../kubernetes.md](../kubernetes.md) |
| Docker | [../docker.md](../docker.md) |
| GCP | [../gcp-architecture.md](../gcp-architecture.md) |

## References

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Serverless Patterns](https://serverlessland.com/patterns)
- [AWS Well-Architected Tool](https://aws.amazon.com/well-architected-tool/)
