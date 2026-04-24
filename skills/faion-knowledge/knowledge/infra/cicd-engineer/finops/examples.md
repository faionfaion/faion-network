# FinOps Examples

## Cost Visibility Examples

### Tagging Strategy Example

```yaml
# Mandatory tags for all resources
mandatory_tags:
  - key: project
    description: Project or product name
    example: "ecommerce-platform"

  - key: environment
    description: Deployment environment
    values: [prod, staging, dev, test]

  - key: owner
    description: Team or person responsible
    example: "platform-team"

  - key: cost-center
    description: Financial cost center code
    example: "CC-1234"

# Optional but recommended tags
optional_tags:
  - key: application
    description: Application name within project

  - key: data-classification
    values: [public, internal, confidential, restricted]

  - key: automation
    values: [true, false]
    description: Whether resource is managed by IaC
```

### AWS Cost Allocation Tags

```bash
# Enable cost allocation tags via AWS CLI
aws ce update-cost-allocation-tags-status \
  --cost-allocation-tags-status \
    "TagKey=project,Status=Active" \
    "TagKey=environment,Status=Active" \
    "TagKey=owner,Status=Active" \
    "TagKey=cost-center,Status=Active"
```

### GCP Labels Example

```hcl
# Terraform - GCP resource with labels
resource "google_compute_instance" "app_server" {
  name         = "app-server-prod"
  machine_type = "e2-standard-4"

  labels = {
    project         = "ecommerce"
    environment     = "prod"
    owner           = "platform-team"
    cost-center     = "cc-1234"
    managed-by      = "terraform"
  }
}
```

## Rightsizing Examples

### AWS Instance Rightsizing Analysis

```bash
# Get EC2 rightsizing recommendations
aws compute-optimizer get-ec2-instance-recommendations \
  --filters Name=Finding,Values=OVER_PROVISIONED \
  --query 'instanceRecommendations[*].{
    InstanceId: instanceArn,
    Current: currentInstanceType,
    Recommended: recommendationOptions[0].instanceType,
    Savings: recommendationOptions[0].projectedUtilizationMetrics[0].value
  }' \
  --output table
```

### Kubernetes Resource Optimization

```yaml
# Before: Overprovisioned pod
apiVersion: v1
kind: Pod
metadata:
  name: api-server
spec:
  containers:
  - name: api
    resources:
      requests:
        cpu: "2"
        memory: "4Gi"
      limits:
        cpu: "4"
        memory: "8Gi"

---
# After: Right-sized based on actual usage (avg: 0.3 CPU, 512Mi)
apiVersion: v1
kind: Pod
metadata:
  name: api-server
spec:
  containers:
  - name: api
    resources:
      requests:
        cpu: "500m"      # 2x average usage
        memory: "1Gi"    # 2x average usage
      limits:
        cpu: "1"
        memory: "2Gi"
```

### VPA (Vertical Pod Autoscaler) Example

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: api-server-vpa
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
        memory: 256Mi
      maxAllowed:
        cpu: 2
        memory: 4Gi
```

## Commitment Discount Examples

### AWS Savings Plans Coverage Analysis

```python
# Python script to analyze Savings Plans coverage
import boto3
from datetime import datetime, timedelta

ce = boto3.client('ce')

# Get Savings Plans coverage
response = ce.get_savings_plans_coverage(
    TimePeriod={
        'Start': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'End': datetime.now().strftime('%Y-%m-%d')
    },
    Granularity='MONTHLY',
    Metrics=['SpendCoveredBySavingsPlans', 'OnDemandCost', 'TotalCost']
)

for period in response['SavingsPlansCoverages']:
    coverage = period['Coverage']
    print(f"Coverage: {coverage['CoveragePercentage']}%")
    print(f"On-Demand Cost: ${float(coverage['OnDemandCost']):.2f}")
    print(f"Spend Covered: ${float(coverage['SpendCoveredBySavingsPlans']):.2f}")
```

### GCP Committed Use Discount

```hcl
# Terraform - GCP CUD reservation
resource "google_compute_reservation" "production" {
  name = "prod-reservation"
  zone = "us-central1-a"

  specific_reservation {
    count = 10
    instance_properties {
      machine_type     = "e2-standard-4"
      min_cpu_platform = "Intel Cascade Lake"
    }
  }

  specific_reservation_required = true
}
```

## Automation Examples

### Scheduled Dev Environment Shutdown

```yaml
# GitHub Actions - Stop dev resources on schedule
name: Dev Environment Scheduler

on:
  schedule:
    # Stop at 7 PM weekdays
    - cron: '0 19 * * 1-5'
    # Start at 8 AM weekdays
    - cron: '0 8 * * 1-5'

jobs:
  manage-dev:
    runs-on: ubuntu-latest
    steps:
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Stop/Start Dev Instances
        run: |
          if [ "${{ github.event.schedule }}" = "0 19 * * 1-5" ]; then
            # Evening - stop instances
            aws ec2 stop-instances --instance-ids \
              $(aws ec2 describe-instances \
                --filters "Name=tag:environment,Values=dev" \
                --query 'Reservations[].Instances[].InstanceId' \
                --output text)
          else
            # Morning - start instances
            aws ec2 start-instances --instance-ids \
              $(aws ec2 describe-instances \
                --filters "Name=tag:environment,Values=dev" \
                --query 'Reservations[].Instances[].InstanceId' \
                --output text)
          fi
```

### Terraform Cost Estimation in CI

```yaml
# GitHub Actions - Infracost integration
name: Terraform Cost

on:
  pull_request:
    paths:
      - 'terraform/**'

