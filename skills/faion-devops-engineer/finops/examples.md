# FinOps Examples

Real-world scenarios and solutions for cloud cost optimization.

## Example 1: Untagged Resource Discovery

**Scenario:** 25% of monthly cloud spend is unallocated, making cost attribution impossible.

**Solution:**

```sql
-- AWS Cost Explorer query for untagged resources
SELECT
  line_item_product_code,
  SUM(line_item_unblended_cost) as cost
FROM cost_and_usage_report
WHERE resource_tags_user_environment IS NULL
  AND line_item_line_item_type = 'Usage'
GROUP BY line_item_product_code
ORDER BY cost DESC
LIMIT 20;
```

**Implementation Steps:**

1. Generate untagged resource report
2. Identify top 10 cost contributors without tags
3. Work with resource owners to apply tags
4. Set up SCP/Policy to prevent untagged deployments
5. Target: Reduce unallocated spend from 25% to <10%

**Expected Outcome:** Full cost visibility, accurate showback reports.

---

## Example 2: Idle EC2 Instance Cleanup

**Scenario:** Development team has 50+ EC2 instances running 24/7, but usage analysis shows 60% have <5% CPU utilization.

**AWS CLI Script:**

```bash
#!/bin/bash
# Find idle instances (avg CPU < 5% over 7 days)

INSTANCES=$(aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query "Reservations[].Instances[].InstanceId" \
  --output text)

for INSTANCE_ID in $INSTANCES; do
  AVG_CPU=$(aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --dimensions Name=InstanceId,Value=$INSTANCE_ID \
    --start-time $(date -d '7 days ago' --iso-8601=seconds) \
    --end-time $(date --iso-8601=seconds) \
    --period 86400 \
    --statistics Average \
    --query 'Datapoints[].Average | avg(@)' \
    --output text)

  if (( $(echo "$AVG_CPU < 5" | bc -l) )); then
    echo "Idle instance: $INSTANCE_ID (Avg CPU: $AVG_CPU%)"
  fi
done
```

**Expected Outcome:** Terminate or rightsize 30 instances, saving ~$15,000/month.

---

## Example 3: Savings Plans Optimization

**Scenario:** Organization spends $100,000/month on EC2 with On-Demand pricing.

**Analysis:**

| Usage Pattern | Recommendation |
|---------------|----------------|
| 60% steady baseline | 1-year Compute Savings Plan (no upfront) |
| 25% predictable peaks | 1-year EC2 Instance Savings Plan |
| 15% variable | Keep On-Demand |

**Calculation:**

```
Baseline (60%): $60,000 * 0.66 (34% discount) = $39,600
Predictable (25%): $25,000 * 0.62 (38% discount) = $15,500
Variable (15%): $15,000 * 1.00 = $15,000
----------------------------------------
New monthly cost: $70,100
Savings: $29,900/month (29.9%)
Annual savings: $358,800
```

**Expected Outcome:** 30% reduction in compute costs with 1-year commitment.

---

## Example 4: Storage Lifecycle Optimization

**Scenario:** S3 bucket with 50TB of data, all in Standard tier, costing $1,150/month.

**Analysis:**

| Data Age | Volume | Current Cost | Recommended Tier |
|----------|--------|--------------|------------------|
| <30 days | 10TB | $230 | Standard |
| 30-90 days | 15TB | $345 | Standard-IA |
| 90-365 days | 15TB | $345 | Glacier IR |
| >365 days | 10TB | $230 | Glacier Deep Archive |

**Lifecycle Policy:**

```json
{
  "Rules": [
    {
      "ID": "MoveToIA",
      "Status": "Enabled",
      "Filter": {},
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER_IR"
        },
        {
          "Days": 365,
          "StorageClass": "DEEP_ARCHIVE"
        }
      ]
    }
  ]
}
```

**New Cost Calculation:**

| Tier | Volume | Price/GB | Monthly Cost |
|------|--------|----------|--------------|
| Standard | 10TB | $0.023 | $230 |
| Standard-IA | 15TB | $0.0125 | $187.50 |
| Glacier IR | 15TB | $0.004 | $60 |
| Deep Archive | 10TB | $0.00099 | $9.90 |
| **Total** | 50TB | - | **$487.40** |

**Expected Outcome:** 58% reduction ($662.60/month savings).

---

## Example 5: Kubernetes Cost Attribution

**Scenario:** Shared Kubernetes cluster with 5 teams, but no per-team cost visibility.

**Solution with OpenCost:**

