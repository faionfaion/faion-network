# Terraform Templates

Starter templates for common Terraform project configurations.

---

## Basic Project Template

### Directory Structure

```
project/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   │   ├── main.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   └── prod/
│       ├── main.tf
│       ├── terraform.tfvars
│       └── backend.tf
├── modules/
│   ├── vpc/
│   ├── ecs/
│   └── rds/
├── .gitignore
├── .terraform.lock.hcl
└── README.md
```

### versions.tf

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}
```

### providers.tf

```hcl
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project
      Environment = var.environment
      ManagedBy   = "terraform"
      Repository  = var.repository_url
    }
  }

  # Assume role for cross-account access
  # assume_role {
  #   role_arn = "arn:aws:iam::${var.account_id}:role/TerraformRole"
  # }
}

# Secondary region provider
provider "aws" {
  alias  = "secondary"
  region = var.secondary_region

  default_tags {
    tags = {
      Project     = var.project
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
```

### variables.tf

```hcl
# ============================================================================
# Project Configuration
# ============================================================================

variable "project" {
  description = "Project name used for resource naming"
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,20}$", var.project))
    error_message = "Project name must be 3-21 lowercase alphanumeric characters, starting with a letter."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "repository_url" {
  description = "Repository URL for tagging"
  type        = string
  default     = ""
}

# ============================================================================
# AWS Configuration
# ============================================================================

variable "aws_region" {
  description = "Primary AWS region"
  type        = string
  default     = "us-east-1"
}

variable "secondary_region" {
  description = "Secondary AWS region for DR"
  type        = string
  default     = "us-west-2"
}

variable "account_id" {
  description = "AWS account ID"
  type        = string
  default     = ""
}

# ============================================================================
# Network Configuration
# ============================================================================

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be a valid CIDR block."
  }
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = []
}

# ============================================================================
# Feature Flags
# ============================================================================

variable "enable_nat_gateway" {
  description = "Enable NAT gateway for private subnets"
  type        = bool
  default     = true
}

variable "enable_vpn" {
  description = "Enable VPN connection"
  type        = bool
  default     = false
}

variable "enable_monitoring" {
  description = "Enable enhanced monitoring"
  type        = bool
  default     = true
}
```

### outputs.tf

```hcl
# ============================================================================
# VPC Outputs
# ============================================================================

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

# ============================================================================
# Application Outputs
# ============================================================================

output "app_url" {
  description = "Application URL"
  value       = "https://${module.app.alb_dns_name}"
}

output "app_security_group_id" {
  description = "Application security group ID"
  value       = module.app.security_group_id
}

# ============================================================================
# Database Outputs
# ============================================================================

output "database_endpoint" {
  description = "Database endpoint"
  value       = module.database.endpoint
  sensitive   = true
}

output "database_credentials_secret_arn" {
  description = "ARN of database credentials secret"
  value       = module.database.credentials_secret_arn
}
```

### locals.tf

```hcl
locals {
  # Naming prefix for all resources
  name_prefix = "${var.project}-${var.environment}"

  # Common tags applied to all resources
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
  }

  # Environment-specific configuration
  env_config = {
    dev = {
      instance_type    = "t3.micro"
      min_capacity     = 1
      max_capacity     = 2
      multi_az         = false
      deletion_protect = false
    }
    staging = {
      instance_type    = "t3.small"
      min_capacity     = 1
      max_capacity     = 3
      multi_az         = false
      deletion_protect = false
    }
    prod = {
      instance_type    = "t3.medium"
      min_capacity     = 2
      max_capacity     = 10
      multi_az         = true
      deletion_protect = true
    }
  }

  # Current environment config
  config = local.env_config[var.environment]

  # Availability zones
  azs = length(var.availability_zones) > 0 ? var.availability_zones : slice(
    data.aws_availability_zones.available.names, 0, 3
  )
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}
```

### main.tf

```hcl
# ============================================================================
# Network
# ============================================================================

