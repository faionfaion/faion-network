# AWS Architecture Services

## Summary

Production-ready patterns for AWS service selection, integration, and deployment. Covers the serverless vs containers decision, event-driven architecture with EventBridge, the AWS Well-Architected Framework six pillars, and Terraform configurations for EKS, RDS Aurora, ALB, S3+CloudFront, and API Gateway. 78% of teams now use hybrid architectures — the concrete rule is: choose Lambda for variable/spiky traffic under 15 minutes; choose containers for steady high-volume 24/7 workloads.

## Why

Choosing the wrong compute service leads to wasted cost (over-provisioned containers) or reliability failures (Lambda timeouts on long-running jobs). Explicit decision criteria and production Terraform examples eliminate guesswork and encode security defaults (no public S3, encrypted RDS, KMS keys, multi-AZ).

## When To Use

- Selecting compute service (Lambda vs ECS/EKS/Fargate) for a new workload
- Designing event-driven architectures with EventBridge, SNS, SQS, or Step Functions
- Applying AWS Well-Architected Framework review to existing infrastructure
- Writing Terraform for EKS clusters, Aurora, ALB, CloudFront, or API Gateway
- Performing cost optimization (Graviton, Spot, Reserved, Instance Scheduler)

## When NOT To Use

- GCP or Azure architecture decisions — use `gcp-arch-patterns` or the Azure methodology instead
- Terraform syntax basics — use `terraform-basics` for HCL fundamentals
- VPC and networking design — use `aws-networking` for subnet, SG, and TGW patterns
- S3 bucket policies and lifecycle rules — use `aws-s3-storage` for storage-specific patterns

## Content

| File | What's inside |
|------|---------------|
| `content/01-service-selection.xml` | Serverless vs containers decision table, hybrid approach, cost model comparison |
| `content/02-event-driven-patterns.xml` | EventBridge, SNS, SQS, Step Functions integration patterns with retry/DLQ rules |
| `content/03-checklist.xml` | Pre-deployment verification rules for EKS, RDS Aurora, ALB, S3, CloudFront, EventBridge, cost |

## Templates

| File | Purpose |
|------|---------|
| `templates/variables.tf` | Common Terraform variables (project, environment, region, VPC CIDR, AZs) |
| `templates/locals.tf` | Common tags and name prefix locals |
| `templates/vpc.tf` | VPC module with NAT gateway, flow logs, Kubernetes subnet tags |
| `templates/kms.tf` | KMS keys for EKS, RDS, S3 encryption |
| `templates/security-groups.tf` | ALB, app, Lambda, RDS security group templates |
| `templates/iam.tf` | ECS task execution, ECS task, Step Functions IAM role templates |
| `templates/alarms.tf` | CloudWatch alarms for ALB, RDS, Lambda with SNS topic |
