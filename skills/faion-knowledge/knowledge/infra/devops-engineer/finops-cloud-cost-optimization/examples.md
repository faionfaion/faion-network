# FinOps Real-World Examples

## Example 1: E-Commerce Platform Cost Reduction

### Scenario

Mid-size e-commerce company with $150K/month AWS spend, experiencing 25% waste.

### Analysis

| Resource Type | Monthly Spend | Waste Identified |
|---------------|---------------|------------------|
| EC2 Compute | $80,000 | 40% oversized, dev always-on |
| RDS Databases | $35,000 | Multi-AZ for dev/staging |
| S3 Storage | $20,000 | No lifecycle policies |
| Data Transfer | $15,000 | Cross-AZ traffic |

### Optimizations Applied

**1. Rightsizing (Savings: $24,000/month)**
```
Before: 50x m5.2xlarge (avg 15% CPU utilization)
After:  50x m5.large + autoscaling (target 60% CPU)
Savings: 75% compute reduction
```

**2. Dev Environment Scheduling (Savings: $8,000/month)**
```
Before: Dev/staging running 24/7
After:  Scheduled 7am-7pm weekdays (12h x 5d = 60h/week)
Savings: 64% of dev compute costs
```

**3. Storage Lifecycle (Savings: $10,000/month)**
```
Implemented:
- Move to S3 IA after 30 days
- Archive to Glacier after 90 days
- Delete temp data after 7 days
Savings: 50% storage costs
```

**4. Reserved Instances (Savings: $28,000/month)**
```
Analyzed 6 months data:
- Purchased 3-year Convertible RIs for baseline
- Coverage: 70% of production compute
- Discount: 35% on covered usage
```

### Results

| Metric | Before | After |
|--------|--------|-------|
| Monthly spend | $150,000 | $80,000 |
| Waste percentage | 25% | 5% |
| Savings | - | $70,000/month |
| Annual impact | - | $840,000 |

---

## Example 2: SaaS Startup Savings Plans Strategy

### Scenario

B2B SaaS with variable workloads, $50K/month AWS, no commitment discounts.

### Analysis

```
Workload pattern:
- Baseline: $30K/month (stable)
- Variable: $15K/month (spiky, unpredictable)
- Burst: $5K/month (occasional peaks)
```

### Strategy

**Phase 1: Conservative Compute Savings Plans**
```
Hourly commitment: $20/hour ($14,600/month)
Coverage: 48% of average spend
Risk: Low (well under baseline)
Savings: $5,256/month (36% on covered)
```

**Phase 2: Add EC2 Instance Savings Plans (Month 3)**
```
Additional commitment: $10/hour ($7,300/month)
Total coverage: 72% of baseline
Combined savings: $8,760/month
```

**Phase 3: Spot for Batch Jobs (Month 4)**
```
Migrated: Background jobs, data processing
Spot usage: $3,000/month (was $10,000 On-Demand)
Savings: $7,000/month
```

### Final Architecture

| Workload Type | Pricing Model | Monthly Cost |
|---------------|---------------|--------------|
| Core services | Savings Plans | $21,900 |
| Variable services | On-Demand | $8,000 |
| Batch processing | Spot | $3,000 |
| **Total** | - | **$32,900** |

**Total Savings: $17,100/month (34%)**

---

## Example 3: ML Training Cost Optimization

### Scenario

AI startup spending $85K/month on GPU training, mostly On-Demand.

### Original Setup

```
Training jobs: 20 concurrent on p3.8xlarge ($12.24/hr On-Demand)
Average training time: 48 hours
Monthly GPU hours: 19,200
Monthly cost: $235,008
```

### Optimization Strategy

**1. Spot Instances with Checkpointing**
```python
# Checkpoint every 30 minutes
checkpoint_callback = ModelCheckpoint(
    dirpath='s3://checkpoints/',
    save_top_k=3,
    every_n_train_steps=1000
)

# Handle spot interruption
def on_termination_notice():
    save_checkpoint()
    log_progress_to_dynamodb()
```

```
Spot price: ~$3.67/hr (70% discount)
Interruption rate: ~5%
Additional training time (restarts): 10%
```

**2. Right-sized GPU Selection**
```
Before: p3.8xlarge (4x V100) for all jobs
After:
- Small models: g4dn.xlarge (1x T4) - $0.526/hr
- Medium models: p3.2xlarge (1x V100) - $3.06/hr
- Large models: p3.8xlarge (4x V100) - $12.24/hr (spot)
```

**3. Mixed Precision Training**
```python
# Enable automatic mixed precision
scaler = torch.cuda.amp.GradScaler()
with torch.cuda.amp.autocast():
    output = model(input)
    loss = criterion(output, target)
```
```
Training speedup: 2x
GPU hours needed: 50% reduction
```

