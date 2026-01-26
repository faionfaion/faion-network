# Terraform Examples

**Production Patterns: State, Modules, Workspaces, CI/CD (2025-2026)**

---

## State Management Examples

### S3 Backend with DynamoDB Locking (AWS)

```hcl
# backend.tf

terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "prod/networking/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:us-east-1:123456789:key/abc123"
    dynamodb_table = "terraform-locks"

    # Cross-account access
    role_arn       = "arn:aws:iam::ACCOUNT_ID:role/TerraformStateRole"
  }
}
```

### DynamoDB Lock Table Setup

```hcl
# global/state-infrastructure/main.tf

resource "aws_s3_bucket" "terraform_state" {
  bucket = "company-terraform-state"

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

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Name      = "terraform-state-locks"
    ManagedBy = "terraform"
  }
}

resource "aws_kms_key" "terraform_state" {
  description             = "KMS key for Terraform state encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}
```

### GCS Backend (GCP)

```hcl
# backend.tf

terraform {
  backend "gcs" {
    bucket = "company-terraform-state"
    prefix = "prod/networking"
  }
}
```

### Azure Blob Backend

```hcl
# backend.tf

terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-rg"
    storage_account_name = "companyterraformstate"
    container_name       = "tfstate"
    key                  = "prod/networking/terraform.tfstate"
    use_azuread_auth     = true
  }
}
```

### Terraform Cloud Backend

```hcl
# backend.tf

terraform {
  cloud {
    organization = "company-name"

    workspaces {
      name = "prod-networking"
    }
  }
}
```

### Remote State Data Source

```hcl
# Access outputs from networking state in compute configuration

data "terraform_remote_state" "networking" {
  backend = "s3"

  config = {
    bucket = "company-terraform-state"
    key    = "prod/networking/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_instance" "app" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = data.terraform_remote_state.networking.outputs.private_subnet_ids[0]

  vpc_security_group_ids = [
    data.terraform_remote_state.networking.outputs.app_security_group_id
  ]
}
```

---

## Module Examples

### VPC Module Definition

```hcl
# modules/vpc/main.tf

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${var.name}-vpc"
  })
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnets)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnets[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "${var.name}-public-${count.index + 1}"
    Type = "public"
  })
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnets[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(var.tags, {
    Name = "${var.name}-private-${count.index + 1}"
    Type = "private"
  })
}

resource "aws_internet_gateway" "main" {
  count  = var.enable_internet_gateway ? 1 : 0
  vpc_id = aws_vpc.main.id

  tags = merge(var.tags, {
    Name = "${var.name}-igw"
  })
}

resource "aws_nat_gateway" "main" {
  count         = var.enable_nat_gateway ? length(var.public_subnets) : 0
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(var.tags, {
    Name = "${var.name}-nat-${count.index + 1}"
  })

  depends_on = [aws_internet_gateway.main]
}

resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? length(var.public_subnets) : 0
  domain = "vpc"

  tags = merge(var.tags, {
    Name = "${var.name}-nat-eip-${count.index + 1}"
  })
}
```

```hcl
# modules/vpc/variables.tf

variable "name" {
  description = "Name prefix for all resources"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be a valid CIDR block."
  }
}

variable "public_subnets" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnets" {
  description = "List of private subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "enable_internet_gateway" {
  description = "Create Internet Gateway"
  type        = bool
  default     = true
}

variable "enable_nat_gateway" {
  description = "Create NAT Gateway(s)"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
```

```hcl
# modules/vpc/outputs.tf

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "nat_gateway_ips" {
  description = "Public IPs of NAT Gateways"
  value       = aws_eip.nat[*].public_ip
}
```

```hcl
# modules/vpc/versions.tf

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0, < 6.0.0"
    }
  }
}
```

### Module Usage

```hcl
# environments/prod/main.tf

module "vpc" {
  source = "../../modules/vpc"

  name               = "production"
  vpc_cidr           = "10.0.0.0/16"
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets    = ["10.0.10.0/24", "10.0.11.0/24", "10.0.12.0/24"]
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

  enable_nat_gateway = true

  tags = local.common_tags
}

module "database" {
  source = "../../modules/rds"

  name             = "production"
  engine           = "postgres"
  engine_version   = "16.1"
  instance_class   = "db.r6g.large"
  allocated_storage = 100

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids

  # Pass sensitive values securely
  master_password = var.db_master_password

  tags = local.common_tags
}
```

### Module with for_each

