# AWS Infrastructure

AWS cloud infrastructure management covering compute, networking, IAM, and infrastructure patterns.

## Overview

| Category | Services | Key Features |
|----------|----------|--------------|
| Compute | EC2, ECS, EKS, Lambda, Fargate | Instances, containers, serverless |
| Networking | VPC, ALB/NLB, CloudFront, Route 53 | Virtual networks, load balancing, CDN |
| IAM | Users, Roles, Policies, Identity Center | Access management, least privilege |
| Storage | S3, EBS, EFS | Object, block, file storage |
| Database | RDS, Aurora, DynamoDB | Relational, NoSQL |
| Monitoring | CloudWatch, X-Ray, CloudTrail | Metrics, tracing, auditing |

## Well-Architected Framework (6 Pillars)

| Pillar | Focus | Key Practices |
|--------|-------|---------------|
| Operational Excellence | Automation, monitoring, improvement | IaC, runbooks, observability |
| Security | IAM, encryption, network security | Least privilege, encryption at rest/transit |
| Reliability | Fault tolerance, recovery, scaling | Multi-AZ, auto-scaling, backups |
| Performance Efficiency | Right-sizing, caching, serverless | Instance selection, caching layers |
| Cost Optimization | Reserved capacity, spot instances | Savings Plans, right-sizing, lifecycle policies |
| Sustainability | Resource efficiency, managed services | Graviton, serverless, efficient architectures |

## AWS CLI Configuration

### Installation

```bash
# Install AWS CLI v2 (Linux)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify
aws --version
```

### Profile Management

```bash
# Configure default profile
aws configure
# Input: Access Key ID, Secret Access Key, Region, Output format

# Configure named profile
aws configure --profile production

# List profiles
aws configure list-profiles

# Use specific profile
aws s3 ls --profile production
export AWS_PROFILE=production
```

### Environment Variables

```bash
# Authentication
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_SESSION_TOKEN="your-session-token"

# Region
export AWS_DEFAULT_REGION="us-east-1"
export AWS_REGION="us-east-1"

# Output format
export AWS_DEFAULT_OUTPUT="json"  # json | text | table | yaml
```

### Credentials File

```ini
# ~/.aws/credentials
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY

[production]
aws_access_key_id = PROD_ACCESS_KEY
aws_secret_access_key = PROD_SECRET_KEY

[development]
role_arn = arn:aws:iam::123456789012:role/DevRole
source_profile = default
```

### Config File

```ini
# ~/.aws/config
[default]
region = us-east-1
output = json

[profile production]
region = eu-west-1
output = table

[profile development]
region = us-west-2
role_arn = arn:aws:iam::123456789012:role/DevRole
source_profile = default
```

## Deployment Pattern

```bash
# Build and push Docker image
docker build -t my-app:latest .
aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_URI
docker tag my-app:latest $ECR_URI/my-app:latest
docker push $ECR_URI/my-app:latest

# Update ECS service
aws ecs update-service \
    --cluster my-cluster \
    --service my-service \
    --force-new-deployment

# Wait for deployment
aws ecs wait services-stable --cluster my-cluster --services my-service
```

## Related References

| Document | Description |
|----------|-------------|
| [checklist.md](checklist.md) | Security and operational checklists |
| [examples.md](examples.md) | EC2, IAM, networking code examples |
| [templates.md](templates.md) | Terraform/CloudFormation templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for AWS tasks |
| [aws-ec2-ecs.md](../aws-ec2-ecs.md) | EC2, ECS, EKS compute services |
| [aws-networking.md](../aws-networking.md) | VPC, IAM, CloudFormation, CloudWatch |
| [aws-lambda.md](../aws-lambda.md) | Lambda serverless functions |
| [aws-s3-storage.md](../aws-s3-storage.md) | S3, RDS, Aurora storage |
| [aws-architecture-foundations.md](../aws-architecture-foundations.md) | VPC design, Well-Architected |
| [aws-architecture-services.md](../aws-architecture-services.md) | Service architecture patterns |

## Sources

- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/latest/userguide/)
- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Best Practices](https://aws.amazon.com/architecture/best-practices/)
- [AWS Security Best Practices 2026](https://www.sentinelone.com/cybersecurity-101/cloud-security/aws-security-best-practices/)
- [AWS re:Invent 2025 Infrastructure Guide](https://aws.amazon.com/blogs/infrastructure-sustainability/aws-reinvent-2025-complete-guide-to-global-infrastructure-and-sustainability/)
- [AWS Success 2026](https://cloudvisor.co/aws-success-in-2026-build-smart-scale-efficiently-stay-sustainable/)
