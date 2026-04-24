# FinOps (Cloud Cost Optimization)

> **Entry point:** `/faion-net` - invoke for automatic routing.

Cloud Financial Operations framework for optimizing cloud spending across AWS, Azure, and GCP.

## Overview

Cloud spending hit $723.4B in 2025, yet organizations waste 32% ($200B+) on unused resources. FinOps adoption grew 46% in 2025, with 70% of large enterprises maintaining dedicated cloud economics teams.

## Key Statistics (2025-2026)

| Metric | Value |
|--------|-------|
| Global cloud spend | $723.4B (2025) |
| Average waste | 32% of budget |
| Budget overrun | 17% on average |
| FinOps automation adoption | 75% enterprises (projected 2026) |
| Potential global savings | $100B/year |
| Typical ROI | 10-20x investment |

## FinOps Framework Phases

### Phase 1: INFORM

Create visibility into cloud spending:
- Billing data ingestion
- Tagging and cost allocation
- Real-time dashboards
- **Target:** 95%+ allocation accuracy

### Phase 2: OPTIMIZE

Improve efficiency through:
- Rightsizing resources
- Eliminating idle instances
- Commitment discounts (RIs, Savings Plans)
- Storage lifecycle management
- **Target:** 20-30% cost reduction

### Phase 3: OPERATE

Continuous improvement:
- Automated policies
- Budget alerts
- Cost metrics in CI/CD
- Regular reviews

## Core Optimization Strategies

| Strategy | Typical Savings | Complexity |
|----------|-----------------|------------|
| Unused resource elimination | 10-20% | Low |
| Rightsizing | 15-25% | Medium |
| Reserved Instances | Up to 75% | Medium |
| Savings Plans | Up to 72% | Medium |
| Spot Instances | 70-90% | High |
| Storage tiering | 30-50% | Low |

## AI/ML Workload Optimization

| Workload Type | Strategy | Savings |
|---------------|----------|---------|
| Training | Spot + checkpointing | 70-90% |
| Training | GPU rightsizing | 20-40% |
| Inference | Model quantization | 50% |
| Inference | Query caching | 20-60% |
| Both | Batch processing | 30-50% |

## Cloud Provider Tools

| Provider | Native Tools |
|----------|--------------|
| AWS | Cost Optimization Hub, Compute Optimizer, Amazon Q, Trusted Advisor |
| Azure | Azure Advisor, Cost Management, Microsoft Copilot |
| GCP | FinOps Hub 2.0, Active Assist, Gemini Cloud Assist |

## Key Metrics

| Metric | Description |
|--------|-------------|
| Cost Per Unit of Work | e.g., cost per 100k API calls |
| Cost Per GPU Hour | Target: near 100% utilization |
| Tag Compliance | Target: >90% |
| Commitment Coverage | Baseline workload percentage |
| Waste Percentage | Idle/unused resources |

## Folder Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklists by phase |
| [examples.md](examples.md) | Real-world optimization scenarios |
| [templates.md](templates.md) | Tagging policies, budget templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for cost analysis |

## Certifications

- FinOps Certified Practitioner
- FinOps Certified Professional
- FinOps for AI (launched 2025)

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

- [FinOps Foundation](https://www.finops.org/)
- [FinOps X Conference](https://x.finops.org/)
- [AWS Cost Optimization Hub](https://aws.amazon.com/aws-cost-management/aws-cost-optimization-hub/)
- [Google Cloud FinOps Hub](https://cloud.google.com/cost-management)
- [Azure Cost Management](https://azure.microsoft.com/en-us/products/cost-management)
- [CloudZero AI Cost Analytics](https://www.cloudzero.com/)

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-infrastructure-engineer](../faion-infrastructure-engineer/CLAUDE.md) | Resource provisioning |
| [faion-cicd-engineer](../faion-cicd-engineer/CLAUDE.md) | Cost metrics in pipelines |
| [faion-ml-engineer](../../faion-ml-engineer/CLAUDE.md) | AI/ML cost optimization |
