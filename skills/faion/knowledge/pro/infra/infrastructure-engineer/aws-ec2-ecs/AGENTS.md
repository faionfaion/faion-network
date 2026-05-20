---
slug: aws-ec2-ecs
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AWS compute services: EC2 instances, ECS Fargate, task definitions, and services.
content_id: "f0a6ab8452c7d6e9"
tags: [aws, ec2, ecs, fargate, containers]
---
# AWS EC2 & ECS Reference

## Summary

**One-sentence:** AWS compute services: EC2 instances, ECS Fargate, task definitions, and services.

**One-paragraph:** AWS compute services: EC2 instances, ECS Fargate, task definitions, and services. Use IAM roles (not access keys), run containers as non-root with read-only root filesystem, spread tasks across multiple AZs, and leverage Graviton for up to 40% cost savings.

## Applies If (ALL must hold)

- EC2: Persistent workloads, custom AMIs, workloads requiring full OS control or specific hardware
- ECS Fargate: Microservices, auto-scaling containerized workloads, teams wanting no infrastructure management
- ECS EC2: Cost optimization at scale, specific instance type requirements, GPU workloads
- ECR: Storing and managing Docker images with integrated IAM and vulnerability scanning

## Skip If (ANY kills it)

- ECS Fargate for batch jobs that run infrequently — use Fargate Spot or Lambda for cost efficiency
- EC2 when you do not want to manage OS patching and node lifecycle — prefer Fargate or managed services
- ECS when workload complexity warrants Kubernetes (multi-cluster federation, complex service mesh, custom CRDs)
- EC2 or ECS for simple cron-style tasks — Lambda or ECS Scheduled Tasks are simpler and cheaper

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/infrastructure-engineer/`
