# IaC Patterns Templates

## Module Templates

### Basic Module Structure

```
modules/{module-name}/
├── main.tf           # Primary resource definitions
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── versions.tf       # Provider requirements
├── locals.tf         # Local values (optional)
├── data.tf           # Data sources (optional)
├── README.md         # Documentation
├── CHANGELOG.md      # Version history
├── examples/
│   └── basic/
│       ├── main.tf
│       └── outputs.tf
└── tests/
    └── module.tftest.hcl
```

### versions.tf Template

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}
```

### variables.tf Template

```hcl
# Required variables
variable "name" {
  description = "Name for the resource"
  type        = string

  validation {
    condition     = length(var.name) > 0 && length(var.name) <= 64
    error_message = "Name must be between 1 and 64 characters."
  }
}

# Optional with defaults
variable "environment" {
  description = "Environment name (dev/staging/prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# Complex type with defaults
variable "config" {
  description = "Configuration object"
  type = object({
    enabled     = optional(bool, true)
    replicas    = optional(number, 1)
    settings    = optional(map(string), {})
  })
  default = {}
}

# Sensitive variable
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

# Tags variable (standard pattern)
variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
```

### outputs.tf Template

```hcl
output "id" {
  description = "The ID of the resource"
  value       = aws_resource.main.id
}

output "arn" {
  description = "The ARN of the resource"
  value       = aws_resource.main.arn
}

output "endpoint" {
  description = "The endpoint URL"
  value       = aws_resource.main.endpoint
}

# Sensitive output
output "connection_string" {
  description = "Database connection string"
  value       = "postgresql://${var.username}:${var.password}@${aws_db_instance.main.endpoint}/${var.db_name}"
  sensitive   = true
}
```

### locals.tf Template

```hcl
locals {
  # Naming convention
  name_prefix = "${var.project}-${var.environment}"

  # Common tags
  common_tags = merge(var.tags, {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
    Module      = "module-name"
  })

  # Environment-specific logic
  is_production = var.environment == "prod"

  # Computed values
  replica_count = local.is_production ? max(var.replicas, 2) : var.replicas

  # Conditional features
  enable_monitoring = local.is_production
  enable_backups    = local.is_production || var.enable_backups
}
```

### README.md Template

```markdown
# Module Name

Brief description of what this module creates.

## Usage

```hcl
module "example" {
  source = "path/to/module"

  name        = "my-resource"
  environment = "prod"

  tags = {
    Team = "platform"
  }
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.5.0 |
| aws | >= 5.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| name | Name for the resource | `string` | n/a | yes |
| environment | Environment (dev/staging/prod) | `string` | `"dev"` | no |
| tags | Tags to apply | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| id | The ID of the resource |
| arn | The ARN of the resource |

## Examples

- [Basic](./examples/basic) - Minimal configuration
- [Complete](./examples/complete) - Full configuration with all options
```

## Environment Templates

### Root Module Structure

```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── backend.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
├── modules/
│   ├── networking/
│   ├── compute/
│   └── database/
└── shared/
    └── providers.tf
```

### backend.tf Template (AWS)

```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "project/environment/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"

    # Assume role for state access
    role_arn = "arn:aws:iam::ACCOUNT_ID:role/TerraformStateAccess"
  }
}
```

### terraform.tfvars Template

```hcl
# Environment: production
project     = "myapp"
environment = "prod"
region      = "us-east-1"

# Networking
vpc_cidr           = "10.0.0.0/16"
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

# Compute
instance_type = "m6i.xlarge"
min_capacity  = 2
max_capacity  = 10

# Database
db_instance_class = "db.r6g.xlarge"
db_allocated_storage = 100

# Feature flags
enable_monitoring = true
enable_backups    = true

# Tags
tags = {
  CostCenter = "engineering"
  Team       = "platform"
}
```

## Testing Templates

### terraform test Template

```hcl
# tests/module.tftest.hcl

# Default variable values for tests
variables {
  name        = "test-resource"
  environment = "dev"
  tags = {
    Test = "true"
  }
}

# Plan-only test (fast, no resources)
run "validates_plan" {
  command = plan

  assert {
    condition     = aws_resource.main.name == "test-resource"
    error_message = "Resource name should match input"
  }
}

# Apply test with mock provider
run "creates_resource_with_mocks" {
  command = apply

  providers = {
    aws = aws.mock
  }

  assert {
    condition     = output.id != ""
    error_message = "Should output resource ID"
  }
}

# Test input validation
run "rejects_invalid_environment" {
  command = plan

  variables {
    environment = "invalid"
  }

  expect_failures = [
    var.environment,
  ]
}
```

### Terratest Template

```go
// tests/module_test.go
package test

import (
    "fmt"
    "testing"
    "time"

    "github.com/gruntwork-io/terratest/modules/random"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestModuleBasic(t *testing.T) {
    t.Parallel()

    uniqueID := random.UniqueId()
    name := fmt.Sprintf("test-%s", uniqueID)

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../",
        Vars: map[string]interface{}{
            "name":        name,
            "environment": "dev",
        },
        EnvVars: map[string]string{
            "AWS_DEFAULT_REGION": "us-east-1",
        },
        // Retry settings for flaky operations
        MaxRetries:         3,
        TimeBetweenRetries: 5 * time.Second,
    })

    // Cleanup resources after test
    defer terraform.Destroy(t, terraformOptions)

    // Deploy infrastructure
    terraform.InitAndApply(t, terraformOptions)

    // Validate outputs
    resourceID := terraform.Output(t, terraformOptions, "id")
    require.NotEmpty(t, resourceID, "Resource ID should not be empty")

    resourceArn := terraform.Output(t, terraformOptions, "arn")
    assert.Contains(t, resourceArn, name, "ARN should contain resource name")
}

func TestModuleProduction(t *testing.T) {
    t.Parallel()

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../",
        Vars: map[string]interface{}{
            "name":        fmt.Sprintf("test-prod-%s", random.UniqueId()),
            "environment": "prod",
        },
    })

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    // Production-specific assertions
    // Verify multi-AZ, encryption, etc.
}
```

## CI/CD Templates

### GitHub Actions Workflow

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  pull_request:
    paths:
      - 'infrastructure/**'
  push:
    branches:
      - main
    paths:
      - 'infrastructure/**'

permissions:
  id-token: write
  contents: read
  pull-requests: write

env:
  TF_VERSION: "1.6.0"
  AWS_REGION: "us-east-1"

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Format
        run: terraform fmt -check -recursive
        working-directory: infrastructure

      - name: Terraform Init
        run: terraform init -backend=false
        working-directory: infrastructure/environments/dev

      - name: Terraform Validate
        run: terraform validate
        working-directory: infrastructure/environments/dev

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: terraform-linters/setup-tflint@v4

      - name: TFLint
        run: |
          tflint --init
          tflint --recursive

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Checkov
        uses: bridgecrewio/checkov-action@v12
        with:
          directory: infrastructure
          framework: terraform
          output_format: sarif

  plan:
    needs: [validate, lint, security]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/TerraformCI
          aws-region: ${{ env.AWS_REGION }}

      - name: Terraform Init
        run: terraform init
        working-directory: infrastructure/environments/${{ matrix.environment }}

      - name: Terraform Plan
        id: plan
        run: terraform plan -no-color -out=tfplan
        working-directory: infrastructure/environments/${{ matrix.environment }}

      - name: Comment Plan
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const output = `#### Terraform Plan - ${{ matrix.environment }}
            \`\`\`
            ${{ steps.plan.outputs.stdout }}
            \`\`\``;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            })

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/TerraformCI
          aws-region: ${{ env.AWS_REGION }}

      - name: Terraform Apply
        run: |
          terraform init
          terraform apply -auto-approve
        working-directory: infrastructure/environments/prod
