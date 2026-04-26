# IaC Patterns Examples

## Module Patterns

### 1. Base Module Pattern

A focused module that manages a single resource type with sensible defaults.

```hcl
# modules/s3-bucket/main.tf
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name

  tags = merge(var.tags, {
    Name = var.bucket_name
  })
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration {
    status = var.versioning_enabled ? "Enabled" : "Disabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = var.kms_key_arn != null ? "aws:kms" : "AES256"
      kms_master_key_id = var.kms_key_arn
    }
    bucket_key_enabled = var.kms_key_arn != null
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.this.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

```hcl
# modules/s3-bucket/variables.tf
variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$", var.bucket_name))
    error_message = "Bucket name must be valid S3 bucket name."
  }
}

variable "versioning_enabled" {
  description = "Enable bucket versioning"
  type        = bool
  default     = true
}

variable "kms_key_arn" {
  description = "KMS key ARN for encryption. If null, uses AES256"
  type        = string
  default     = null
}

variable "tags" {
  description = "Tags to apply to bucket"
  type        = map(string)
  default     = {}
}
```

```hcl
# modules/s3-bucket/outputs.tf
output "bucket_id" {
  description = "The name of the bucket"
  value       = aws_s3_bucket.this.id
}

output "bucket_arn" {
  description = "The ARN of the bucket"
  value       = aws_s3_bucket.this.arn
}

output "bucket_domain_name" {
  description = "The bucket domain name"
  value       = aws_s3_bucket.this.bucket_domain_name
}
```

### 2. Wrapper Module Pattern

Wraps community/base modules with organization-specific defaults and policies.

```hcl
# modules/company-rds/main.tf
# Wrapper module enforcing company RDS standards

module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "${var.name_prefix}-${var.db_name}"

  engine               = var.engine
  engine_version       = var.engine_version
  family               = var.family
  major_engine_version = var.major_engine_version
  instance_class       = var.instance_class

  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.allocated_storage * 2  # Company policy: autoscale up to 2x

  db_name  = var.db_name
  username = var.username
  port     = var.port

  # Company security requirements (non-negotiable)
  storage_encrypted = true                           # Always encrypted
  kms_key_id        = var.kms_key_arn

  multi_az               = var.environment == "prod" ? true : var.multi_az
  deletion_protection    = var.environment == "prod" ? true : var.deletion_protection
  skip_final_snapshot    = var.environment == "prod" ? false : var.skip_final_snapshot
  backup_retention_period = var.environment == "prod" ? 30 : max(var.backup_retention_period, 7)

  # Company network requirements
  vpc_security_group_ids = var.security_group_ids
  subnet_ids             = var.subnet_ids
  publicly_accessible    = false  # Never public (company policy)

  # Performance insights (enabled for prod)
  performance_insights_enabled = var.environment == "prod" ? true : var.performance_insights_enabled

  # Company tagging standard
  tags = merge(var.tags, {
    Environment = var.environment
    ManagedBy   = "terraform"
    Module      = "company-rds"
  })
}
```

### 3. Facade Module Pattern

Provides simplified API hiding complex orchestration of multiple modules.

```hcl
# modules/web-application/main.tf
# Facade: deploys complete web app stack with simple inputs

