# AWS Architecture - Services

Production-ready patterns for AWS service selection, integration, and deployment. Updated for 2025-2026 best practices.

## Overview

This methodology covers service selection decisions, integration patterns, and production configurations for core AWS services.

## Service Categories

| Category | Services | Use Case |
|----------|----------|----------|
| Compute | EKS, ECS, Fargate, Lambda | Container orchestration, serverless |
| Database | RDS Aurora, DynamoDB | Relational, NoSQL |
| Networking | ALB, NLB, API Gateway | Load balancing, API management |
| Storage | S3, EBS, EFS | Object, block, file storage |
| CDN | CloudFront | Static assets, edge caching |
| Events | EventBridge, SNS, SQS | Event-driven architecture |

## Serverless vs Containers Decision (2025-2026)

### Choose Serverless (Lambda) When

- Event-driven workloads with short execution times
- Variable/spiky traffic patterns
- Cost sensitivity for sporadic workloads
- MVPs and rapid prototyping
- Sub-second response requirements with low concurrency

### Choose Containers (EKS/ECS/Fargate) When

- Long-running processes or persistent connections
- Steady, high-volume 24/7 traffic
- Complex microservices requiring specific runtimes
- AI/ML workloads requiring GPU support
- Need for full infrastructure control

### Hybrid Approach (2026 Default)

78% of engineering teams now run hybrid architectures. The decision is not "serverless vs containers" but "which workload belongs where."

| Factor | Serverless | Containers |
|--------|------------|------------|
| Traffic | Variable/Spiky | Steady/Predictable |
| Execution | Short-lived events | Long-running processes |
| Control | Less customization | Full infrastructure control |
| Cost Model | Pay-per-invocation | Pay for provisioned resources |
| Scaling | Automatic, instant | Requires orchestration setup |

## Event-Driven Architecture Patterns

### Amazon EventBridge (2025)

- Handles 1M events/sec with sub-50ms latency
- Native integrations with 140+ AWS and SaaS services
- Cross-account direct delivery (new in 2025)
- Event filtering and transformation

### Integration Patterns

| Pattern | AWS Service | Use Case |
|---------|-------------|----------|
| Choreography | EventBridge | Decoupled event routing |
| Orchestration | Step Functions | Stateful workflows |
| Pub/Sub | SNS | Fan-out notifications |
| Queue | SQS | Async processing, buffering |
| API Gateway | API Gateway + Lambda | Synchronous APIs |

## AWS Well-Architected Framework (2025-2026)

Six pillars for architecture decisions:

1. **Operational Excellence** - Automation, observability
2. **Security** - IAM, encryption, compliance
3. **Reliability** - Multi-AZ, fault tolerance
4. **Performance Efficiency** - Right-sizing, caching
5. **Cost Optimization** - Reserved, Spot, Graviton
6. **Sustainability** - Graviton, efficient workloads

### 2025-2026 Key Trends

- **Graviton Adoption**: Default for most workloads, x86 needs justification
- **AI-Powered Architecture**: Amazon Bedrock for automated Well-Architected reviews
- **Self-Healing Systems**: Agentic AI for autonomous monitoring
- **Instance Scheduler**: Save up to 75% by stopping idle resources

## Files in This Methodology

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre-deployment verification checklist |
| [examples.md](examples.md) | Production Terraform configurations |
| [templates.md](templates.md) | Reusable service templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for architecture decisions |

## Common Pitfalls

1. **Overly permissive IAM** - Always scope to specific ARNs
2. **Public S3 buckets** - Enable block public access
3. **Single AZ deployments** - Critical workloads must span multiple AZs
4. **No encryption** - Encrypt all storage and data transfer
5. **Missing monitoring** - CloudWatch alarms are essential
6. **Hardcoded credentials** - Use IAM roles, Secrets Manager


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Serverless vs containers decision | opus | Strategic choice with implications |
| Lambda vs ECS vs EKS selection | sonnet | Requires understanding trade-offs |
| Service integration patterns | sonnet | Established architectural patterns |
| Event-driven architecture design | opus | Novel problem, needs deep reasoning |

## Sources

- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS Cloud Design Patterns](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/introduction.html)
- [EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)
- [AWS EventBridge](https://aws.amazon.com/eventbridge/)
- [Serverless vs Containers 2026](https://dev.to/ripenapps-technologies/serverless-vs-containers-whats-winning-in-2026-556e)
- [AWS FinOps Guide](https://aws.amazon.com/blogs/aws-cloud-financial-management/a-finops-guide-to-comparing-containers-and-serverless-functions-for-compute/)

---

*AWS Architecture Services | faion-infrastructure-engineer*
