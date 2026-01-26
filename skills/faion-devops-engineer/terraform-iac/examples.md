# Terraform Examples

## Backend Configuration

### S3 Backend (AWS) - Recommended

```hcl
terraform {
  required_version = ">= 1.10.0"

  backend "s3" {
    bucket       = "mycompany-terraform-state"
    key          = "environments/prod/terraform.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true  # S3 native locking (Terraform 1.10+)

    # Optional: Cross-account access
    # role_arn = "arn:aws:iam::123456789012:role/TerraformRole"
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

### GCS Backend (GCP)

```hcl
terraform {
  required_version = ">= 1.10.0"

  backend "gcs" {
    bucket = "mycompany-terraform-state"
    prefix = "prod"
    # Locking is built-in, encryption is default
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
```

---

## Variable Definitions

### variables.tf with Validation

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
  description = "Project name for resource naming"
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

variable "eks_node_groups" {
  description = "EKS node group configurations"
  type = map(object({
    instance_types = list(string)
    min_size       = number
    max_size       = number
    desired_size   = number
    disk_size      = number
    labels         = map(string)
    taints = list(object({
      key    = string
      value  = string
      effect = string
    }))
  }))
  default = {
    general = {
      instance_types = ["t3.medium"]
      min_size       = 2
      max_size       = 10
      desired_size   = 3
      disk_size      = 50
      labels         = {}
      taints         = []
    }
  }
}

variable "rds_password" {
  description = "RDS master password"
  type        = string
  sensitive   = true
}
```

---

## Module Examples

### VPC Module (modules/vpc/)

**modules/vpc/main.tf:**

```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-${var.environment}-vpc"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-${var.environment}-igw"
  }
}

resource "aws_subnet" "public" {
  count = length(var.availability_zones)

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
  count = length(var.availability_zones)

  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index + length(var.availability_zones))
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name = "${var.project_name}-${var.environment}-private-${count.index + 1}"
    Type = "private"
  }
}

resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? 1 : 0
  domain = "vpc"

  tags = {
    Name = "${var.project_name}-${var.environment}-nat-eip"
  }
}

resource "aws_nat_gateway" "main" {
  count = var.enable_nat_gateway ? 1 : 0

  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "${var.project_name}-${var.environment}-nat"
  }

  depends_on = [aws_internet_gateway.main]
}
```

**modules/vpc/variables.tf:**

```hcl
variable "project_name" {
  description = "Project name for resource naming"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "enable_nat_gateway" {
  description = "Enable NAT gateway for private subnets"
  type        = bool
  default     = true
}
```

**modules/vpc/outputs.tf:**

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
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "nat_gateway_ip" {
  description = "NAT gateway public IP"
  value       = var.enable_nat_gateway ? aws_eip.nat[0].public_ip : null
}
```

### Module Usage

```hcl
module "vpc" {
  source = "../../modules/vpc"

  project_name       = var.project_name
  environment        = var.environment
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  enable_nat_gateway = var.environment != "dev"
}

module "eks" {
  source = "../../modules/eks"

  project_name   = var.project_name
  environment    = var.environment
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids
  node_groups    = var.eks_node_groups

  depends_on = [module.vpc]
}
```

---

## Testing Examples

### Unit Test (tests/vpc.tftest.hcl)

```hcl
# Test VPC module with mocking
run "vpc_creation" {
  command = plan

  variables {
    project_name       = "test"
    environment        = "dev"
    vpc_cidr           = "10.0.0.0/16"
    availability_zones = ["eu-central-1a", "eu-central-1b"]
    enable_nat_gateway = false
  }

  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR block does not match expected value"
  }

  assert {
    condition     = length(aws_subnet.public) == 2
    error_message = "Expected 2 public subnets"
  }

  assert {
    condition     = length(aws_subnet.private) == 2
    error_message = "Expected 2 private subnets"
  }
}

run "vpc_with_nat" {
  command = plan

  variables {
    project_name       = "test"
    environment        = "prod"
    vpc_cidr           = "10.0.0.0/16"
    availability_zones = ["eu-central-1a", "eu-central-1b"]
    enable_nat_gateway = true
  }

  assert {
    condition     = length(aws_nat_gateway.main) == 1
    error_message = "NAT gateway should be created for prod"
  }
}
```

### Integration Test with Real Resources

```hcl
# tests/integration.tftest.hcl
run "create_vpc" {
  command = apply

  variables {
    project_name       = "tftest-${timestamp()}"
    environment        = "test"
    vpc_cidr           = "10.99.0.0/16"
    availability_zones = ["eu-central-1a"]
    enable_nat_gateway = false
  }

  assert {
    condition     = output.vpc_id != ""
    error_message = "VPC ID should not be empty"
  }
}

run "verify_vpc_attributes" {
  command = plan

  # Uses state from previous run
  assert {
    condition     = length(output.public_subnet_ids) > 0
    error_message = "Should have at least one public subnet"
  }
}
```

### Test with Mocking

```hcl
# tests/mocked.tftest.hcl
mock_provider "aws" {
  mock_resource "aws_vpc" {
    defaults = {
      id         = "vpc-mock123"
      cidr_block = "10.0.0.0/16"
    }
  }

  mock_resource "aws_subnet" {
    defaults = {
      id = "subnet-mock123"
    }
  }
}

run "mocked_vpc_test" {
  command = plan

  providers = {
    aws = aws.mock
  }

  assert {
    condition     = aws_vpc.main.id == "vpc-mock123"
    error_message = "Should use mocked VPC ID"
  }
}
```

---

## CI/CD Examples

### GitHub Actions Workflow

```yaml
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

env:
  TF_VERSION: "1.10.0"
  WORKING_DIR: infrastructure/environments/prod

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Format Check
        run: terraform fmt -check -recursive
        working-directory: infrastructure

      - name: Terraform Init
        run: terraform init -backend=false
        working-directory: ${{ env.WORKING_DIR }}

      - name: Terraform Validate
        run: terraform validate
        working-directory: ${{ env.WORKING_DIR }}

  test:
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Test
        run: terraform test
        working-directory: infrastructure/modules/vpc

  plan:
    runs-on: ubuntu-latest
    needs: [validate, test]
    if: github.event_name == 'pull_request'
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: eu-central-1

      - name: Terraform Init
        run: terraform init
        working-directory: ${{ env.WORKING_DIR }}

      - name: Terraform Plan
        id: plan
        run: |
          terraform plan -no-color -out=tfplan 2>&1 | tee plan.txt
        working-directory: ${{ env.WORKING_DIR }}

      - name: Comment PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const plan = fs.readFileSync('${{ env.WORKING_DIR }}/plan.txt', 'utf8');
            const output = `#### Terraform Plan
            \`\`\`
            ${plan.substring(0, 65000)}
            \`\`\``;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            });

  apply:
    runs-on: ubuntu-latest
    needs: [validate, test]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: eu-central-1

      - name: Terraform Init
        run: terraform init
        working-directory: ${{ env.WORKING_DIR }}

      - name: Terraform Apply
        run: terraform apply -auto-approve
        working-directory: ${{ env.WORKING_DIR }}
