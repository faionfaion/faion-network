# Terraform State Templates

Copy-paste ready configurations for common state management scenarios.

## Backend Configuration Templates

### AWS S3 Backend (Standard)

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "${COMPANY}-terraform-state"
    key            = "${ENV}/${COMPONENT}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### AWS S3 Backend (Multi-Account)

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "${COMPANY}-terraform-state"
    key            = "${ENV}/${COMPONENT}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
    kms_key_id     = "alias/terraform-state"
    role_arn       = "arn:aws:iam::${STATE_ACCOUNT_ID}:role/TerraformStateAccess"
  }
}
```

### GCS Backend (Standard)

```hcl
# backend.tf
terraform {
  backend "gcs" {
    bucket = "${COMPANY}-terraform-state"
    prefix = "${ENV}/${COMPONENT}"
  }
}
```

### Azure Blob Backend (Standard)

```hcl
# backend.tf
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "${COMPANY}tfstate"
    container_name       = "tfstate"
    key                  = "${ENV}/${COMPONENT}/terraform.tfstate"
    use_azuread_auth     = true
  }
}
```

### Terraform Cloud Backend

```hcl
# backend.tf
terraform {
  cloud {
    organization = "${ORGANIZATION}"

    workspaces {
      name = "${ENV}-${COMPONENT}"
    }
  }
}
```

## State Infrastructure Templates

### AWS State Infrastructure (Complete)

```hcl
# state-infrastructure/main.tf

# KMS Key for State Encryption
resource "aws_kms_key" "terraform_state" {
  description             = "KMS key for Terraform state encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Name      = "terraform-state-key"
    ManagedBy = "terraform"
  }
}

resource "aws_kms_alias" "terraform_state" {
  name          = "alias/terraform-state"
  target_key_id = aws_kms_key.terraform_state.key_id
}

# S3 Bucket for State
resource "aws_s3_bucket" "terraform_state" {
  bucket = "${var.company_name}-terraform-state"

  tags = {
    Name      = "terraform-state"
    ManagedBy = "terraform"
  }

  lifecycle {
    prevent_destroy = true
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
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.terraform_state.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    id     = "cleanup-old-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

# DynamoDB Table for Locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name      = "terraform-locks"
    ManagedBy = "terraform"
  }

  lifecycle {
    prevent_destroy = true
  }
}

# IAM Policy for State Access
resource "aws_iam_policy" "terraform_state_access" {
  name        = "TerraformStateAccess"
  description = "Policy for Terraform state access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3StateAccess"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.terraform_state.arn,
          "${aws_s3_bucket.terraform_state.arn}/*"
        ]
      },
      {
        Sid    = "DynamoDBLocking"
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:DeleteItem"
        ]
        Resource = aws_dynamodb_table.terraform_locks.arn
      },
      {
        Sid    = "KMSAccess"
        Effect = "Allow"
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ]
        Resource = aws_kms_key.terraform_state.arn
      }
    ]
  })
}

# Outputs
output "state_bucket_name" {
  value       = aws_s3_bucket.terraform_state.id
  description = "Name of the S3 bucket for Terraform state"
}

output "state_bucket_arn" {
  value       = aws_s3_bucket.terraform_state.arn
  description = "ARN of the S3 bucket for Terraform state"
}

output "lock_table_name" {
  value       = aws_dynamodb_table.terraform_locks.name
  description = "Name of the DynamoDB table for state locking"
}

output "state_policy_arn" {
  value       = aws_iam_policy.terraform_state_access.arn
  description = "ARN of the IAM policy for state access"
}
```

### GCP State Infrastructure

```hcl
# state-infrastructure/main.tf

resource "google_storage_bucket" "terraform_state" {
  name          = "${var.project_id}-terraform-state"
  location      = var.region
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      num_newer_versions = 5
    }
    action {
      type = "Delete"
    }
  }

  labels = {
    managed-by = "terraform"
  }
}

# Service Account for Terraform
resource "google_service_account" "terraform" {
  account_id   = "terraform"
  display_name = "Terraform Service Account"
}

resource "google_storage_bucket_iam_member" "terraform_state_access" {
  bucket = google_storage_bucket.terraform_state.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.terraform.email}"
}

output "state_bucket_name" {
  value       = google_storage_bucket.terraform_state.name
  description = "Name of the GCS bucket for Terraform state"
}

output "terraform_sa_email" {
  value       = google_service_account.terraform.email
  description = "Email of the Terraform service account"
}
```

## Import Block Templates

### Single Resource Import

```hcl
# imports.tf

import {
  to = aws_instance.${RESOURCE_NAME}
  id = "${INSTANCE_ID}"
}
```

### Multiple Resources Import

```hcl
# imports.tf

import {
  to = aws_vpc.main
  id = "vpc-12345678"
}

import {
  to = aws_subnet.public[0]
  id = "subnet-11111111"
}

import {
  to = aws_subnet.public[1]
  id = "subnet-22222222"
}

import {
  to = aws_security_group.web
  id = "sg-12345678"
}
```

## Moved Block Templates

### Rename Resource

```hcl
# moved.tf

moved {
  from = aws_instance.${OLD_NAME}
  to   = aws_instance.${NEW_NAME}
}
```

### Move to Module

```hcl
# moved.tf

moved {
  from = aws_instance.${RESOURCE_NAME}
  to   = module.${MODULE_NAME}.aws_instance.${RESOURCE_NAME}
}
```

### Rename Module

```hcl
# moved.tf

moved {
  from = module.${OLD_MODULE_NAME}
  to   = module.${NEW_MODULE_NAME}
}
```

## Remote State Data Source Template

```hcl
# data.tf

data "terraform_remote_state" "${STATE_NAME}" {
  backend = "s3"

  config = {
    bucket = "${COMPANY}-terraform-state"
    key    = "${ENV}/${COMPONENT}/terraform.tfstate"
    region = "us-east-1"
  }
}

# Usage example
locals {
  vpc_id     = data.terraform_remote_state.${STATE_NAME}.outputs.vpc_id
  subnet_ids = data.terraform_remote_state.${STATE_NAME}.outputs.subnet_ids
}
```

## CI/CD Backend Configuration Template

### GitHub Actions with OIDC

```hcl
# backend.tf

terraform {
  backend "s3" {
    bucket         = "${COMPANY}-terraform-state"
    key            = "${ENV}/${COMPONENT}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"

    # No static credentials - uses OIDC
  }
}
```

```yaml
# .github/workflows/terraform.yml (partial)
permissions:
  id-token: write
  contents: read

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${ACCOUNT_ID}:role/GitHubActionsRole
          aws-region: us-east-1

      - name: Terraform Init
        run: terraform init
        env:
          TF_IN_AUTOMATION: true
```

## Variables Template for Placeholders

```hcl
# variables.tf

variable "company_name" {
  description = "Company name for resource naming"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

variable "component" {
  description = "Component name (networking, compute, etc.)"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
```

---

*Terraform State Templates | Part of terraform-state methodology*