module "vpc" {
  source = "../../modules/vpc"

  project     = var.project
  environment = var.environment

  vpc_cidr           = var.vpc_cidr
  availability_zones = local.azs

  enable_nat_gateway = var.enable_nat_gateway
  single_nat_gateway = var.environment != "prod"

  tags = local.common_tags
}

# ============================================================================
# Database
# ============================================================================

module "database" {
  source = "../../modules/rds"

  project     = var.project
  environment = var.environment

  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.private_subnet_ids
  security_group_ids = [module.vpc.database_security_group_id]

  instance_class = local.config.instance_type
  multi_az       = local.config.multi_az

  deletion_protection = local.config.deletion_protect

  tags = local.common_tags
}

# ============================================================================
# Application
# ============================================================================

module "app" {
  source = "../../modules/ecs"

  project     = var.project
  environment = var.environment

  vpc_id             = module.vpc.vpc_id
  public_subnet_ids  = module.vpc.public_subnet_ids
  private_subnet_ids = module.vpc.private_subnet_ids

  min_capacity = local.config.min_capacity
  max_capacity = local.config.max_capacity

  database_url_secret_arn = module.database.credentials_secret_arn

  tags = local.common_tags

  depends_on = [module.vpc, module.database]
}
```

### backend.tf (environment-specific)

```hcl
# environments/dev/backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "project/dev/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### terraform.tfvars (environment-specific)

```hcl
# environments/dev/terraform.tfvars
project        = "myapp"
environment    = "dev"
aws_region     = "us-east-1"
vpc_cidr       = "10.0.0.0/16"
repository_url = "https://github.com/company/myapp"

enable_nat_gateway = true
enable_monitoring  = false
```

### .gitignore

```gitignore
# Terraform
.terraform/
*.tfstate
*.tfstate.*
crash.log
crash.*.log
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Sensitive files
*.tfvars
!*.tfvars.example
.env
*.pem
*.key

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Keep lock file
!.terraform.lock.hcl
```

---

## Module Template

### modules/vpc/main.tf

```hcl
# ============================================================================
# VPC
# ============================================================================

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${var.project}-${var.environment}-vpc"
  })
}

# ============================================================================
# Internet Gateway
# ============================================================================

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(var.tags, {
    Name = "${var.project}-${var.environment}-igw"
  })
}

# ============================================================================
# Subnets
# ============================================================================

resource "aws_subnet" "public" {
  count = length(var.availability_zones)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "${var.project}-${var.environment}-public-${count.index + 1}"
    Tier = "public"
  })
}

resource "aws_subnet" "private" {
  count = length(var.availability_zones)

  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone = var.availability_zones[count.index]

  tags = merge(var.tags, {
    Name = "${var.project}-${var.environment}-private-${count.index + 1}"
    Tier = "private"
  })
}

# ... (NAT gateway, route tables, etc.)
```

### modules/vpc/variables.tf

```hcl
variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "enable_nat_gateway" {
  description = "Enable NAT gateway"
  type        = bool
  default     = true
}

variable "single_nat_gateway" {
  description = "Use single NAT gateway for all AZs"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Additional tags"
  type        = map(string)
  default     = {}
}
```

### modules/vpc/outputs.tf

```hcl
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "VPC CIDR block"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "internet_gateway_id" {
  description = "Internet gateway ID"
  value       = aws_internet_gateway.main.id
}
```

### modules/vpc/versions.tf

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}
```

### modules/vpc/README.md

```markdown
# VPC Module

Creates a VPC with public and private subnets across multiple availability zones.

## Usage

