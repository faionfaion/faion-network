---
id: aws-architecture-foundations
name: "AWS Architecture - Foundations"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# AWS Architecture - Foundations

Core AWS architectural patterns, VPC design, IAM, monitoring, and Well-Architected Framework principles for production-grade infrastructure.

## Well-Architected Pillars

| Pillar | Focus |
|--------|-------|
| Operational Excellence | Automation, monitoring, improvement |
| Security | IAM, encryption, network security |
| Reliability | Fault tolerance, recovery, scaling |
| Performance | Right-sizing, caching, serverless |
| Cost Optimization | Reserved capacity, spot instances |
| Sustainability | Resource efficiency, managed services |

## Core Services

| Category | Services |
|----------|----------|
| Compute | EC2, ECS, EKS, Lambda, Fargate |
| Storage | S3, EBS, EFS, FSx |
| Database | RDS, Aurora, DynamoDB, ElastiCache |
| Networking | VPC, ALB/NLB, CloudFront, Route 53 |
| Security | IAM, KMS, Secrets Manager, WAF |
| Monitoring | CloudWatch, X-Ray, CloudTrail |

## VPC Architecture

### Three-Tier Design

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project}-${var.environment}"
  cidr = "10.0.0.0/16"

  azs              = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
  public_subnets   = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets  = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = var.environment != "prod"
  one_nat_gateway_per_az = var.environment == "prod"

  enable_dns_hostnames = true
  enable_dns_support   = true

  enable_flow_log                      = true
  create_flow_log_cloudwatch_log_group = true
  create_flow_log_cloudwatch_iam_role  = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }
  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}
```

### Subnet Design

- **Public:** Load balancers, NAT gateways, bastion hosts
- **Private:** Application workloads, EKS nodes
- **Database:** RDS, ElastiCache clusters

### Multi-AZ Best Practices

- Minimum 3 AZs for production
- Spread resources evenly across AZs
- One NAT gateway per AZ in production
- Enable VPC Flow Logs for security auditing

## IAM Roles

### EKS Pod Identity (IRSA)

```hcl
module "app_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name = "${var.project}-${var.environment}-app"

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["app:app"]
    }
  }

  role_policy_arns = {
    policy = aws_iam_policy.app.arn
  }
}

resource "aws_iam_policy" "app" {
  name = "${var.project}-${var.environment}-app"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3Access"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          module.s3_static.s3_bucket_arn,
          "${module.s3_static.s3_bucket_arn}/*"
        ]
      },
      {
        Sid    = "SecretsAccess"
        Effect = "Allow"
        Action = ["secretsmanager:GetSecretValue"]
        Resource = ["arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:${var.project}/${var.environment}/*"]
      },
      {
        Sid      = "KMSDecrypt"
        Effect   = "Allow"
        Action   = ["kms:Decrypt"]
        Resource = [aws_kms_key.secrets.arn]
      }
    ]
  })
}
```

### IAM Best Practices

1. **Least Privilege:** Grant minimum permissions
2. **Use Roles:** Prefer roles over access keys
3. **Scope Resources:** Always specify ARNs, avoid `*`
4. **Enable MFA:** For privileged operations
5. **Rotate Credentials:** Automate key rotation
6. **Use IRSA:** Pod identities for EKS workloads

## Monitoring

### CloudWatch Dashboard

```hcl
resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "${var.project}-${var.environment}"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          title  = "EKS Cluster CPU"
          region = var.region
          metrics = [
            ["ContainerInsights", "pod_cpu_utilization", "ClusterName", module.eks.cluster_name]
          ]
          period = 300
          stat   = "Average"
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          title  = "RDS Connections"
          region = var.region
          metrics = [
            ["AWS/RDS", "DatabaseConnections", "DBClusterIdentifier", module.aurora.cluster_id]
          ]
          period = 300
          stat   = "Average"
        }
      }
    ]
  })
}
```

### CloudWatch Alarms

```hcl
resource "aws_cloudwatch_metric_alarm" "rds_cpu" {
  alarm_name          = "${var.project}-${var.environment}-rds-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "RDS CPU utilization high"

  dimensions = {
    DBClusterIdentifier = module.aurora.cluster_id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]
}

resource "aws_sns_topic" "alerts" {
  name              = "${var.project}-${var.environment}-alerts"
  kms_master_key_id = aws_kms_key.sns.id
}
```

### Monitoring Best Practices

1. Enable Container Insights for EKS
2. Create centralized dashboards
3. Set up proactive alarms
4. Route alerts via SNS topics
5. Enable X-Ray for distributed tracing
6. Enable CloudTrail for API auditing

## Security

### Networking

- Run workloads in private subnets
- Restrictive security group rules
- Network ACLs for additional protection
- Enable VPC Flow Logs
- Use PrivateLink for AWS services

### Encryption

- Enable encryption at rest (EBS, S3, RDS)
- Use TLS/HTTPS for data in transit
- Customer-managed KMS keys for sensitive data
- Store credentials in Secrets Manager
- Use Certificate Manager for SSL/TLS

### IAM

- Minimum required permissions
- No root user access
- Enable MFA for all human users
- Use roles over access keys
- Regular policy audits

## Cost Optimization

### Compute

- **Reserved Instances:** 72% savings for predictable workloads
- **Savings Plans:** 66% savings with flexible commitment
- **Spot Instances:** 90% savings for non-critical workloads
- **Right-Sizing:** Match instances to actual usage
- **Auto Scaling:** Scale down during low-traffic periods

### Storage

- S3 lifecycle policies for tier optimization
- Delete unused EBS snapshots
- Use Intelligent Tiering for S3
- Glacier/Deep Archive for long-term storage

### Networking

- CloudFront to reduce data transfer costs
- VPC endpoints to avoid NAT gateway charges
- One NAT gateway per environment for dev/staging

## Sources

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Best Practices Guide](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
