# IaC Templates

## Terraform Project Template

### Directory Structure

```
infrastructure/
├── .gitignore
├── .pre-commit-config.yaml
├── .tflint.hcl
├── README.md
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── prod/
├── modules/
│   └── [module-name]/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── README.md
└── policies/
    └── [policy-name].rego
```

### .gitignore Template

```gitignore
# Terraform
*.tfstate
*.tfstate.*
.terraform/
.terraform.lock.hcl
*.tfplan
crash.log
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Secrets
*.pem
*.key
.env
.env.*
secrets.tfvars
*-secrets.tfvars

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test artifacts
terraform-test-*/
```

### Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_docs
        args:
          - --hook-config=--path-to-file=README.md
          - --hook-config=--add-to-existing-file=true
          - --hook-config=--create-file-if-not-exist=true
      - id: terraform_tflint
        args:
          - --args=--config=__GIT_WORKING_DIR__/.tflint.hcl
      - id: terraform_tfsec
```

### TFLint Configuration

```hcl
# .tflint.hcl
config {
  module = true
}

plugin "terraform" {
  enabled = true
  preset  = "recommended"
}

plugin "aws" {
  enabled = true
  version = "0.28.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

rule "terraform_naming_convention" {
  enabled = true
  format  = "snake_case"
}

rule "terraform_documented_variables" {
  enabled = true
}

rule "terraform_documented_outputs" {
  enabled = true
}

rule "terraform_standard_module_structure" {
  enabled = true
}
```

### Backend Configuration Template

```hcl
# backend.tf
terraform {
  required_version = ">= 1.6.0"

  backend "s3" {
    bucket         = "COMPANY-terraform-state"
    key            = "environments/ENV/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
      Project     = var.project_name
      Team        = var.team
    }
  }
}
```

### Variables Template

```hcl
# variables.tf
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name for resource naming and tagging"
  type        = string
}

variable "team" {
  description = "Team responsible for these resources"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be a valid IPv4 CIDR block."
  }
}

variable "availability_zones" {
  description = "List of availability zones to use"
  type        = list(string)
  default     = []
}
```

### Outputs Template

```hcl
# outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

output "cluster_endpoint" {
  description = "Kubernetes cluster endpoint"
  value       = module.eks.cluster_endpoint
  sensitive   = true
}

output "cluster_name" {
  description = "Kubernetes cluster name"
  value       = module.eks.cluster_name
}
```

### tfvars Template

```hcl
# terraform.tfvars
environment = "dev"
aws_region  = "eu-central-1"
project_name = "myproject"
team         = "platform"

vpc_cidr = "10.0.0.0/16"

availability_zones = [
  "eu-central-1a",
  "eu-central-1b",
  "eu-central-1c"
]

# EKS configuration
eks_cluster_version = "1.29"
eks_node_groups = {
  general = {
    instance_types = ["t3.medium"]
    min_size       = 2
    max_size       = 10
    desired_size   = 3
    disk_size      = 50
    labels = {
      role = "general"
    }
    taints = []
  }
}

# RDS configuration
rds_config = {
  engine_version    = "16.1"
  instance_class    = "db.t3.medium"
  allocated_storage = 100
  multi_az          = false
}
```

## Module Template

### Module Structure

```
modules/[name]/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── README.md
└── examples/
    └── basic/
        ├── main.tf
        └── outputs.tf
```

### Module main.tf Template

```hcl
# main.tf
resource "aws_RESOURCE" "main" {
  name = var.name

  dynamic "BLOCK" {
    for_each = var.BLOCK_config
    content {
      key   = BLOCK.value.key
      value = BLOCK.value.value
    }
  }

  tags = merge(
    var.tags,
    {
      Name = var.name
    }
  )

  lifecycle {
    create_before_destroy = true
  }
}
```

### Module versions.tf Template

```hcl
# versions.tf
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

### Module README Template

```markdown
# Module: [name]

## Description

Brief description of what this module provisions.

## Usage

\`\`\`hcl
module "example" {
  source = "../../modules/[name]"

  name        = "my-resource"
  environment = "dev"

  # Additional configuration
}
\`\`\`

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.6.0 |
| aws | >= 5.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| name | Resource name | `string` | n/a | yes |
| environment | Environment name | `string` | n/a | yes |
| tags | Additional tags | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| id | Resource ID |
| arn | Resource ARN |

## Examples

See [examples/basic](examples/basic) for a complete example.
```

## GitHub Actions Workflow Template

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
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'dev'
        type: choice
        options:
          - dev
          - staging
          - prod

env:
  TF_VERSION: '1.6.0'
  AWS_REGION: 'eu-central-1'

permissions:
  contents: read
  pull-requests: write
  id-token: write

jobs:
  validate:
    name: Validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Format Check
        run: terraform fmt -check -recursive

      - name: Setup TFLint
        uses: terraform-linters/setup-tflint@v4

      - name: Run TFLint
        run: tflint --recursive

      - name: Run tfsec
        uses: aquasecurity/tfsec-action@v1.0.3
        with:
          working_directory: infrastructure

  plan:
    name: Plan
    needs: validate
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
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
        id: plan
        working-directory: infrastructure/environments/${{ matrix.environment }}
        run: terraform plan -no-color -out=tfplan

      - name: Upload Plan
        uses: actions/upload-artifact@v4
        with:
          name: tfplan-${{ matrix.environment }}
          path: infrastructure/environments/${{ matrix.environment }}/tfplan

  apply:
    name: Apply
    needs: plan
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
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
          name: tfplan-prod
          path: infrastructure/environments/prod

      - name: Terraform Init
        working-directory: infrastructure/environments/prod
        run: terraform init

      - name: Terraform Apply
        working-directory: infrastructure/environments/prod
        run: terraform apply -auto-approve tfplan
```

## OPA Policy Template

```rego
# policies/required-tags.rego
package terraform.policies.required_tags

import rego.v1

required_tags := ["Environment", "Project", "ManagedBy", "Team"]

deny contains msg if {
    resource := input.resource_changes[_]
    resource.change.actions[_] == "create"
    tags := resource.change.after.tags

    missing := {tag | tag := required_tags[_]; not tags[tag]}
    count(missing) > 0

    msg := sprintf(
        "Resource %s is missing required tags: %v",
        [resource.address, missing]
    )
}

deny contains msg if {
    resource := input.resource_changes[_]
    resource.change.actions[_] == "create"
    not resource.change.after.tags

    msg := sprintf(
        "Resource %s has no tags defined",
        [resource.address]
    )
}
```

## Makefile Template

```makefile
# Makefile
.PHONY: init plan apply destroy fmt validate lint security test

ENV ?= dev
TF_DIR = infrastructure/environments/$(ENV)

init:
	cd $(TF_DIR) && terraform init

plan:
	cd $(TF_DIR) && terraform plan -out=tfplan

apply:
	cd $(TF_DIR) && terraform apply tfplan

destroy:
	cd $(TF_DIR) && terraform destroy

fmt:
	terraform fmt -recursive

validate:
	cd $(TF_DIR) && terraform validate

lint:
	tflint --recursive

security:
	tfsec infrastructure/

test:
	cd tests && go test -v -timeout 30m

clean:
	find . -name "*.tfplan" -delete
	find . -name ".terraform" -type d -exec rm -rf {} +
```

---

*IaC Templates | faion-infrastructure-engineer*
