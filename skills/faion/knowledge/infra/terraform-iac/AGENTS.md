# Terraform IaC

## Summary

**One-sentence:** Terraform IaC architecture spec: module composition pattern, state-isolation per environment, monorepo vs polyrepo decision, blast-radius limits per workspace, refactor playbook for legacy resources.

**One-paragraph:** terraform-iac sits above 'terraform' (the tool) and covers the architecture: how to lay out state across envs, where modules live, how to isolate blast radius, how to refactor legacy resources without state surgery causing outage. The standard pattern: one workspace per (env, layer), modules in a registry, state isolated so a prod apply cannot touch dev. Refactor uses moved blocks (TF >=1.1) instead of state rm/import gymnastics. This methodology codifies the layout + the boundary rules + the refactor playbook.

**Ефективно для:**

- Workspace per (env, layer) — prod apply не може зачепити dev.
- Module registry замість copy-paste між проєктами.
- Refactor через moved blocks замість state rm + import dance.
- Blast radius per workspace: 'один apply, один scope'.

## Applies If (ALL must hold)

- Multiple envs (dev / staging / prod) sharing a Terraform codebase
- Multiple infra layers (network / data / compute / app) with different change cadences
- Legacy resources need refactoring (moved blocks, import)
- Compliance requires explicit blast-radius limits

## Skip If (ANY kills it)

- Single-env single-layer infra — 'terraform' methodology alone is enough
- Hand-off-only project where the consumer will rewrite the layout

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing Terraform setup | repo + state backend | platform team |
| Module registry (Terraform Registry / Artifactory) | registry credentials | platform team |
| Terraform >=1.5 | binary version | DevOps lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[terraform]] | Tool fundamentals — pinning, remote state, CI apply |
| [[drift-classification-taxonomy]] | How drift gets surfaced + classified |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/05-examples.xml` | medium | Worked example end-to-end | ~500 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `workspace_split_plan` | opus | Cross-resource impact judgment |
| `module_extraction` | sonnet | HCL refactor |
| `blast_radius_writeup` | sonnet | Concise structured writing |

## Templates

| File | Purpose |
|------|---------|
| `templates/backend-s3.tf` | Backend s3 template |
| `templates/github-actions.yml` | Github actions template |
| `templates/modules-vpc.tf` | Modules vpc template |
| `templates/variables.tf` | Variables template |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-terraform-iac.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[terraform]]
- [[drift-classification-taxonomy]]
- [[greenfield-infra-decision-matrix]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/backend-s3.tf`

```hcl
terraform {
  required_version = ">= 1.10.0"

  backend "s3" {
    bucket       = "mycompany-terraform-state"
    key          = "environments/prod/terraform.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true  # S3 native locking (Terraform 1.10+)
    # role_arn = "arn:aws:iam::123456789012:role/TerraformRole"  # cross-account
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
    }
  }
}
```

### `templates/github-actions.yml`

````yaml
name: Terraform

on:
  pull_request:
    paths: ['infrastructure/**']
  push:
    branches: [main]
    paths: ['infrastructure/**']

env:
  TF_VERSION: "1.10.0"
  WORKING_DIR: infrastructure/environments/prod

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with: { terraform_version: "${{ env.TF_VERSION }}" }
      - run: terraform fmt -check -recursive
        working-directory: infrastructure
      - run: terraform init -backend=false
        working-directory: ${{ env.WORKING_DIR }}
      - run: terraform validate
        working-directory: ${{ env.WORKING_DIR }}

  test:
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with: { terraform_version: "${{ env.TF_VERSION }}" }
      - run: terraform test
        working-directory: infrastructure/modules/vpc

  plan:
    runs-on: ubuntu-latest
    needs: [validate, test]
    if: github.event_name == 'pull_request'
    permissions: { pull-requests: write }
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with: { terraform_version: "${{ env.TF_VERSION }}" }
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: eu-central-1
      - run: terraform init
        working-directory: ${{ env.WORKING_DIR }}
      - run: terraform plan -no-color -out=tfplan 2>&1 | tee plan.txt
        id: plan
        working-directory: ${{ env.WORKING_DIR }}
      - uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const plan = fs.readFileSync('${{ env.WORKING_DIR }}/plan.txt', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner, repo: context.repo.repo,
              body: '#### Terraform Plan\n```\n' + plan.substring(0, 65000) + '\n```'
            });

  apply:
    runs-on: ubuntu-latest
    needs: [validate, test]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with: { terraform_version: "${{ env.TF_VERSION }}" }
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: eu-central-1
      - run: terraform init
        working-directory: ${{ env.WORKING_DIR }}
      - run: terraform apply -auto-approve
        working-directory: ${{ env.WORKING_DIR }}
````

### `templates/modules-vpc.tf`

```hcl
# modules/vpc/main.tf

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = { Name = "${var.project_name}-${var.environment}-vpc" }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.project_name}-${var.environment}-igw" }
}

resource "aws_subnet" "public" {
  count                   = length(var.availability_zones)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 4, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.project_name}-${var.environment}-public-${count.index + 1}"
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index + length(var.availability_zones))
  availability_zone = var.availability_zones[count.index]
  tags = {
    Name = "${var.project_name}-${var.environment}-private-${count.index + 1}"
    Type = "private"
  }
}

resource "aws_nat_gateway" "main" {
  count         = var.enable_nat_gateway ? 1 : 0
  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public[0].id
  tags          = { Name = "${var.project_name}-${var.environment}-nat" }
  depends_on    = [aws_internet_gateway.main]
}

resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? 1 : 0
  domain = "vpc"
  tags   = { Name = "${var.project_name}-${var.environment}-nat-eip" }
}

# modules/vpc/variables.tf
variable "project_name" { type = string }
variable "environment" { type = string }
variable "vpc_cidr" { type = string }
variable "availability_zones" { type = list(string) }
variable "enable_nat_gateway" { type = bool; default = true }

# modules/vpc/outputs.tf
output "vpc_id"             { value = aws_vpc.main.id }
output "vpc_cidr"           { value = aws_vpc.main.cidr_block }
output "public_subnet_ids"  { value = aws_subnet.public[*].id }
output "private_subnet_ids" { value = aws_subnet.private[*].id }
output "nat_gateway_ip"     { value = var.enable_nat_gateway ? aws_eip.nat[0].public_ip : null }
```

### `templates/variables.tf`

```hcl
variable "environment" {
  description = "Environment name"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name for resource naming (lowercase, 3-21 chars)"
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,20}$", var.project_name))
    error_message = "Project name must be lowercase, start with letter, 3-21 chars."
  }
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

variable "rds_password" {
  description = "RDS master password"
  type        = string
  sensitive   = true
}
```