```yaml
# Install OpenCost for cost allocation
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opencost
  namespace: opencost
spec:
  replicas: 1
  selector:
    matchLabels:
      app: opencost
  template:
    metadata:
      labels:
        app: opencost
    spec:
      containers:
      - name: opencost
        image: ghcr.io/opencost/opencost:latest
        env:
        - name: PROMETHEUS_SERVER_ENDPOINT
          value: "http://prometheus-server.monitoring:80"
```

**Namespace Labels for Attribution:**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: team-alpha
  labels:
    team: alpha
    costcenter: engineering
    environment: production
```

**Query for Per-Team Costs:**

```promql
sum(
  container_memory_working_set_bytes{namespace!=""}
  * on(node) group_left()
  node_price_per_gb_memory
) by (namespace)
```

**Expected Outcome:** Per-namespace cost allocation with daily reports.

---

## Example 6: AI/ML Cost Optimization

**Scenario:** ML team spending $50,000/month on GPU training jobs.

**Current State:**

| Resource | Configuration | Cost/Month |
|----------|--------------|------------|
| Training instances | 10x p4d.24xlarge On-Demand | $45,000 |
| Storage | 5TB EBS gp3 | $2,000 |
| Data transfer | 10TB/month | $3,000 |

**Optimization Strategy:**

1. **Spot Instances with Checkpointing:**
```python
# Training script with checkpointing
import torch

def train_with_checkpoints(model, epochs):
    checkpoint_interval = 100  # steps
    for epoch in range(epochs):
        for step, batch in enumerate(dataloader):
            # Training logic
            if step % checkpoint_interval == 0:
                torch.save({
                    'epoch': epoch,
                    'step': step,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                }, f's3://checkpoints/model_{epoch}_{step}.pt')
```

2. **GPU Rightsizing:**
```bash
# Analyze GPU utilization
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total \
  --format=csv -l 60 > gpu_utilization.csv
```

**Optimized State:**

| Resource | Configuration | Cost/Month | Savings |
|----------|--------------|------------|---------|
| Training instances | 10x p4d.24xlarge Spot | $13,500 | 70% |
| Storage | 5TB EBS gp3 | $2,000 | 0% |
| Data transfer | Same-region + VPC endpoint | $1,500 | 50% |
| **Total** | - | **$17,000** | **66%** |

**Expected Outcome:** $33,000/month savings (66% reduction).

---

## Example 7: Cross-Account Cost Governance

**Scenario:** Enterprise with 50 AWS accounts, inconsistent cost management practices.

**AWS Organizations SCP for Budget Control:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyExpensiveInstances",
      "Effect": "Deny",
      "Action": "ec2:RunInstances",
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "ForAnyValue:StringLike": {
          "ec2:InstanceType": [
            "*.metal",
            "*.24xlarge",
            "p4d.*",
            "p5.*"
          ]
        }
      }
    },
    {
      "Sid": "RequireTagging",
      "Effect": "Deny",
      "Action": [
        "ec2:RunInstances",
        "rds:CreateDBInstance"
      ],
      "Resource": "*",
      "Condition": {
        "Null": {
          "aws:RequestTag/Environment": "true",
          "aws:RequestTag/Owner": "true"
        }
      }
    }
  ]
}
```

**Expected Outcome:** Consistent tagging, prevented expensive resource launches without approval.

---

## Example 8: Budget Alert Configuration

**Scenario:** Teams frequently exceed budgets without awareness.

**AWS Budget with SNS Alert:**

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  TeamBudget:
    Type: AWS::Budgets::Budget
    Properties:
      Budget:
        BudgetName: team-alpha-monthly
        BudgetType: COST
        TimeUnit: MONTHLY
        BudgetLimit:
          Amount: 10000
          Unit: USD
        CostFilters:
          TagKeyValue:
            - "user:team$alpha"
      NotificationsWithSubscribers:
        - Notification:
            NotificationType: ACTUAL
            ComparisonOperator: GREATER_THAN
            Threshold: 80
          Subscribers:
            - SubscriptionType: EMAIL
              Address: team-alpha@company.com
            - SubscriptionType: SNS
              Address: !Ref BudgetAlertTopic
        - Notification:
            NotificationType: FORECASTED
            ComparisonOperator: GREATER_THAN
            Threshold: 100
          Subscribers:
            - SubscriptionType: EMAIL
              Address: finops@company.com
```

**Expected Outcome:** Teams alerted at 80% actual spend, finance alerted when forecast exceeds budget.

## Sources

- [AWS Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/)
- [GCP Cost Management](https://cloud.google.com/cost-management)
- [OpenCost Documentation](https://www.opencost.io/docs/)
