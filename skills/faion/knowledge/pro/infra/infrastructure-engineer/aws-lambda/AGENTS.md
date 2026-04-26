# AWS Lambda

## Summary

Serverless function design, cold start optimization, layer management, and event source configuration for AWS Lambda. The concrete rule is: initialize all SDK clients and database connections outside the handler; use `ReportBatchItemFailures` for all polling event sources (SQS, Kinesis, DynamoDB Streams); use ARM64 (Graviton2) architecture by default for 20% cost reduction; enable SnapStart for Java/Python/.NET to reduce cold starts by 58-94%.

## Why

Cold starts billed since August 2025 (INIT phase same rate as invocation). Incorrect initialization inside the handler wastes every invocation paying re-initialization cost. Partial batch failure reporting without `ReportBatchItemFailures` sends entire batches to DLQ on a single failure, multiplying processing cost and delay.

## When To Use

- Writing a new Lambda handler (Python, Node.js, Java) for any event source
- Optimizing cold start latency for latency-sensitive APIs
- Configuring SQS, Kinesis, or DynamoDB Streams event source mappings
- Packaging shared dependencies as Lambda layers
- Setting up blue-green or canary deployments with Lambda aliases
- Creating SAM or Terraform IaC for Lambda infrastructure

## When NOT To Use

- Workloads running longer than 15 minutes — use ECS/Fargate containers instead
- Functions requiring GPU — Lambda has no GPU support; use SageMaker or ECS
- Steady-state high-concurrency APIs where provisioned concurrency cost exceeds container cost
- Kubernetes or containerized architecture decisions — use `aws-architecture-services`

## Content

| File | What's inside |
|------|---------------|
| `content/01-function-design.xml` | Handler structure rules, idempotency pattern, cold start optimization strategies table |
| `content/02-event-sources.xml` | SQS/Kinesis/DynamoDB Streams config rules, batch processing with partial failures, event filtering |
| `content/03-checklist.xml` | Code structure, security, deployment, layers, event source, monitoring, cost checklists |

## Templates

| File | Purpose |
|------|---------|
| `templates/sam-basic.yaml` | SAM template: basic function with DynamoDB, arm64, X-Ray |
| `templates/sam-api.yaml` | SAM template: Lambda + API Gateway with access logs |
| `templates/sam-sqs.yaml` | SAM template: SQS trigger with DLQ, batch item failures, event filter |
| `templates/sam-dynamodb-streams.yaml` | SAM template: DynamoDB Streams with bisect-on-error, parallelization |
| `templates/sam-snapstart.yaml` | SAM template: SnapStart for Java and Python with AutoPublishAlias |
| `templates/sam-canary.yaml` | SAM template: canary deployment with CodeDeploy hooks and alarms |
| `templates/tf-lambda-basic.tf` | Terraform: Lambda function with IAM role, X-Ray, CloudWatch logs |
| `templates/tf-lambda-sqs.tf` | Terraform: SQS queue + event source mapping with filter criteria |
