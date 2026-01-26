# FinOps Cloud Cost Optimization Examples

## Case Study 1: SmartNews - Spot + Graviton Migration

### Context
Large-scale news aggregation platform with significant compute requirements for content processing and ML workloads.

### Implementation
- Migrated main compute workloads to Spot Instances
- Adopted AWS Graviton (ARM) processors
- Implemented proper checkpointing for ML training jobs

### Results
| Metric | Improvement |
|--------|-------------|
| Main compute costs | 50% reduction |
| ML workload costs | 15% reduction |
| Latency | Improved (Graviton performance gains) |

### Key Takeaways
- Spot + modern processors = multiplicative savings
- Checkpointing investment pays off for ML workloads
- ARM migration often improves performance alongside cost

---

## Case Study 2: E-Commerce Platform - Hybrid Instance Strategy

### Context
E-commerce platform with predictable baseline traffic and seasonal spikes (Black Friday, holiday sales).

### Before
- 100% on-demand instances
- Monthly compute spend: $150,000
- No commitment-based pricing

### Implementation

```
Workload Distribution:
- Baseline (60%): 3-year Standard RIs
- Predictable growth (20%): 1-year Convertible RIs
- Seasonal/burst (15%): On-Demand
- Batch processing (5%): Spot Instances
```

### Results
| Category | Monthly Cost | Savings |
|----------|--------------|---------|
| RI baseline | $36,000 | 60% off on-demand |
| RI growth buffer | $15,000 | 50% off on-demand |
| On-Demand burst | $22,500 | - |
| Spot batch | $750 | 90% off on-demand |
| **Total** | **$74,250** | **50.5% overall** |

### Key Takeaways
- Layer pricing models for maximum efficiency
- Start conservative with commitments (80% of minimum usage)
- Reserve flexibility for unknown workloads

---

## Case Study 3: SaaS Startup - Rightsizing Exercise

### Context
B2B SaaS startup with 50+ microservices running on oversized instances "just in case."

### Discovery
4-week analysis using CloudWatch metrics revealed:

| Instance Class | Count | Avg CPU | Avg Memory |
|---------------|-------|---------|------------|
| m5.xlarge | 25 | 12% | 28% |
| m5.2xlarge | 15 | 8% | 22% |
| r5.xlarge | 10 | 15% | 35% |

### Implementation
Phased rightsizing over 3 months:

**Phase 1 - Non-prod environments:**
- Downsized all dev instances by 50%
- Validated no performance impact
- Savings: $8,000/month

**Phase 2 - Low-risk production:**
- Rightsized batch processors and background workers
- Implemented auto-scaling policies
- Savings: $12,000/month

**Phase 3 - Critical production:**
- Careful rightsizing with rollback plans
- Converted to Graviton instances
- Savings: $15,000/month

### Results
| Metric | Before | After |
|--------|--------|-------|
| Monthly compute | $85,000 | $50,000 |
| Average CPU utilization | 11% | 45% |
| Instance count | 50 | 42 |
| Total savings | - | 41% |

---

## Case Study 4: ML Platform - Training Cost Optimization

### Context
Machine learning platform running daily model training jobs consuming expensive GPU instances.

### Before
- Training on p3.8xlarge instances (on-demand)
- Monthly GPU spend: $120,000
- No checkpointing implemented
- Jobs occasionally fail, full restart required

### Implementation

**Checkpointing Infrastructure:**
```python
# Checkpoint every N steps
if step % checkpoint_interval == 0:
    save_checkpoint(model, optimizer, step, s3_path)

# Resume from checkpoint on Spot interruption
if checkpoint_exists(s3_path):
    model, optimizer, start_step = load_checkpoint(s3_path)
```

**Spot Strategy:**
- Primary: Spot Instances (p3.8xlarge)
- Fallback: On-Demand (if Spot unavailable > 10 min)
- Diversification: Multiple instance types (p3, p4d, g5)

**GPU Rightsizing:**
- Analyzed model memory requirements
- Matched GPU memory to actual needs
- Some jobs moved to smaller GPU instances

### Results
| Metric | Before | After |
|--------|--------|-------|
| Monthly GPU spend | $120,000 | $38,000 |
| Spot adoption | 0% | 85% |
| Average training cost | $450/job | $140/job |
| Job completion rate | 92% | 96% |
| Total savings | - | 68% |

---

## Case Study 5: Non-Production Environment Scheduling

