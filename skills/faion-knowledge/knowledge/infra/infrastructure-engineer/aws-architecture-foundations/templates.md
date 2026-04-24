# AWS Architecture Foundations Templates

## Multi-Account Landing Zone

### Directory Structure

```
infrastructure/
├── terraform/
│   ├── organization/           # AWS Organizations, SCPs
│   │   ├── main.tf
│   │   ├── ous.tf
│   │   ├── scps.tf
│   │   └── variables.tf
│   ├── shared/                 # Shared services account
│   │   ├── vpc/
│   │   ├── transit-gateway/
│   │   └── dns/
│   ├── security/               # Security account
│   │   ├── guardduty/
│   │   ├── securityhub/
│   │   └── config/
│   ├── log-archive/            # Log archive account
│   │   ├── s3-logs/
│   │   └── cloudtrail/
│   └── workloads/              # Workload accounts
│       ├── prod/
│       └── staging/
└── modules/
    ├── vpc/
    ├── eks/
    └── monitoring/
```

### Organization Configuration

```hcl
# organization/main.tf
terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "organization/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      ManagedBy   = "terraform"
      Project     = "organization"
      Environment = "management"
    }
  }
}

# organization/variables.tf
variable "region" {
  type    = string
  default = "eu-central-1"
}

variable "allowed_regions" {
  type    = list(string)
  default = ["eu-central-1", "eu-west-1"]
}

variable "security_account_email" {
  type = string
}

variable "log_archive_account_email" {
  type = string
}
```

## VPC Module

### Module Interface

```hcl
# modules/vpc/variables.tf
variable "project" {
  type        = string
  description = "Project name"
}

variable "environment" {
  type        = string
  description = "Environment (dev/staging/prod)"
}

variable "cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "VPC CIDR block"
}

variable "azs" {
  type        = list(string)
  default     = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
  description = "Availability zones"
}

variable "enable_nat_gateway" {
  type        = bool
  default     = true
  description = "Enable NAT Gateway"
}

variable "single_nat_gateway" {
  type        = bool
  default     = false
  description = "Use single NAT Gateway (cost optimization)"
}

variable "enable_flow_logs" {
  type        = bool
  default     = true
  description = "Enable VPC Flow Logs"
}

variable "enable_vpc_endpoints" {
  type        = bool
  default     = true
  description = "Enable VPC Endpoints for AWS services"
}

variable "eks_cluster_name" {
  type        = string
  default     = ""
  description = "EKS cluster name for subnet tagging"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Additional tags"
}

# modules/vpc/outputs.tf
output "vpc_id" {
  value = module.vpc.vpc_id
}

output "vpc_cidr" {
  value = module.vpc.vpc_cidr_block
}

output "public_subnets" {
  value = module.vpc.public_subnets
}

output "private_subnets" {
  value = module.vpc.private_subnets
}

output "database_subnets" {
  value = module.vpc.database_subnets
}

output "database_subnet_group_name" {
  value = module.vpc.database_subnet_group_name
}

output "nat_gateway_ids" {
  value = module.vpc.natgw_ids
}
```

## IAM Role Template

### Application Role

```hcl
# modules/iam-role/main.tf
variable "role_name" {
  type = string
}

variable "project" {
  type = string
}

variable "environment" {
  type = string
}

variable "eks_oidc_provider_arn" {
  type        = string
  default     = ""
  description = "EKS OIDC provider ARN for IRSA"
}

variable "namespace" {
  type        = string
  default     = "default"
  description = "Kubernetes namespace"
}

variable "service_account" {
  type        = string
  default     = ""
  description = "Kubernetes service account name"
}

variable "s3_buckets" {
  type        = list(string)
  default     = []
  description = "S3 bucket ARNs for access"
}

variable "secrets_prefix" {
  type        = string
  default     = ""
  description = "Secrets Manager prefix pattern"
}

variable "sqs_queues" {
  type        = list(string)
  default     = []
  description = "SQS queue ARNs for access"
}

variable "kms_key_arns" {
  type        = list(string)
  default     = []
  description = "KMS key ARNs for encryption"
}

# IRSA trust policy
data "aws_iam_policy_document" "irsa_trust" {
  count = var.eks_oidc_provider_arn != "" ? 1 : 0

  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    principals {
      type        = "Federated"
      identifiers = [var.eks_oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${replace(var.eks_oidc_provider_arn, "/^(.*provider/)/", "")}:sub"
      values   = ["system:serviceaccount:${var.namespace}:${var.service_account}"]
    }

    condition {
      test     = "StringEquals"
      variable = "${replace(var.eks_oidc_provider_arn, "/^(.*provider/)/", "")}:aud"
      values   = ["sts.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "this" {
  name               = "${var.project}-${var.environment}-${var.role_name}"
  assume_role_policy = var.eks_oidc_provider_arn != "" ? data.aws_iam_policy_document.irsa_trust[0].json : data.aws_iam_policy_document.ec2_trust.json

  tags = {
    Project     = var.project
    Environment = var.environment
  }
}

# EC2 trust policy (fallback)
data "aws_iam_policy_document" "ec2_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}
```