```hcl
# Create multiple EC2 instances from module

module "web_servers" {
  source   = "./modules/ec2"
  for_each = toset(["web-1", "web-2", "web-3"])

  name          = each.key
  instance_type = var.instance_type
  subnet_id     = module.vpc.private_subnet_ids[index(tolist(toset(["web-1", "web-2", "web-3"])), each.key) % length(module.vpc.private_subnet_ids)]

  tags = merge(local.common_tags, {
    Role = "web-server"
  })
}

# Access outputs
output "web_server_ips" {
  value = { for k, v in module.web_servers : k => v.private_ip }
}
```

---

## Workspace Examples

### Workspace-Based Configuration

```hcl
# main.tf

locals {
  environment = terraform.workspace

  config = {
    default = {
      instance_count = 1
      instance_type  = "t3.micro"
      enable_nat     = false
    }
    development = {
      instance_count = 1
      instance_type  = "t3.micro"
      enable_nat     = false
    }
    staging = {
      instance_count = 2
      instance_type  = "t3.small"
      enable_nat     = true
    }
    production = {
      instance_count = 4
      instance_type  = "t3.large"
      enable_nat     = true
    }
  }

  current_config = local.config[local.environment]
}

module "vpc" {
  source = "./modules/vpc"

  name               = "app-${local.environment}"
  enable_nat_gateway = local.current_config.enable_nat

  tags = {
    Environment = local.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}

resource "aws_instance" "app" {
  count = local.current_config.instance_count

  ami           = data.aws_ami.ubuntu.id
  instance_type = local.current_config.instance_type
  subnet_id     = module.vpc.private_subnet_ids[count.index % length(module.vpc.private_subnet_ids)]

  tags = {
    Name        = "app-${local.environment}-${count.index + 1}"
    Environment = local.environment
  }
}
```

### Workspace Commands

```bash
# List workspaces
terraform workspace list

# Create workspaces
terraform workspace new development
terraform workspace new staging
terraform workspace new production

# Select workspace
terraform workspace select production

# Show current
terraform workspace show

# Delete (cannot delete if current)
terraform workspace select default
terraform workspace delete staging
```

### Directory-Based Environment Isolation (Recommended for Production)

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf           # Points to dev state
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf           # Points to staging state
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars
│       └── backend.tf           # Points to prod state
└── modules/
    └── ...
```

```hcl
# environments/prod/backend.tf

terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "prod/infrastructure/terraform.tfstate"  # Different key per env
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

---

## CI/CD Integration Examples

### GitHub Actions Pipeline

```yaml
# .github/workflows/terraform.yml

name: Terraform

on:
  push:
    branches: [main]
    paths:
      - 'terraform/**'
  pull_request:
    branches: [main]
    paths:
      - 'terraform/**'

permissions:
  contents: read
  pull-requests: write
  id-token: write  # For OIDC

env:
  TF_VERSION: "1.6.0"
  WORKING_DIR: "./terraform/environments/prod"

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup TFLint
        uses: terraform-linters/setup-tflint@v4

      - name: Run TFLint
        working-directory: ${{ env.WORKING_DIR }}
        run: |
          tflint --init
          tflint --format=compact

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run tfsec
        uses: aquasecurity/tfsec-action@v1.0.0
        with:
          working_directory: ${{ env.WORKING_DIR }}
          soft_fail: false

      - name: Run Checkov
        uses: bridgecrewio/checkov-action@v12
        with:
          directory: ${{ env.WORKING_DIR }}
          framework: terraform
          output_format: cli

  plan:
    name: Plan
    runs-on: ubuntu-latest
    needs: [lint, security]
    outputs:
      plan_exitcode: ${{ steps.plan.outputs.exitcode }}
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/GitHubActionsRole
          aws-region: us-east-1

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Init
        working-directory: ${{ env.WORKING_DIR }}
        run: terraform init

      - name: Terraform Plan
        id: plan
        working-directory: ${{ env.WORKING_DIR }}
        run: |
          terraform plan -detailed-exitcode -out=tfplan 2>&1 | tee plan.txt
          echo "exitcode=$?" >> $GITHUB_OUTPUT
        continue-on-error: true

      - name: Upload Plan
        uses: actions/upload-artifact@v4
        with:
          name: tfplan
          path: ${{ env.WORKING_DIR }}/tfplan

      - name: Comment Plan on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const plan = fs.readFileSync('${{ env.WORKING_DIR }}/plan.txt', 'utf8');
            const truncated = plan.length > 60000 ? plan.substring(0, 60000) + '\n... [truncated]' : plan;

            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `## Terraform Plan\n\`\`\`\n${truncated}\n\`\`\``
            });

  apply:
    name: Apply
    runs-on: ubuntu-latest
    needs: [plan]
    if: github.ref == 'refs/heads/main' && needs.plan.outputs.plan_exitcode == '2'
    environment: production  # Requires approval
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/GitHubActionsRole
          aws-region: us-east-1

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Download Plan
        uses: actions/download-artifact@v4
        with:
          name: tfplan
          path: ${{ env.WORKING_DIR }}

      - name: Terraform Init
        working-directory: ${{ env.WORKING_DIR }}
        run: terraform init

      - name: Terraform Apply
        working-directory: ${{ env.WORKING_DIR }}
        run: terraform apply -auto-approve tfplan
