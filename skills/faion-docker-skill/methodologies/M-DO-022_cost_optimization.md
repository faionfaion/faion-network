# M-DO-022: Cloud Cost Optimization

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #cost, #finops, #optimization, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Cloud bills grow unexpectedly. Unused resources run indefinitely. No visibility into spending leads to budget overruns.

## Promise

After this methodology, you will optimize cloud costs systematically. You'll identify waste, right-size resources, and implement cost controls.

## Overview

Cloud cost optimization includes right-sizing, reserved capacity, spot instances, and automated cleanup. FinOps practices provide ongoing visibility.

---

## Framework

### Step 1: Cost Visibility

```bash
# AWS Cost Explorer CLI
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE

# Get recommendations
aws ce get-rightsizing-recommendation \
  --service AmazonEC2 \
  --configuration RecommendationTarget=SAME_INSTANCE_FAMILY
```

```hcl
# AWS Budget
resource "aws_budgets_budget" "monthly" {
  name         = "monthly-budget"
  budget_type  = "COST"
  limit_amount = "1000"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = ["alerts@example.com"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["alerts@example.com"]
  }
}
```

### Step 2: Right-Sizing

```bash
# AWS Compute Optimizer
aws compute-optimizer get-ec2-instance-recommendations \
  --instance-arns arn:aws:ec2:us-east-1:123456789:instance/i-xxx

# Memory utilization check (requires CloudWatch agent)
aws cloudwatch get-metric-statistics \
  --namespace CWAgent \
  --metric-name mem_used_percent \
  --dimensions Name=InstanceId,Value=i-xxx \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-31T00:00:00Z \
  --period 86400 \
  --statistics Average
```

```hcl
# Auto-scaling based on actual usage
resource "aws_autoscaling_policy" "scale_down" {
  name                   = "scale-down-policy"
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 70.0
  }
}

# Scheduled scaling for predictable patterns
resource "aws_autoscaling_schedule" "night" {
  scheduled_action_name  = "night-scale-down"
  min_size               = 1
  max_size               = 2
  desired_capacity       = 1
  recurrence             = "0 22 * * *"
  autoscaling_group_name = aws_autoscaling_group.app.name
}

resource "aws_autoscaling_schedule" "morning" {
  scheduled_action_name  = "morning-scale-up"
  min_size               = 2
  max_size               = 10
  desired_capacity       = 3
  recurrence             = "0 7 * * *"
  autoscaling_group_name = aws_autoscaling_group.app.name
}
```

### Step 3: Reserved Instances / Savings Plans

```hcl
# Calculate RI coverage
# Use AWS Cost Explorer RI Utilization Report

# Savings Plan recommendation
# Check: aws ce get-savings-plans-purchase-recommendation

# Example commitment
# 1-year, No Upfront Savings Plan
# Compute: ~30% savings
# EC2 Instance: ~40% savings

# Strategy:
# 1. Cover baseline with 1-year RIs
# 2. Use Savings Plans for flexibility
# 3. Spot for variable/interruptible
# 4. On-Demand for bursting
```

### Step 4: Spot Instances

```hcl
# EC2 Spot Fleet
resource "aws_spot_fleet_request" "workers" {
  iam_fleet_role                      = aws_iam_role.spot_fleet.arn
  spot_price                          = "0.03"
  target_capacity                     = 5
  allocation_strategy                 = "lowestPrice"
  terminate_instances_with_expiration = true
  valid_until                         = "2025-01-01T00:00:00Z"

  launch_specification {
    instance_type          = "t3.medium"
    ami                    = data.aws_ami.amazon_linux.id
    vpc_security_group_ids = [aws_security_group.workers.id]
    subnet_id              = aws_subnet.private[0].id
  }

  launch_specification {
    instance_type          = "t3a.medium"
    ami                    = data.aws_ami.amazon_linux.id
    vpc_security_group_ids = [aws_security_group.workers.id]
    subnet_id              = aws_subnet.private[0].id
  }
}

# EKS with Spot
resource "aws_eks_node_group" "spot" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "spot-workers"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = aws_subnet.private[*].id
  capacity_type   = "SPOT"
  instance_types  = ["t3.medium", "t3a.medium", "t3.large"]

  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 1
  }
}
```