### Context
Enterprise with multiple environments running 24/7 despite only being used during business hours.

### Discovery
| Environment | Instances | Monthly Cost | Usage Pattern |
|-------------|-----------|--------------|---------------|
| Production | 100 | $80,000 | 24/7 |
| Staging | 50 | $40,000 | Business hours only |
| Development | 75 | $35,000 | Weekdays 8am-8pm |
| QA | 25 | $15,000 | Weekdays only |

### Implementation
AWS Instance Scheduler configuration:

```yaml
# Development schedule
dev-schedule:
  periods:
    - name: weekday-work
      begintime: "08:00"
      endtime: "20:00"
      weekdays: "mon-fri"

# Staging schedule
staging-schedule:
  periods:
    - name: business-hours
      begintime: "06:00"
      endtime: "22:00"
      weekdays: "mon-fri"
```

### Results
| Environment | Before | After | Savings |
|-------------|--------|-------|---------|
| Staging | $40,000 | $13,500 | 66% |
| Development | $35,000 | $10,200 | 71% |
| QA | $15,000 | $4,500 | 70% |
| **Total non-prod** | **$90,000** | **$28,200** | **69%** |

---

## Case Study 6: Cost Allocation Transformation

### Context
300-person engineering organization with no visibility into which teams drive cloud costs.

### Before
- Single AWS account, no tagging
- Monthly bill: $500,000
- Blame game between teams
- No accountability

### Implementation

**Tag Taxonomy:**
```yaml
required_tags:
  - key: Environment
    values: [prod, staging, dev, sandbox]
  - key: Team
    values: [platform, payments, search, ml, data]
  - key: Service
    values: [api, web, worker, db, cache]
  - key: CostCenter
    values: [CC-100, CC-200, CC-300]
```

**Enforcement:**
- AWS SCP preventing untagged resource creation
- Automated weekly report to team leads
- Dashboard in Slack showing team costs

### Results

**Monthly Cost Attribution:**
| Team | Monthly Spend | Actions Taken |
|------|--------------|---------------|
| Platform | $150,000 | Rightsized Kubernetes nodes |
| ML | $180,000 | Moved training to Spot |
| Data | $120,000 | Optimized Redshift |
| Payments | $30,000 | Already efficient |
| Search | $20,000 | Consolidated clusters |

**After 6 months:**
- Total spend: $400,000 (20% reduction)
- 98% resource tagging compliance
- Team-level accountability established
- Proactive optimization culture

---

## Quick Win Examples

### 1. Unattached EBS Volumes
```bash
# Find unattached volumes
aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query 'Volumes[*].{ID:VolumeId,Size:Size,Type:VolumeType}'
```
**Typical savings:** $500-5,000/month

### 2. GP2 to GP3 Migration
```bash
# Modify volume type (no downtime required)
aws ec2 modify-volume \
  --volume-id vol-xxx \
  --volume-type gp3
```
**Savings:** ~20% per volume

### 3. Old Generation Instances
```bash
# Find instances using old generation
aws ec2 describe-instances \
  --query 'Reservations[].Instances[?starts_with(InstanceType, `m4`) || starts_with(InstanceType, `c4`)].{ID:InstanceId,Type:InstanceType}'
```
**Savings:** 10-40% by migrating to current generation

### 4. Unused Elastic IPs
```bash
# Find unused EIPs (charged when unattached)
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==`null`].PublicIp'
```
**Savings:** $3.60/IP/month (small but easy)

---

## Anti-Patterns to Avoid

### 1. Over-Committing to RIs
**Problem:** Purchased 3-year RIs for 100% of capacity, then usage dropped.
**Solution:** Start at 70-80% of minimum usage, use Convertible RIs.

### 2. Spot Without Checkpointing
**Problem:** ML training job ran for 18 hours, Spot interrupted, started over.
**Solution:** Implement checkpointing every N steps.

### 3. Single Spot Instance Type
**Problem:** Requested only c5.4xlarge Spots, frequent unavailability.
**Solution:** Diversify across instance types and AZs.

### 4. Tagging After the Fact
**Problem:** Tried to tag resources retroactively, 40% couldn't be attributed.
**Solution:** Enforce tagging at creation time with SCPs/policies.

### 5. One-Time Optimization
**Problem:** Did rightsizing once, never revisited.
**Solution:** Continuous monitoring and quarterly reviews.

---

*Real examples demonstrate 40-70% savings achievable with proper FinOps practices.*
