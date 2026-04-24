# FinOps (Cloud Financial Operations)

Cloud cost optimization framework combining finance, technology, and business practices.

## Problem

Cloud spending hit $723.4B in 2025, yet organizations waste 32% ($200B+) on unused resources.

## Market Context (2025-2026)

| Metric | Value |
|--------|-------|
| Cloud spending waste | 32% (~$200B annually) |
| FinOps adoption growth | 46% in 2025 |
| Enterprises with FinOps teams | 70% of large enterprises |
| Cloud budgets exceeding limits | 17% average overrun |
| Projected savings with FinOps | Up to $100B globally/year |
| FinOps automation adoption | 75% of enterprises by 2026 |

## FinOps Framework Phases

### Phase 1: INFORM

Create visibility into cloud spending.

| Activity | Target |
|----------|--------|
| Billing data ingestion | 100% coverage |
| Tagging implementation | 95%+ allocation accuracy |
| Cost dashboards | Real-time for all stakeholders |
| Anomaly detection | Automated alerts |

### Phase 2: OPTIMIZE

Improve efficiency through active measures.

| Strategy | Expected Savings |
|----------|------------------|
| Rightsizing | 15-30% |
| Spot/Preemptible instances | 70-90% |
| Reserved instances/Savings Plans | 30-60% |
| Storage optimization | 20-40% |
| Idle resource termination | 10-25% |

### Phase 3: OPERATE

Establish continuous improvement.

| Practice | Frequency |
|----------|-----------|
| Cost reviews | Weekly |
| Budget alerts | Real-time |
| Optimization recommendations | Automated |
| Forecasting | Weekly/Monthly |

## AI/ML Cost Optimization

AI workloads present unique challenges with GPU costs 5-10x standard compute.

| Metric | Value |
|--------|-------|
| Organizations tracking AI/ML costs | 63% (up from 31% in 2024) |
| Average monthly AI spend | $85,521 |
| GPU cost premium | 5-10x standard compute |

### Training Workloads

| Strategy | Benefit |
|----------|---------|
| Spot instances + checkpointing | 70-90% discount |
| GPU rightsizing | Match workload to instance |
| Approval workflows | Prevent expensive mistakes |

### Inference Workloads

| Strategy | Benefit |
|----------|---------|
| Model quantization | 2x speedup, 50% cost reduction |
| Response caching | 20-60% savings |
| Request batching | Efficient GPU utilization |

## Key Metrics

### Cost Efficiency

| Metric | Description |
|--------|-------------|
| Cost Per Unit of Work | e.g., cost per 100k tokens |
| Cost Per GPU Hour | Target: near 100% utilization |
| Unit Economics | Cost per customer, feature, transaction |
| Waste Percentage | Unallocated/unused resources |

### Tag Coverage

| Level | Compliance |
|-------|------------|
| Target | >90% (100% unrealistic due to untaggable resources) |
| Critical tags | Environment, Owner, Project, CostCenter |
| Initial goal | >80% for high-impact tags |

## Cloud Provider Features (2025)

| Provider | Feature |
|----------|---------|
| AWS | Cost Optimization Hub + Amazon Q, Savings Plans for all databases |
| GCP | FinOps Hub 2.0, AI anomaly detection, Gemini Cloud Assist |
| Azure | Cost Management, Carbon optimization dashboard |
| Oracle | Carbon Emissions Reporting (GHG Protocol compliant) |

## ROI Expectations

| Investment | Return |
|------------|--------|
| Starting team | 1-2 people part-time |
| Scaled team | 3-7 for $10-50M spend |
| Tool costs | $0-100K first year |
| Typical ROI | 10-20x |
| Time to results | 30-60 days visible savings |
| Cultural transformation | 12-18 months |

## Certifications

| Certification | Provider |
|---------------|----------|
| FinOps Certified Practitioner | FinOps Foundation |
| FinOps Certified Professional | FinOps Foundation |
| FinOps for AI (new 2025) | FinOps Foundation |

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Real-world scenarios |
| [templates.md](templates.md) | Reusable templates |
| [llm-prompts.md](llm-prompts.md) | AI-assisted analysis prompts |

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
- [State of FinOps Report](https://data.finops.org/)
- [AWS Cost Optimization Hub](https://aws.amazon.com/aws-cost-management/aws-cost-optimization-hub/)
- [Google Cloud FinOps Hub](https://cloud.google.com/cost-management)
- [CloudZero AI Cost Analytics](https://www.cloudzero.com/)
- [FinOps X Conference](https://x.finops.org/)