### Step 5: Resource Cleanup

```bash
# Find unused EBS volumes
aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query "Volumes[*].{ID:VolumeId,Size:Size,Created:CreateTime}"

# Find unattached Elastic IPs
aws ec2 describe-addresses \
  --filters Name=association-id,Values= \
  --query "Addresses[*].{IP:PublicIp,AllocationId:AllocationId}"

# Find old snapshots
aws ec2 describe-snapshots \
  --owner-ids self \
  --query "Snapshots[?StartTime<'2024-01-01'].{ID:SnapshotId,Size:VolumeSize}"

# Find idle load balancers
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:...
```

```hcl
# Auto-delete unused resources with Lambda
resource "aws_lambda_function" "cleanup" {
  function_name = "resource-cleanup"
  role          = aws_iam_role.cleanup.arn
  handler       = "index.handler"
  runtime       = "python3.11"
  timeout       = 300

  filename = "cleanup.zip"
}

resource "aws_cloudwatch_event_rule" "weekly" {
  name                = "weekly-cleanup"
  schedule_expression = "cron(0 2 ? * SUN *)"
}

resource "aws_cloudwatch_event_target" "cleanup" {
  rule      = aws_cloudwatch_event_rule.weekly.name
  target_id = "cleanup"
  arn       = aws_lambda_function.cleanup.arn
}
```

### Step 6: Storage Optimization

```hcl
# S3 Lifecycle rules
resource "aws_s3_bucket_lifecycle_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    id     = "archive-old-logs"
    status = "Enabled"

    filter {
      prefix = "logs/"
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }

  rule {
    id     = "intelligent-tiering"
    status = "Enabled"

    filter {
      prefix = "data/"
    }

    transition {
      days          = 0
      storage_class = "INTELLIGENT_TIERING"
    }
  }
}

# EBS gp3 migration
resource "aws_ebs_volume" "optimized" {
  availability_zone = "us-east-1a"
  size              = 100
  type              = "gp3"
  iops              = 3000
  throughput        = 125  # MB/s

  # gp3 is cheaper than gp2 for most workloads
}
```

---

## Templates

### Cost Dashboard (CloudWatch)

```hcl
resource "aws_cloudwatch_dashboard" "cost" {
  dashboard_name = "cost-overview"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          title   = "Daily Estimated Charges"
          view    = "timeSeries"
          stacked = false
          metrics = [
            ["AWS/Billing", "EstimatedCharges", "Currency", "USD"]
          ]
          period = 86400
          stat   = "Maximum"
        }
      }
    ]
  })
}
```

### Tagging Strategy

```hcl
# Required tags for cost allocation
locals {
  required_tags = {
    Project     = var.project
    Environment = var.environment
    Team        = var.team
    CostCenter  = var.cost_center
    ManagedBy   = "terraform"
  }
}

# Apply to all resources
resource "aws_instance" "app" {
  # ...
  tags = merge(local.required_tags, {
    Name = "app-server"
  })
}
```

---

## Common Mistakes

1. **No cost allocation tags** - Can't attribute spending
2. **Oversized instances** - Start small, scale up
3. **No cleanup automation** - Unused resources accumulate
4. **100% on-demand** - Use RIs/Savings Plans
5. **No budget alerts** - Surprises at month end

---

## Checklist

- [ ] Cost allocation tags defined
- [ ] Budget alerts configured
- [ ] Right-sizing recommendations reviewed
- [ ] Reserved capacity for baseline
- [ ] Spot instances for variable loads
- [ ] Scheduled scaling configured
- [ ] Unused resource cleanup automated
- [ ] Storage lifecycle policies

---

## Next Steps

- M-DO-010: Infrastructure Patterns
- M-DO-007: AWS EC2
- M-DO-009: Terraform Basics

---

*Methodology M-DO-022 v1.0*