```

### GitLab CI Pipeline

```yaml
# .gitlab-ci.yml

image:
  name: hashicorp/terraform:1.6.0
  entrypoint: [""]

variables:
  TF_ROOT: ${CI_PROJECT_DIR}/terraform/environments/prod
  TF_STATE_NAME: prod

cache:
  key: terraform-${CI_COMMIT_REF_SLUG}
  paths:
    - ${TF_ROOT}/.terraform

stages:
  - validate
  - plan
  - apply

before_script:
  - cd ${TF_ROOT}
  - terraform init

validate:
  stage: validate
  script:
    - terraform fmt -check -recursive
    - terraform validate
    - tflint --init && tflint
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

security_scan:
  stage: validate
  image: bridgecrew/checkov:latest
  script:
    - checkov -d ${TF_ROOT} --framework terraform
  allow_failure: false
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

plan:
  stage: plan
  script:
    - terraform plan -out=plan.tfplan
  artifacts:
    name: plan
    paths:
      - ${TF_ROOT}/plan.tfplan
    expire_in: 1 week
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

apply:
  stage: apply
  script:
    - terraform apply -auto-approve plan.tfplan
  dependencies:
    - plan
  environment:
    name: production
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

### Atlantis Configuration

```yaml
# atlantis.yaml

version: 3
automerge: false
delete_source_branch_on_merge: true

projects:
  - name: prod-networking
    dir: terraform/environments/prod/networking
    workspace: default
    autoplan:
      when_modified: ["*.tf", "*.tfvars", "../../modules/**/*.tf"]
      enabled: true
    apply_requirements: [approved, mergeable]
    workflow: default

  - name: prod-compute
    dir: terraform/environments/prod/compute
    workspace: default
    autoplan:
      when_modified: ["*.tf", "*.tfvars", "../../modules/**/*.tf"]
      enabled: true
    apply_requirements: [approved, mergeable]
    workflow: default

workflows:
  default:
    plan:
      steps:
        - run: tflint --init && tflint
        - run: tfsec .
        - init
        - plan
    apply:
      steps:
        - apply
```

---

## Advanced Patterns

### Conditional Resource Creation

```hcl
resource "aws_nat_gateway" "main" {
  count = var.create_nat_gateway ? 1 : 0

  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public[0].id
}

resource "aws_eip" "nat" {
  count  = var.create_nat_gateway ? 1 : 0
  domain = "vpc"
}
```

### Dynamic Blocks

```hcl
resource "aws_security_group" "main" {
  name   = "dynamic-sg"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
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
}

# Variable definition
variable "ingress_rules" {
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
  default = [
    {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTPS"
    },
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTP"
    }
  ]
}
```

### Moved Block (Refactoring)

```hcl
# When renaming resources, use moved block to preserve state

moved {
  from = aws_instance.web
  to   = aws_instance.app
}

moved {
  from = module.old_vpc
  to   = module.networking
}
```

### Import Block (Terraform 1.5+)

```hcl
# Import existing resources declaratively

import {
  to = aws_instance.existing
  id = "i-1234567890abcdef0"
}

resource "aws_instance" "existing" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  # ... other attributes
}
```

### Terraform Test (Native Testing)

```hcl
# tests/vpc.tftest.hcl

run "vpc_creation" {
  command = plan

  variables {
    name     = "test"
    vpc_cidr = "10.0.0.0/16"
  }

  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR mismatch"
  }

  assert {
    condition     = aws_vpc.main.enable_dns_hostnames == true
    error_message = "DNS hostnames should be enabled"
  }
}

run "subnet_count" {
  command = plan

  variables {
    name           = "test"
    public_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  }

  assert {
    condition     = length(aws_subnet.public) == 2
    error_message = "Should create 2 public subnets"
  }
}
```

---

*Terraform Examples | faion-infrastructure-engineer*