```hcl
module "vpc" {
  source = "./modules/vpc"

  project     = "myapp"
  environment = "prod"

  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

  enable_nat_gateway = true
  single_nat_gateway = false

  tags = {
    Team = "platform"
  }
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| project | Project name | `string` | - | yes |
| environment | Environment name | `string` | - | yes |
| vpc_cidr | VPC CIDR block | `string` | - | yes |
| availability_zones | List of AZs | `list(string)` | - | yes |
| enable_nat_gateway | Enable NAT gateway | `bool` | `true` | no |
| single_nat_gateway | Use single NAT | `bool` | `false` | no |
| tags | Additional tags | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| vpc_id | VPC ID |
| vpc_cidr | VPC CIDR block |
| public_subnet_ids | Public subnet IDs |
| private_subnet_ids | Private subnet IDs |
```

---

## CI/CD Template (GitHub Actions)

### .github/workflows/terraform.yml

```yaml
name: Terraform

on:
  push:
    branches: [main]
    paths:
      - 'terraform/**'
      - '.github/workflows/terraform.yml'
  pull_request:
    branches: [main]
    paths:
      - 'terraform/**'
      - '.github/workflows/terraform.yml'

permissions:
  id-token: write
  contents: read
  pull-requests: write

env:
  TF_VERSION: '1.6.0'
  AWS_REGION: 'us-east-1'

jobs:
  validate:
    name: Validate
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Format
        run: terraform fmt -check -recursive
        working-directory: terraform

      - name: Terraform Init
        run: terraform init -backend=false
        working-directory: terraform/environments/dev

      - name: Terraform Validate
        run: terraform validate
        working-directory: terraform/environments/dev

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: tfsec
        uses: aquasecurity/tfsec-action@v1.0.0
        with:
          working_directory: terraform

      - name: Checkov
        uses: bridgecrewio/checkov-action@v12
        with:
          directory: terraform
          framework: terraform

  plan:
    name: Plan (${{ matrix.environment }})
    needs: [validate, security]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
    environment: ${{ matrix.environment }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/GitHubActionsRole
          aws-region: ${{ env.AWS_REGION }}

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Init
        run: terraform init
        working-directory: terraform/environments/${{ matrix.environment }}

      - name: Terraform Plan
        id: plan
        run: terraform plan -no-color -out=tfplan
        working-directory: terraform/environments/${{ matrix.environment }}

      - name: Upload Plan
        uses: actions/upload-artifact@v4
        with:
          name: tfplan-${{ matrix.environment }}
          path: terraform/environments/${{ matrix.environment }}/tfplan

  apply:
    name: Apply (${{ matrix.environment }})
    needs: [plan]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev]  # Add staging, prod with manual approval
    environment: ${{ matrix.environment }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/GitHubActionsRole
          aws-region: ${{ env.AWS_REGION }}

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Download Plan
        uses: actions/download-artifact@v4
        with:
          name: tfplan-${{ matrix.environment }}
          path: terraform/environments/${{ matrix.environment }}

      - name: Terraform Init
        run: terraform init
        working-directory: terraform/environments/${{ matrix.environment }}

      - name: Terraform Apply
        run: terraform apply -auto-approve tfplan
        working-directory: terraform/environments/${{ matrix.environment }}
```

---

## State Backend Bootstrap Template

### bootstrap/main.tf

```hcl
# Bootstrap resources for Terraform state backend
# Run this once to create S3 bucket and DynamoDB table

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default = "us-east-1"
}

variable "bucket_name" {
  description = "S3 bucket name for Terraform state"
  type        = string
}

variable "dynamodb_table_name" {
  description = "DynamoDB table name for state locking"
  type        = string
  default     = "terraform-locks"
}

# S3 Bucket
resource "aws_s3_bucket" "terraform_state" {
  bucket = var.bucket_name

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    Name      = "Terraform State"
    ManagedBy = "terraform-bootstrap"
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# DynamoDB Table for locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name      = "Terraform Locks"
    ManagedBy = "terraform-bootstrap"
  }
}

output "bucket_name" {
  value = aws_s3_bucket.terraform_state.id
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.terraform_locks.name
}

output "bucket_arn" {
  value = aws_s3_bucket.terraform_state.arn
}
```
