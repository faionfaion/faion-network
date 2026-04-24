# AWS Architecture Templates

## Project Structure

```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
├── modules/
│   ├── networking/
│   ├── compute/
│   ├── database/
│   └── monitoring/
├── shared/
│   ├── backend.tf
│   └── providers.tf
└── README.md
```

---

## Backend Configuration

```hcl
# backend.tf
terraform {
  required_version = ">= 1.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "myproject-terraform-state"
    key            = "environments/${var.environment}/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Project     = var.project
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
```

---

## Variables Template

```hcl
# variables.tf
variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "domain" {
  description = "Domain name"
  type        = string
}

# Network
variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
}

# Database
variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.serverless"
}

variable "db_min_capacity" {
  description = "Aurora Serverless v2 min ACU"
  type        = number
  default     = 0.5
}

variable "db_max_capacity" {
  description = "Aurora Serverless v2 max ACU"
  type        = number
  default     = 16
}
```

---

## Environment Variables (tfvars)

```hcl
# environments/dev/terraform.tfvars
project     = "myproject"
environment = "dev"
region      = "eu-central-1"
domain      = "dev.example.com"

# Cost optimization for dev
db_min_capacity = 0.5
db_max_capacity = 2
```

```hcl
# environments/prod/terraform.tfvars
project     = "myproject"
environment = "prod"
region      = "eu-central-1"
domain      = "example.com"

# Production capacity
db_min_capacity = 2
db_max_capacity = 32
```

---

## Three-Tier Architecture Template

```hcl
# main.tf - Three-tier architecture
locals {
  name = "${var.project}-${var.environment}"
}

# Networking
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = local.name
  cidr = var.vpc_cidr

  azs              = var.availability_zones
  public_subnets   = [for i, az in var.availability_zones : cidrsubnet(var.vpc_cidr, 8, i)]
  private_subnets  = [for i, az in var.availability_zones : cidrsubnet(var.vpc_cidr, 8, i + 10)]
  database_subnets = [for i, az in var.availability_zones : cidrsubnet(var.vpc_cidr, 8, i + 20)]

  enable_nat_gateway     = true
  single_nat_gateway     = var.environment != "prod"
  one_nat_gateway_per_az = var.environment == "prod"

  enable_dns_hostnames = true
  enable_dns_support   = true
  enable_flow_log      = true
}

# Load Balancer
module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 9.0"

  name    = local.name
  vpc_id  = module.vpc.vpc_id
  subnets = module.vpc.public_subnets

  # ... (see examples.md for full config)
}

# Application (ECS/EKS)
module "ecs" {
  source  = "terraform-aws-modules/ecs/aws"
  version = "~> 5.0"

  cluster_name = local.name

  fargate_capacity_providers = {
    FARGATE = {
      default_capacity_provider_strategy = {
        weight = 50
        base   = 20
      }
    }
    FARGATE_SPOT = {
      default_capacity_provider_strategy = {
        weight = 50
      }
    }
  }
}

# Database
module "aurora" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "~> 9.0"

  name           = local.name
  engine         = "aurora-postgresql"
  engine_version = "16.4"
  engine_mode    = "provisioned"

  vpc_id               = module.vpc.vpc_id
  db_subnet_group_name = module.vpc.database_subnet_group_name

  serverlessv2_scaling_configuration = {
    min_capacity = var.db_min_capacity
    max_capacity = var.db_max_capacity
  }

  instance_class = var.db_instance_class
  instances = {
    writer = {}
    reader = var.environment == "prod" ? {} : null
  }

  storage_encrypted   = true
  deletion_protection = var.environment == "prod"
}
```

---

## Serverless API Template

```hcl
# main.tf - Serverless API
locals {
  name = "${var.project}-${var.environment}"
}

# API Gateway
module "api_gateway" {
  source  = "terraform-aws-modules/apigateway-v2/aws"
  version = "~> 5.0"

  name          = local.name
  protocol_type = "HTTP"

  cors_configuration = {
    allow_headers = ["*"]
    allow_methods = ["*"]
    allow_origins = ["https://${var.domain}"]
  }

  domain_name                 = "api.${var.domain}"
  domain_name_certificate_arn = module.acm.acm_certificate_arn

  integrations = {
    "ANY /{proxy+}" = {
      lambda_arn             = module.lambda.lambda_function_arn
      payload_format_version = "2.0"
    }
  }
}

# Lambda
module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 7.0"

  function_name = local.name
  handler       = "main.handler"
  runtime       = "python3.12"
  architectures = ["arm64"]

  source_path = "${path.module}/../src"

  memory_size = 256
  timeout     = 30

  tracing_mode = "Active"

  environment_variables = {
    ENVIRONMENT    = var.environment
    TABLE_NAME     = module.dynamodb.dynamodb_table_id
    LOG_LEVEL      = var.environment == "prod" ? "INFO" : "DEBUG"
  }
}

# DynamoDB
module "dynamodb" {
  source  = "terraform-aws-modules/dynamodb-table/aws"
  version = "~> 4.0"

  name         = local.name
  hash_key     = "pk"
  range_key    = "sk"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "pk", type = "S" },
    { name = "sk", type = "S" }
  ]

  point_in_time_recovery_enabled = true
  server_side_encryption_enabled = true
}
```