```

---

## Common Operations

### Import Existing Resource

```bash
# Import S3 bucket
terraform import aws_s3_bucket.example my-bucket-name

# Import with module
terraform import module.vpc.aws_vpc.main vpc-abc123

# Import multiple resources (script)
for id in vpc-1 vpc-2 vpc-3; do
  terraform import "aws_vpc.main[\"$id\"]" "$id"
done
```

### State Operations

```bash
# List all resources
terraform state list

# Show resource details
terraform state show aws_vpc.main

# Move resource (refactoring)
terraform state mv aws_s3_bucket.old aws_s3_bucket.new

# Remove resource from state (keep in cloud)
terraform state rm aws_s3_bucket.orphaned

# Pull state for backup
terraform state pull > backup.tfstate

# Push restored state
terraform state push backup.tfstate
```

### Workspace Operations

```bash
# List workspaces
terraform workspace list

# Create new workspace
terraform workspace new staging

# Select workspace
terraform workspace select prod

# Show current workspace
terraform workspace show
```

### Debugging

```bash
# Enable debug logging
TF_LOG=DEBUG terraform plan

# Log to file
TF_LOG=DEBUG TF_LOG_PATH=./terraform.log terraform plan

# Trace provider operations
TF_LOG=TRACE terraform apply
```