```

### Makefile Template

```makefile
# Makefile for Terraform operations

ENV ?= dev
MODULE ?= .

.PHONY: init plan apply destroy fmt validate lint test

init:
	cd environments/$(ENV) && terraform init

plan:
	cd environments/$(ENV) && terraform plan

apply:
	cd environments/$(ENV) && terraform apply

destroy:
	cd environments/$(ENV) && terraform destroy

fmt:
	terraform fmt -recursive

validate:
	@for env in environments/*/; do \
		echo "Validating $$env..."; \
		cd $$env && terraform init -backend=false && terraform validate && cd ../..; \
	done

lint:
	tflint --recursive

security:
	checkov -d . --framework terraform

test:
	cd modules/$(MODULE)/tests && terraform test

test-all:
	@for module in modules/*/; do \
		if [ -d "$$module/tests" ]; then \
			echo "Testing $$module..."; \
			cd $$module/tests && terraform test && cd ../../..; \
		fi \
	done

docs:
	@for module in modules/*/; do \
		terraform-docs markdown $$module > $$module/README.md; \
	done
```

## Terragrunt Templates

### Root terragrunt.hcl

```hcl
# terragrunt.hcl (root)

locals {
  # Parse the file path to extract environment and region
  path_parts = split("/", path_relative_to_include())

  environment = try(local.path_parts[0], "dev")
  region      = try(local.path_parts[1], "us-east-1")

  # Load environment-specific variables
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl", "env.hcl"))

  # Common tags for all resources
  common_tags = {
    Environment = local.environment
    ManagedBy   = "terragrunt"
    Region      = local.region
  }
}

# Generate provider configuration
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.region}"

  default_tags {
    tags = ${jsonencode(local.common_tags)}
  }
}
EOF
}

# Remote state configuration
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket         = "company-terraform-state-${get_aws_account_id()}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# Common inputs for all modules
inputs = {
  environment = local.environment
  region      = local.region
  tags        = local.common_tags
}
```

### Module terragrunt.hcl

```hcl
# environments/prod/us-east-1/vpc/terragrunt.hcl

include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "${get_repo_root()}/modules/vpc"
}

inputs = {
  name_prefix        = "myapp-prod"
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

  enable_nat_gateway = true
  single_nat_gateway = false  # Production: NAT per AZ
}
```

---

*IaC Patterns Templates | faion-infrastructure-engineer*