### Results

| Metric | Before | After |
|--------|--------|-------|
| Monthly GPU hours | 19,200 | 10,560 |
| Average cost/hour | $12.24 | $4.12 |
| Monthly spend | $235,008 | $43,507 |
| Cost per model | $11,750 | $2,175 |

**Total Savings: $191,501/month (81%)**

---

## Example 4: Multi-Cloud FinOps Implementation

### Scenario

Enterprise with AWS ($500K), Azure ($300K), GCP ($200K) monthly spend.

### Challenges

- No unified visibility
- Inconsistent tagging
- Separate optimization efforts
- 35% estimated waste

### Implementation

**1. Unified Tagging Standard**
```yaml
# Mandatory tags (all providers)
mandatory_tags:
  - project        # Project identifier
  - environment    # prod/staging/dev/sandbox
  - owner          # Team or individual
  - cost-center    # Finance allocation code

# Recommended tags
recommended_tags:
  - application    # Application name
  - data-classification  # public/internal/confidential
  - automation     # terraform/manual
```

**2. Centralized Dashboard**
```
Tool: CloudHealth / Apptio
Integration:
- AWS: CUR → S3 → CloudHealth
- Azure: Cost Management API
- GCP: BigQuery billing export

Unified views:
- Total spend by provider
- Cost by team/project
- Waste identification
- Commitment coverage
```

**3. Provider-Specific Optimizations**

| Provider | Action | Savings |
|----------|--------|---------|
| AWS | 3-year Convertible RIs (65% coverage) | $97,500/month |
| Azure | Reserved VMs + Hybrid Benefit | $54,000/month |
| GCP | Committed Use Discounts + Sustained Use | $36,000/month |
| All | Rightsizing + idle termination | $70,000/month |

### Results

| Provider | Before | After | Savings |
|----------|--------|-------|---------|
| AWS | $500,000 | $362,500 | 27.5% |
| Azure | $300,000 | $216,000 | 28.0% |
| GCP | $200,000 | $144,000 | 28.0% |
| **Total** | **$1,000,000** | **$722,500** | **27.8%** |

**Annual Savings: $3.33M**

---

## Example 5: Kubernetes Cost Optimization

### Scenario

Platform team running 500-node GKE cluster, $120K/month.

### Analysis

```
Cluster profile:
- 500 nodes (n2-standard-8)
- Average CPU utilization: 25%
- Average memory utilization: 40%
- Node autoscaler: disabled
```

### Optimizations

**1. Right-sized Node Pools**
```yaml
# Before: one-size-fits-all
nodePools:
  - name: default
    machineType: n2-standard-8
    nodeCount: 500

# After: workload-specific pools
nodePools:
  - name: cpu-intensive
    machineType: c2-standard-8
    autoscaling:
      minNodeCount: 10
      maxNodeCount: 100
  - name: memory-intensive
    machineType: n2-highmem-4
    autoscaling:
      minNodeCount: 20
      maxNodeCount: 150
  - name: general
    machineType: e2-standard-4
    autoscaling:
      minNodeCount: 50
      maxNodeCount: 300
```

**2. Spot Node Pool for Batch**
```yaml
nodePools:
  - name: batch-spot
    machineType: e2-standard-8
    preemptible: true
    autoscaling:
      minNodeCount: 0
      maxNodeCount: 200
    taints:
      - key: cloud.google.com/gke-spot
        value: "true"
        effect: NoSchedule
```

**3. Vertical Pod Autoscaler (VPA)**
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: api-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
      - containerName: api
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 2
          memory: 4Gi
```

**4. Committed Use Discounts**
```
Baseline nodes: 150 (always running)
CUD commitment: 150 x n2-standard-4
Term: 1 year
Discount: 37%
```

### Results

| Metric | Before | After |
|--------|--------|-------|
| Average node count | 500 | 280 |
| CPU utilization | 25% | 55% |
| Memory utilization | 40% | 65% |
| Monthly spend | $120,000 | $62,400 |

**Savings: $57,600/month (48%)**

---

## Key Takeaways

| Optimization | Typical Savings | Implementation Effort |
|--------------|-----------------|----------------------|
| Unused resource cleanup | 10-20% | Low |
| Dev environment scheduling | 40-60% of dev costs | Low |
| Rightsizing | 15-25% | Medium |
| Savings Plans/RIs | 30-40% of covered | Medium |
| Spot instances | 60-80% | High |
| Storage lifecycle | 30-50% of storage | Low |

## Sources

- [FinOps Foundation Case Studies](https://www.finops.org/resources/)
- [AWS Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)
- [GKE Cost Optimization](https://cloud.google.com/kubernetes-engine/docs/concepts/cost-optimization)
- [CloudZero Customer Stories](https://www.cloudzero.com/customers/)