## Monitoring Template

### CloudWatch Dashboard

```hcl
# modules/monitoring/variables.tf
variable "project" {
  type = string
}

variable "environment" {
  type = string
}

variable "region" {
  type = string
}

variable "eks_cluster_name" {
  type    = string
  default = ""
}

variable "rds_cluster_id" {
  type    = string
  default = ""
}

variable "alb_arn_suffix" {
  type    = string
  default = ""
}

variable "sns_topic_arn" {
  type        = string
  description = "SNS topic ARN for alarms"
}

# modules/monitoring/dashboard.tf
locals {
  dashboard_widgets = concat(
    var.eks_cluster_name != "" ? local.eks_widgets : [],
    var.rds_cluster_id != "" ? local.rds_widgets : [],
    var.alb_arn_suffix != "" ? local.alb_widgets : []
  )

  eks_widgets = [
    {
      type   = "metric"
      x      = 0
      y      = 0
      width  = 12
      height = 6
      properties = {
        title   = "EKS CPU Utilization"
        region  = var.region
        metrics = [
          ["ContainerInsights", "pod_cpu_utilization", "ClusterName", var.eks_cluster_name]
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
        title   = "EKS Memory Utilization"
        region  = var.region
        metrics = [
          ["ContainerInsights", "pod_memory_utilization", "ClusterName", var.eks_cluster_name]
        ]
        period = 300
        stat   = "Average"
      }
    }
  ]

  rds_widgets = [
    {
      type   = "metric"
      x      = 0
      y      = 6
      width  = 8
      height = 6
      properties = {
        title   = "RDS CPU"
        region  = var.region
        metrics = [
          ["AWS/RDS", "CPUUtilization", "DBClusterIdentifier", var.rds_cluster_id]
        ]
        period = 300
        stat   = "Average"
      }
    },
    {
      type   = "metric"
      x      = 8
      y      = 6
      width  = 8
      height = 6
      properties = {
        title   = "RDS Connections"
        region  = var.region
        metrics = [
          ["AWS/RDS", "DatabaseConnections", "DBClusterIdentifier", var.rds_cluster_id]
        ]
        period = 300
        stat   = "Average"
      }
    },
    {
      type   = "metric"
      x      = 16
      y      = 6
      width  = 8
      height = 6
      properties = {
        title   = "RDS IOPS"
        region  = var.region
        metrics = [
          ["AWS/RDS", "ReadIOPS", "DBClusterIdentifier", var.rds_cluster_id],
          ["AWS/RDS", "WriteIOPS", "DBClusterIdentifier", var.rds_cluster_id]
        ]
        period = 300
        stat   = "Average"
      }
    }
  ]

  alb_widgets = [
    {
      type   = "metric"
      x      = 0
      y      = 12
      width  = 12
      height = 6
      properties = {
        title   = "ALB Request Count"
        region  = var.region
        metrics = [
          ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", var.alb_arn_suffix]
        ]
        period = 60
        stat   = "Sum"
      }
    },
    {
      type   = "metric"
      x      = 12
      y      = 12
      width  = 12
      height = 6
      properties = {
        title   = "ALB Latency"
        region  = var.region
        metrics = [
          ["AWS/ApplicationELB", "TargetResponseTime", "LoadBalancer", var.alb_arn_suffix]
        ]
        period = 60
        stat   = "Average"
      }
    }
  ]
}

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "${var.project}-${var.environment}"
  dashboard_body = jsonencode({
    widgets = local.dashboard_widgets
  })
}
```

## SCP Templates

### Security Baseline SCP