---

## KMS Keys Template

```hcl
# kms.tf
resource "aws_kms_key" "main" {
  description             = "${local.name} encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      }
    ]
  })
}

resource "aws_kms_alias" "main" {
  name          = "alias/${local.name}"
  target_key_id = aws_kms_key.main.key_id
}

# Per-service KMS keys
resource "aws_kms_key" "rds" {
  description             = "${local.name} RDS encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}

resource "aws_kms_key" "secrets" {
  description             = "${local.name} Secrets Manager"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}
```

---

## Security Groups Template

```hcl
# security_groups.tf
module "alb_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name        = "${local.name}-alb"
  description = "ALB security group"
  vpc_id      = module.vpc.vpc_id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["http-80-tcp", "https-443-tcp"]

  egress_rules = ["all-all"]
}

module "app_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name        = "${local.name}-app"
  description = "Application security group"
  vpc_id      = module.vpc.vpc_id

  ingress_with_source_security_group_id = [
    {
      from_port                = 8000
      to_port                  = 8000
      protocol                 = "tcp"
      source_security_group_id = module.alb_sg.security_group_id
    }
  ]

  egress_rules = ["all-all"]
}

module "db_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name        = "${local.name}-db"
  description = "Database security group"
  vpc_id      = module.vpc.vpc_id

  ingress_with_source_security_group_id = [
    {
      from_port                = 5432
      to_port                  = 5432
      protocol                 = "tcp"
      source_security_group_id = module.app_sg.security_group_id
    }
  ]

  egress_rules = []  # No egress needed
}
```

---

## Outputs Template

```hcl
# outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "alb_dns_name" {
  description = "ALB DNS name"
  value       = module.alb.dns_name
}

output "api_endpoint" {
  description = "API Gateway endpoint"
  value       = module.api_gateway.api_endpoint
}

output "database_endpoint" {
  description = "Database endpoint"
  value       = module.aurora.cluster_endpoint
  sensitive   = true
}

output "cloudfront_domain" {
  description = "CloudFront domain"
  value       = module.cloudfront.cloudfront_distribution_domain_name
}
```

---

## GitHub Actions Workflow

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [main]
    paths: ['infrastructure/**']
  pull_request:
    branches: [main]
    paths: ['infrastructure/**']

env:
  TF_VERSION: "1.7"
  AWS_REGION: "eu-central-1"

jobs:
  plan:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]

    permissions:
      id-token: write
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Init
        working-directory: infrastructure/environments/${{ matrix.environment }}
        run: terraform init

      - name: Terraform Plan
        working-directory: infrastructure/environments/${{ matrix.environment }}
        run: terraform plan -out=tfplan

      - name: Upload Plan
        uses: actions/upload-artifact@v4
        with:
          name: tfplan-${{ matrix.environment }}
          path: infrastructure/environments/${{ matrix.environment }}/tfplan

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    strategy:
      matrix:
        environment: [dev, staging, prod]
      max-parallel: 1

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Download Plan
        uses: actions/download-artifact@v4
        with:
          name: tfplan-${{ matrix.environment }}
          path: infrastructure/environments/${{ matrix.environment }}

      - name: Terraform Init
        working-directory: infrastructure/environments/${{ matrix.environment }}
        run: terraform init

      - name: Terraform Apply
        working-directory: infrastructure/environments/${{ matrix.environment }}
        run: terraform apply -auto-approve tfplan
```

---

## Cost Estimation Tags

```hcl
# tags.tf
locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
    CostCenter  = var.cost_center
    Owner       = var.owner
  }
}

# Apply to all resources via provider default_tags
provider "aws" {
  default_tags {
    tags = local.common_tags
  }
}
```