locals {
  name_prefix = "${var.project}-${var.environment}"
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# Internal module composition
module "vpc" {
  source = "../vpc"

  name_prefix        = local.name_prefix
  cidr               = var.vpc_cidr
  availability_zones = var.availability_zones
  tags               = local.common_tags
}

module "alb" {
  source = "../alb"

  name_prefix       = local.name_prefix
  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  certificate_arn   = var.certificate_arn
  tags              = local.common_tags
}

module "ecs" {
  source = "../ecs-service"

  name_prefix         = local.name_prefix
  vpc_id              = module.vpc.vpc_id
  private_subnet_ids  = module.vpc.private_subnet_ids
  alb_target_group_arn = module.alb.target_group_arn

  container_image     = var.container_image
  container_port      = var.container_port
  desired_count       = var.desired_count
  cpu                 = var.cpu
  memory              = var.memory

  environment_variables = var.environment_variables
  secrets              = var.secrets

  tags = local.common_tags
}

module "rds" {
  count  = var.create_database ? 1 : 0
  source = "../company-rds"

  name_prefix   = local.name_prefix
  db_name       = var.db_name
  environment   = var.environment
  instance_class = var.db_instance_class

  subnet_ids         = module.vpc.database_subnet_ids
  security_group_ids = [module.ecs.security_group_id]

  tags = local.common_tags
}
```

```hcl
# modules/web-application/variables.tf
# Simplified interface - consumers only need to know high-level config

variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "container_image" {
  description = "Docker image for the application"
  type        = string
}

variable "container_port" {
  description = "Port the container listens on"
  type        = number
  default     = 8080
}

variable "desired_count" {
  description = "Number of container instances"
  type        = number
  default     = 2
}

# Sensible defaults hide complexity
variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of AZs"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}
```

### 4. Factory Module Pattern

Creates multiple similar resources from configuration objects.

```hcl
# modules/s3-buckets-factory/main.tf

variable "buckets" {
  description = "Map of bucket configurations"
  type = map(object({
    versioning = optional(bool, true)
    lifecycle_rules = optional(list(object({
      id      = string
      enabled = bool
      prefix  = optional(string, "")
      expiration_days = optional(number)
      transition = optional(object({
        days          = number
        storage_class = string
      }))
    })), [])
    cors_rules = optional(list(object({
      allowed_headers = list(string)
      allowed_methods = list(string)
      allowed_origins = list(string)
      max_age_seconds = optional(number, 3600)
    })), [])
  }))
}

resource "aws_s3_bucket" "buckets" {
  for_each = var.buckets

  bucket = "${var.name_prefix}-${each.key}"

  tags = merge(var.tags, {
    Name = "${var.name_prefix}-${each.key}"
  })
}

resource "aws_s3_bucket_versioning" "buckets" {
  for_each = var.buckets

  bucket = aws_s3_bucket.buckets[each.key].id
  versioning_configuration {
    status = each.value.versioning ? "Enabled" : "Disabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "buckets" {
  for_each = { for k, v in var.buckets : k => v if length(v.lifecycle_rules) > 0 }

  bucket = aws_s3_bucket.buckets[each.key].id

  dynamic "rule" {
    for_each = each.value.lifecycle_rules
    content {
      id     = rule.value.id
      status = rule.value.enabled ? "Enabled" : "Disabled"

      filter {
        prefix = rule.value.prefix
      }

      dynamic "expiration" {
        for_each = rule.value.expiration_days != null ? [1] : []
        content {
          days = rule.value.expiration_days
        }
      }

      dynamic "transition" {
        for_each = rule.value.transition != null ? [rule.value.transition] : []
        content {
          days          = transition.value.days
          storage_class = transition.value.storage_class
        }
      }
    }
  }
}
```

Usage:

```hcl
module "app_buckets" {
  source = "./modules/s3-buckets-factory"

  name_prefix = "myapp-prod"

  buckets = {
    uploads = {
      versioning = true
      lifecycle_rules = [{
        id      = "archive-old"
        enabled = true
        transition = {
          days          = 90
          storage_class = "GLACIER"
        }
      }]
    }
    logs = {
      versioning = false
      lifecycle_rules = [{
        id              = "expire-old"
        enabled         = true
        expiration_days = 30
      }]
    }
    static-assets = {
      versioning = true
      cors_rules = [{
        allowed_headers = ["*"]
        allowed_methods = ["GET", "HEAD"]
        allowed_origins = ["https://myapp.com"]
      }]
    }
  }

  tags = local.common_tags
}
```

## DRY Patterns

### Locals for Computed Values

```hcl
locals {
  # Naming convention
  name_prefix = "${var.project}-${var.environment}"

  # Common tags applied everywhere
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
    CostCenter  = var.cost_center
  }

  # Computed CIDR blocks
  public_cidrs   = [for i in range(3) : cidrsubnet(var.vpc_cidr, 4, i)]
  private_cidrs  = [for i in range(3) : cidrsubnet(var.vpc_cidr, 4, i + 3)]
  database_cidrs = [for i in range(3) : cidrsubnet(var.vpc_cidr, 4, i + 6)]

  # Environment-specific configuration
  is_production = var.environment == "prod"

  instance_class = local.is_production ? "db.r6g.xlarge" : "db.t4g.medium"
  multi_az       = local.is_production ? true : false

  # Merge user-provided values with defaults
  final_config = merge(local.default_config, var.custom_config)
}
```

### Dynamic Blocks for Repeated Structures

```hcl
variable "ingress_rules" {
  description = "List of ingress rules"
  type = list(object({
    port        = number
    protocol    = optional(string, "tcp")
    cidr_blocks = list(string)
    description = optional(string, "")
  }))
  default = []
}

resource "aws_security_group" "app" {
  name_prefix = "${local.name_prefix}-app-"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags

  lifecycle {
    create_before_destroy = true
  }
}
```

## Testing Patterns

### Native Terraform Test

```hcl
# tests/s3_bucket.tftest.hcl

variables {
  bucket_name = "test-bucket-example"
  tags = {
    Environment = "test"
  }
}

run "bucket_creates_successfully" {
  command = plan

  assert {
    condition     = aws_s3_bucket.this.bucket == "test-bucket-example"
    error_message = "Bucket name does not match expected value"
  }

  assert {
    condition     = aws_s3_bucket_versioning.this.versioning_configuration[0].status == "Enabled"
    error_message = "Versioning should be enabled by default"
  }
}

run "bucket_blocks_public_access" {
  command = plan

  assert {
    condition     = aws_s3_bucket_public_access_block.this.block_public_acls == true
    error_message = "Public ACLs should be blocked"
  }

  assert {
    condition     = aws_s3_bucket_public_access_block.this.block_public_policy == true
    error_message = "Public policy should be blocked"
  }
}
```

### Terratest Example

```go
// tests/s3_bucket_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/gruntwork-io/terratest/modules/aws"
    "github.com/stretchr/testify/assert"
)

