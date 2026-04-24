# AWS EC2 & ECS Reference

AWS compute services: EC2 instances, ECS Fargate, task definitions, and services.

## Overview

| Service | Purpose | When to Use |
|---------|---------|-------------|
| EC2 | Virtual machines | Persistent workloads, custom AMIs, full control |
| ECS Fargate | Serverless containers | Microservices, auto-scaling, no infra management |
| ECS EC2 | Container on EC2 | Cost optimization, specific instance requirements |
| ECR | Container registry | Store/manage Docker images |

## EC2 Instance Types (2025)

### General Purpose

| Type | vCPU | Memory | Use Case |
|------|------|--------|----------|
| t3.micro | 2 | 1 GB | Dev/test, low traffic |
| t3.small | 2 | 2 GB | Small apps, staging |
| t3.medium | 2 | 4 GB | Web servers, APIs |
| m7g.medium | 1 | 4 GB | Balanced workloads (Graviton3) |
| m7g.large | 2 | 8 GB | Production apps (Graviton3) |

### Compute Optimized

| Type | vCPU | Memory | Use Case |
|------|------|--------|----------|
| c7g.medium | 1 | 2 GB | CPU-intensive (Graviton3) |
| c7g.large | 2 | 4 GB | Batch processing, gaming |

### Memory Optimized

| Type | vCPU | Memory | Use Case |
|------|------|--------|----------|
| r7g.medium | 1 | 8 GB | In-memory caching |
| r7g.large | 2 | 16 GB | Databases, analytics |

## ECS Fargate Task Sizes

| CPU | Memory Options |
|-----|----------------|
| 256 (.25 vCPU) | 512 MB, 1 GB, 2 GB |
| 512 (.5 vCPU) | 1-4 GB |
| 1024 (1 vCPU) | 2-8 GB |
| 2048 (2 vCPU) | 4-16 GB |
| 4096 (4 vCPU) | 8-30 GB |
| 8192 (8 vCPU) | 16-60 GB |
| 16384 (16 vCPU) | 32-120 GB |

## Best Practices (2025-2026)

### Security

- Use IAM roles instead of access keys for EC2/ECS tasks
- Run containers as non-root users
- Use minimal/distroless base images
- Enable ECR image scanning
- Use immutable image tags in ECR
- Configure read-only root filesystem for containers
- Set CPU and memory limits on all tasks

### Cost Optimization

- Use Graviton instances (up to 40% cost savings)
- Leverage Spot instances for fault-tolerant workloads
- Use Fargate Spot for batch processing
- Right-size task definitions (avoid over-provisioning)
- Enable bin-packing for EC2 launch type
- Use Reserved Instances for predictable workloads

### Resilience

- Spread tasks across multiple AZs
- Configure health checks with appropriate parameters
- Use ECS Service Auto Scaling
- Enable Container Insights for monitoring
- Test with AWS Fault Injection Service

### Networking

- Place ECS tasks in private subnets
- Use ALB in public subnets
- Configure VPC endpoints for ECR, CloudWatch, S3
- Use security groups with least-privilege rules

## Quick Reference

| Action | See |
|--------|-----|
| Implementation steps | [checklist.md](checklist.md) |
| CLI commands | [examples.md](examples.md) |
| Task definitions | [templates.md](templates.md) |
| LLM prompts | [llm-prompts.md](llm-prompts.md) |


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| ECS task definition creation | sonnet | Standard configuration pattern |
| EC2 instance type selection | sonnet | Performance/cost analysis |
| ECS service scaling policies | sonnet | Metric-driven configuration |
| Container health checks | haiku | Simple configuration |

## Sources

- [Amazon ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-best-practices.html)
- [ECS Task and Container Security](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-tasks-containers.html)
- [AWS EC2 Guide 2025](https://cloudurable.com/blog/aws-ec2-2025/)
- [ECS Resilience Best Practices](https://aws.amazon.com/blogs/containers/best-practices-for-resilience-and-availability-on-amazon-ecs/)
- [AWS Security Considerations for ECS](https://aws.amazon.com/blogs/security/security-considerations-for-running-containers-on-amazon-ecs/)

---

*AWS EC2 & ECS Reference | faion-infrastructure-engineer*