jobs:
  infracost:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Infracost
        uses: infracost/actions/setup@v3
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}

      - name: Generate Infracost JSON
        run: |
          infracost breakdown --path=terraform \
            --format=json \
            --out-file=/tmp/infracost.json

      - name: Post comment
        uses: infracost/actions/comment@v1
        with:
          path: /tmp/infracost.json
          behavior: update
```

## Budget Alerts Example

### AWS Budget with SNS Alert

```hcl
# Terraform - AWS Budget
resource "aws_budgets_budget" "monthly_cost" {
  name         = "monthly-total-cost"
  budget_type  = "COST"
  limit_amount = "10000"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "FORECASTED"
    subscriber_email_addresses = ["finops@company.com"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = ["finops@company.com", "cto@company.com"]
  }

  cost_filter {
    name   = "TagKeyValue"
    values = ["user:environment$prod"]
  }
}
```

### GCP Budget Alert

```hcl
# Terraform - GCP Budget
resource "google_billing_budget" "monthly_budget" {
  billing_account = "000000-AAAAAA-BBBBBB"
  display_name    = "Monthly Production Budget"

  budget_filter {
    projects = ["projects/${var.project_id}"]
    labels = {
      environment = "prod"
    }
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = "10000"
    }
  }

  threshold_rules {
    threshold_percent = 0.5
    spend_basis       = "FORECASTED_SPEND"
  }

  threshold_rules {
    threshold_percent = 0.9
    spend_basis       = "CURRENT_SPEND"
  }

  threshold_rules {
    threshold_percent = 1.0
    spend_basis       = "CURRENT_SPEND"
  }

  all_updates_rule {
    monitoring_notification_channels = [
      google_monitoring_notification_channel.finops.id
    ]
    pubsub_topic = google_pubsub_topic.budget_alerts.id
  }
}
```

## AI/ML Cost Examples

### GPU Spot Instance with Checkpointing

```python
# PyTorch training with checkpointing for spot instances
import torch
import signal
import sys

class SpotCheckpointer:
    def __init__(self, model, optimizer, checkpoint_path):
        self.model = model
        self.optimizer = optimizer
        self.checkpoint_path = checkpoint_path
        self.epoch = 0
        self.step = 0

        # Handle spot termination signal
        signal.signal(signal.SIGTERM, self.save_and_exit)

    def save_checkpoint(self):
        torch.save({
            'epoch': self.epoch,
            'step': self.step,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, self.checkpoint_path)
        print(f"Checkpoint saved at epoch {self.epoch}, step {self.step}")

    def load_checkpoint(self):
        if os.path.exists(self.checkpoint_path):
            checkpoint = torch.load(self.checkpoint_path)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.epoch = checkpoint['epoch']
            self.step = checkpoint['step']
            print(f"Resumed from epoch {self.epoch}, step {self.step}")

    def save_and_exit(self, signum, frame):
        print("Spot termination notice received, saving checkpoint...")
        self.save_checkpoint()
        sys.exit(0)
```

### LLM Response Caching

```python
# Redis-based LLM response caching
import hashlib
import json
import redis
from openai import OpenAI

class CachedLLM:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.client = OpenAI()
        self.cache = redis.from_url(redis_url)
        self.cache_ttl = 86400  # 24 hours

    def _cache_key(self, messages, model):
        content = json.dumps({'messages': messages, 'model': model}, sort_keys=True)
        return f"llm:v1:{hashlib.sha256(content.encode()).hexdigest()}"

    def chat(self, messages, model="gpt-4o", use_cache=True):
        cache_key = self._cache_key(messages, model)

        # Check cache
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached:
                return json.loads(cached)

        # Call API
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )

        result = response.choices[0].message.content

        # Cache response
        if use_cache:
            self.cache.setex(cache_key, self.cache_ttl, json.dumps(result))

        return result

# Usage - saves 20-60% on repeated queries
llm = CachedLLM()
response = llm.chat([{"role": "user", "content": "What is FinOps?"}])
```

## Cost Dashboard Query Examples

### AWS Cost Explorer Query

```python
# Python - Get cost by service
import boto3

ce = boto3.client('ce')

response = ce.get_cost_and_usage(
    TimePeriod={
        'Start': '2025-01-01',
        'End': '2025-01-31'
    },
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    GroupBy=[
        {'Type': 'DIMENSION', 'Key': 'SERVICE'},
        {'Type': 'TAG', 'Key': 'environment'}
    ],
    Filter={
        'Tags': {
            'Key': 'environment',
            'Values': ['prod']
        }
    }
)

for group in response['ResultsByTime'][0]['Groups']:
    service = group['Keys'][0]
    env = group['Keys'][1]
    cost = float(group['Metrics']['UnblendedCost']['Amount'])
    print(f"{service} ({env}): ${cost:.2f}")
```

### BigQuery Cost Analysis (GCP)

```sql
-- BigQuery - Monthly cost by project and service
SELECT
  project.id AS project_id,
  service.description AS service,
  ROUND(SUM(cost), 2) AS total_cost,
  ROUND(SUM(IFNULL(credits.amount, 0)), 2) AS credits,
  ROUND(SUM(cost) + SUM(IFNULL(credits.amount, 0)), 2) AS net_cost
FROM
  `billing_export.gcp_billing_export_v1_*`
LEFT JOIN
  UNNEST(credits) AS credits
WHERE
  invoice.month = '202501'
GROUP BY
  project_id, service
ORDER BY
  net_cost DESC
LIMIT 20;
```

---

*FinOps Examples | faion-cicd-engineer*