func TestS3BucketModule(t *testing.T) {
    t.Parallel()

    awsRegion := "us-east-1"
    bucketName := fmt.Sprintf("test-bucket-%s", random.UniqueId())

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../modules/s3-bucket",
        Vars: map[string]interface{}{
            "bucket_name":        bucketName,
            "versioning_enabled": true,
        },
        EnvVars: map[string]string{
            "AWS_DEFAULT_REGION": awsRegion,
        },
    })

    defer terraform.Destroy(t, terraformOptions)

    terraform.InitAndApply(t, terraformOptions)

    // Verify bucket exists
    bucketId := terraform.Output(t, terraformOptions, "bucket_id")
    assert.Equal(t, bucketName, bucketId)

    // Verify encryption
    encryption := aws.GetS3BucketEncryption(t, awsRegion, bucketName)
    assert.Equal(t, "AES256", encryption)

    // Verify versioning
    versioning := aws.GetS3BucketVersioning(t, awsRegion, bucketName)
    assert.Equal(t, "Enabled", versioning)
}
```

## Composition Patterns

### Environment Composition with Terragrunt

```hcl
# environments/prod/terragrunt.hcl

include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "${get_repo_root()}/modules/web-application"
}

inputs = {
  project     = "myapp"
  environment = "prod"

  container_image = "myapp:${get_env("IMAGE_TAG", "latest")}"
  desired_count   = 4
  cpu             = 1024
  memory          = 2048

  create_database  = true
  db_instance_class = "db.r6g.xlarge"
}
```

```hcl
# terragrunt.hcl (root)

locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))

  account_id = local.account_vars.locals.account_id
  aws_region = local.region_vars.locals.aws_region
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.aws_region}"

  default_tags {
    tags = {
      ManagedBy = "terragrunt"
    }
  }
}
EOF
}

remote_state {
  backend = "s3"
  config = {
    bucket         = "terraform-state-${local.account_id}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = local.aws_region
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

---

*IaC Patterns Examples | faion-infrastructure-engineer*