```hcl
# organization/scps.tf
locals {
  scps = {
    deny_root_user = {
      name        = "DenyRootUser"
      description = "Deny all actions for root user"
      targets     = [aws_organizations_organizational_unit.workloads.id]
      content = {
        Version = "2012-10-17"
        Statement = [
          {
            Sid       = "DenyRootUser"
            Effect    = "Deny"
            Action    = "*"
            Resource  = "*"
            Condition = {
              StringLike = {
                "aws:PrincipalArn" = "arn:aws:iam::*:root"
              }
            }
          }
        ]
      }
    }

    require_imdsv2 = {
      name        = "RequireIMDSv2"
      description = "Require EC2 instances to use IMDSv2"
      targets     = [aws_organizations_organizational_unit.workloads.id]
      content = {
        Version = "2012-10-17"
        Statement = [
          {
            Sid    = "RequireIMDSv2"
            Effect = "Deny"
            Action = "ec2:RunInstances"
            Resource = "arn:aws:ec2:*:*:instance/*"
            Condition = {
              StringNotEquals = {
                "ec2:MetadataHttpTokens" = "required"
              }
            }
          }
        ]
      }
    }

    require_encryption = {
      name        = "RequireEncryption"
      description = "Require encryption for S3 and EBS"
      targets     = [aws_organizations_organizational_unit.workloads.id]
      content = {
        Version = "2012-10-17"
        Statement = [
          {
            Sid       = "DenyUnencryptedS3"
            Effect    = "Deny"
            Action    = "s3:PutObject"
            Resource  = "*"
            Condition = {
              Null = {
                "s3:x-amz-server-side-encryption" = "true"
              }
            }
          },
          {
            Sid      = "DenyUnencryptedEBS"
            Effect   = "Deny"
            Action   = "ec2:CreateVolume"
            Resource = "*"
            Condition = {
              Bool = {
                "ec2:Encrypted" = "false"
              }
            }
          }
        ]
      }
    }

    region_restriction = {
      name        = "RegionRestriction"
      description = "Restrict to allowed regions"
      targets     = [aws_organizations_organizational_unit.workloads.id]
      content = {
        Version = "2012-10-17"
        Statement = [
          {
            Sid    = "DenyOtherRegions"
            Effect = "Deny"
            NotAction = [
              "iam:*",
              "organizations:*",
              "route53:*",
              "budgets:*",
              "waf:*",
              "wafv2:*",
              "cloudfront:*",
              "globalaccelerator:*",
              "support:*",
              "health:*",
              "trustedadvisor:*"
            ]
            Resource = "*"
            Condition = {
              StringNotEquals = {
                "aws:RequestedRegion" = var.allowed_regions
              }
            }
          }
        ]
      }
    }
  }
}

resource "aws_organizations_policy" "scps" {
  for_each = local.scps

  name        = each.value.name
  description = each.value.description
  type        = "SERVICE_CONTROL_POLICY"
  content     = jsonencode(each.value.content)
}

resource "aws_organizations_policy_attachment" "scps" {
  for_each = local.scps

  policy_id = aws_organizations_policy.scps[each.key].id
  target_id = each.value.targets[0]
}
```

## Tagging Strategy

```hcl
# Common tags for all resources
locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
    Team        = var.team
    CostCenter  = var.cost_center
  }

  # Required tags for compliance
  required_tags = {
    DataClassification = var.data_classification # public/internal/confidential/restricted
    Compliance         = var.compliance_framework # gdpr/hipaa/pci/none
  }
}

# Tag policy for organization
resource "aws_organizations_policy" "required_tags" {
  name    = "RequiredTags"
  type    = "TAG_POLICY"

  content = jsonencode({
    tags = {
      Project = {
        tag_key = {
          @@assign = "Project"
        }
        enforced_for = {
          @@assign = ["ec2:instance", "rds:db", "s3:bucket"]
        }
      }
      Environment = {
        tag_key = {
          @@assign = "Environment"
        }
        tag_value = {
          @@assign = ["dev", "staging", "prod"]
        }
        enforced_for = {
          @@assign = ["ec2:instance", "rds:db", "s3:bucket"]
        }
      }
      CostCenter = {
        tag_key = {
          @@assign = "CostCenter"
        }
        enforced_for = {
          @@assign = ["ec2:instance", "rds:db"]
        }
      }
    }
  })
}
```
