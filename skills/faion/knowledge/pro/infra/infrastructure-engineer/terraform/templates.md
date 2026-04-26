# Terraform Templates

**Ready-to-Use Configurations for Production Infrastructure (2025-2026)**

---

## Project Structure Template

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   ├── backend.tf
│   │   └── versions.tf
│   ├── staging/
│   │   └── ...
│   └── prod/
│       └── ...
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── versions.tf
│   │   ├── README.md
│   │   └── examples/
│   ├── compute/
│   │   └── ...
│   └── database/
│       └── ...
├── global/
│   ├── iam/
│   └── dns/
├── .terraform.lock.hcl
├── .tflint.hcl
├── .tfsec.yml
└── README.md
```

---

## Core Configuration Templates

### versions.tf Template

```hcl
# versions.tf

terraform {
  required_version = ">= 1.6.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    # Add other providers as needed
    # google = {
    #   source  = "hashicorp/google"
    #   version = "~> 5.0"
    # }
    # azurerm = {
    #   source  = "hashicorp/azurerm"
    #   version = "~> 3.0"
    # }
  }
}
```

### providers.tf Template

```hcl
# providers.tf

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "terraform"
      Owner       = var.owner
    }
  }

  # Cross-account assume role (if needed)
  # assume_role {
  #   role_arn     = "arn:aws:iam::ACCOUNT_ID:role/TerraformRole"
  #   session_name = "terraform-${var.environment}"
  # }
}

# Multi-region provider alias
provider "aws" {
  alias  = "us_west"
  region = "us-west-2"
}
```

### backend.tf Template (S3)

```hcl
# backend.tf

terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "ENVIRONMENT/COMPONENT/terraform.tfstate"  # e.g., "prod/networking/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"

    # Optional: KMS encryption
    # kms_key_id   = "arn:aws:kms:us-east-1:ACCOUNT:key/KEY_ID"

    # Optional: Cross-account access
    # role_arn     = "arn:aws:iam::ACCOUNT_ID:role/TerraformStateRole"
  }
}
```

### variables.tf Template

```hcl
# variables.tf

#--------------------------------------------------------------
# Required Variables
#--------------------------------------------------------------

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

#--------------------------------------------------------------
# Optional Variables with Defaults
#--------------------------------------------------------------

variable "owner" {
  description = "Owner of the infrastructure"
  type        = string
  default     = "platform-team"
}

variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}
```

### outputs.tf Template

```hcl
# outputs.tf

#--------------------------------------------------------------
# VPC Outputs
#--------------------------------------------------------------

output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = module.vpc.private_subnet_ids
}

#--------------------------------------------------------------
# Sensitive Outputs
#--------------------------------------------------------------

output "database_endpoint" {
  description = "Database endpoint"
  value       = module.database.endpoint
  sensitive   = true
}
```

### locals.tf Template

```hcl
# locals.tf

locals {
  # Naming convention
  name_prefix = "${var.project_name}-${var.environment}"

  # Common tags merged with variable tags
  common_tags = merge(
    {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "terraform"
      Owner       = var.owner
    },
    var.tags
  )

  # Environment-specific configurations
  config = {
    dev = {
      instance_type  = "t3.micro"
      instance_count = 1
      enable_nat     = false
      multi_az       = false
    }
    staging = {
      instance_type  = "t3.small"
      instance_count = 2
      enable_nat     = true
      multi_az       = false
    }
    prod = {
      instance_type  = "t3.large"
      instance_count = 4
      enable_nat     = true
      multi_az       = true
    }
  }

  # Current environment config
  env_config = local.config[var.environment]
}
```

### terraform.tfvars Template

```hcl
# terraform.tfvars (environment-specific)

# Required
environment  = "prod"
project_name = "myapp"
aws_region   = "us-east-1"

# Optional overrides
owner = "platform-team"

tags = {
  CostCenter = "engineering"
  Compliance = "soc2"
}
```

---

## Module Templates

### Module README.md Template

```markdown
# Module Name

Brief description of what this module does.

## Usage

```hcl
module "example" {
  source = "../../modules/example"

  name        = "my-resource"
  environment = "prod"

  tags = {
    Project = "myapp"
  }
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.6.0 |
| aws | ~> 5.0 |

## Providers

| Name | Version |
|------|---------|
| aws | ~> 5.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| name | Name prefix for resources | `string` | n/a | yes |
| environment | Environment name | `string` | n/a | yes |
| tags | Additional tags | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| id | Resource ID |
| arn | Resource ARN |

## Examples

See [examples/](examples/) directory.

## License

Apache 2.0
```

### Module main.tf Template

```hcl
# main.tf

#--------------------------------------------------------------
# Data Sources
#--------------------------------------------------------------

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

#--------------------------------------------------------------
# Resources
#--------------------------------------------------------------

resource "aws_resource" "main" {
  name = "${var.name}-resource"

  # Configuration
  setting = var.setting

  # Tags
  tags = merge(var.tags, {
    Name = "${var.name}-resource"
  })

  # Lifecycle
  lifecycle {
    create_before_destroy = true
  }
}
```

### Module variables.tf Template

```hcl
# variables.tf

#--------------------------------------------------------------
# Required Variables
#--------------------------------------------------------------

variable "name" {
  description = "Name prefix for all resources"
  type        = string

  validation {
    condition     = length(var.name) > 0 && length(var.name) <= 32
    error_message = "Name must be between 1 and 32 characters."
  }
}

#--------------------------------------------------------------
# Optional Variables
#--------------------------------------------------------------

variable "setting" {
  description = "Module setting"
  type        = string
  default     = "default-value"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
```

### Module outputs.tf Template

```hcl
# outputs.tf

output "id" {
  description = "ID of the resource"
  value       = aws_resource.main.id
}

output "arn" {
  description = "ARN of the resource"
  value       = aws_resource.main.arn
}
```

---

## VPC Module Template

### modules/vpc/main.tf

```hcl
# modules/vpc/main.tf

#--------------------------------------------------------------
# VPC
#--------------------------------------------------------------

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${var.name}-vpc"
  })
}

#--------------------------------------------------------------
# Public Subnets
#--------------------------------------------------------------

resource "aws_subnet" "public" {
  count = length(var.public_subnets)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnets[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "${var.name}-public-${var.availability_zones[count.index]}"
    Type = "public"
  })
}

#--------------------------------------------------------------
# Private Subnets
#--------------------------------------------------------------

resource "aws_subnet" "private" {
  count = length(var.private_subnets)

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnets[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(var.tags, {
    Name = "${var.name}-private-${var.availability_zones[count.index]}"
    Type = "private"
  })
}

#--------------------------------------------------------------
# Internet Gateway
#--------------------------------------------------------------

resource "aws_internet_gateway" "main" {
  count = var.create_igw ? 1 : 0

  vpc_id = aws_vpc.main.id

  tags = merge(var.tags, {
    Name = "${var.name}-igw"
  })
}

#--------------------------------------------------------------
# NAT Gateway
#--------------------------------------------------------------

resource "aws_eip" "nat" {
  count = var.create_nat_gateway ? var.single_nat_gateway ? 1 : length(var.public_subnets) : 0

  domain = "vpc"

  tags = merge(var.tags, {
    Name = "${var.name}-nat-eip-${count.index + 1}"
  })

  depends_on = [aws_internet_gateway.main]
}

resource "aws_nat_gateway" "main" {
  count = var.create_nat_gateway ? var.single_nat_gateway ? 1 : length(var.public_subnets) : 0

  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(var.tags, {
    Name = "${var.name}-nat-${count.index + 1}"
  })

  depends_on = [aws_internet_gateway.main]
}

#--------------------------------------------------------------
# Route Tables
#--------------------------------------------------------------

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  tags = merge(var.tags, {
    Name = "${var.name}-public-rt"
  })
}

resource "aws_route" "public_internet" {
  count = var.create_igw ? 1 : 0

  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main[0].id
}

resource "aws_route_table_association" "public" {
  count = length(var.public_subnets)

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
  count = var.create_nat_gateway ? var.single_nat_gateway ? 1 : length(var.private_subnets) : 1

  vpc_id = aws_vpc.main.id

  tags = merge(var.tags, {
    Name = var.single_nat_gateway ? "${var.name}-private-rt" : "${var.name}-private-rt-${count.index + 1}"
  })
}

resource "aws_route" "private_nat" {
  count = var.create_nat_gateway ? var.single_nat_gateway ? 1 : length(var.private_subnets) : 0

  route_table_id         = aws_route_table.private[count.index].id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = var.single_nat_gateway ? aws_nat_gateway.main[0].id : aws_nat_gateway.main[count.index].id
}

resource "aws_route_table_association" "private" {
  count = length(var.private_subnets)

  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = var.single_nat_gateway || !var.create_nat_gateway ? aws_route_table.private[0].id : aws_route_table.private[count.index].id
}

#--------------------------------------------------------------
# VPC Flow Logs
#--------------------------------------------------------------

resource "aws_flow_log" "main" {
  count = var.enable_flow_logs ? 1 : 0

  vpc_id                   = aws_vpc.main.id
  traffic_type             = "ALL"
  log_destination_type     = "cloud-watch-logs"
  log_destination          = aws_cloudwatch_log_group.flow_logs[0].arn
  iam_role_arn             = aws_iam_role.flow_logs[0].arn
  max_aggregation_interval = 60

  tags = merge(var.tags, {
    Name = "${var.name}-flow-logs"
  })
}

resource "aws_cloudwatch_log_group" "flow_logs" {
  count = var.enable_flow_logs ? 1 : 0

  name              = "/aws/vpc/${var.name}/flow-logs"
  retention_in_days = var.flow_logs_retention_days

  tags = var.tags
}

resource "aws_iam_role" "flow_logs" {
  count = var.enable_flow_logs ? 1 : 0

  name = "${var.name}-flow-logs-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "vpc-flow-logs.amazonaws.com"
      }
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy" "flow_logs" {
  count = var.enable_flow_logs ? 1 : 0

  name = "${var.name}-flow-logs-policy"
  role = aws_iam_role.flow_logs[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams"
      ]
      Resource = "*"
    }]
  })
}
```

### modules/vpc/variables.tf

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

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "public_subnets" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
  default     = []
}

variable "private_subnets" {
  description = "List of private subnet CIDR blocks"
  type        = list(string)
  default     = []
}

variable "create_igw" {
  description = "Create Internet Gateway"
  type        = bool
  default     = true
}

variable "create_nat_gateway" {
  description = "Create NAT Gateway(s)"
  type        = bool
  default     = true
}

variable "single_nat_gateway" {
  description = "Use single NAT Gateway (cost savings, less HA)"
  type        = bool
  default     = false
}

variable "enable_flow_logs" {
  description = "Enable VPC Flow Logs"
  type        = bool
  default     = true
}

variable "flow_logs_retention_days" {
  description = "Flow logs retention in days"
  type        = number
  default     = 30
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
```

### modules/vpc/outputs.tf

```hcl
# modules/vpc/outputs.tf

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_arn" {
  description = "ARN of the VPC"
  value       = aws_vpc.main.arn
}

output "vpc_cidr_block" {
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

output "public_subnet_cidrs" {
  description = "CIDR blocks of public subnets"
  value       = aws_subnet.public[*].cidr_block
}

output "private_subnet_cidrs" {
  description = "CIDR blocks of private subnets"
  value       = aws_subnet.private[*].cidr_block
}

output "nat_gateway_public_ips" {
  description = "Public IPs of NAT Gateways"
  value       = aws_eip.nat[*].public_ip
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = var.create_igw ? aws_internet_gateway.main[0].id : null
}
```

---

## Tool Configuration Templates

### .tflint.hcl

```hcl
# .tflint.hcl

config {
  plugin_dir = "~/.tflint.d/plugins"
}

plugin "aws" {
  enabled = true
  version = "0.29.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

rule "terraform_deprecated_interpolation" {
  enabled = true
}

rule "terraform_documented_outputs" {
  enabled = true
}

rule "terraform_documented_variables" {
  enabled = true
}

rule "terraform_naming_convention" {
  enabled = true
  format  = "snake_case"
}

rule "terraform_required_providers" {
  enabled = true
}

rule "terraform_required_version" {
  enabled = true
}

rule "terraform_standard_module_structure" {
  enabled = true
}

rule "terraform_unused_declarations" {
  enabled = true
}

rule "terraform_unused_required_providers" {
  enabled = true
}
```

### .tfsec.yml

```yaml
# .tfsec.yml

minimum_severity: MEDIUM

exclude:
  - aws-vpc-no-public-egress-sg  # If intentionally allowing outbound

severity_overrides:
  aws-s3-enable-bucket-logging: LOW

exclude_ignores:
  - "This resource is intentionally public"
```

### .gitignore

```gitignore
# Terraform
.terraform/
.terraform.lock.hcl
*.tfstate
*.tfstate.*
*.tfvars
!*.tfvars.example
*.tfplan
crash.log
crash.*.log
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Secrets
*.pem
*.key
.env
```

### Makefile

```makefile
# Makefile for Terraform operations

.PHONY: init plan apply destroy fmt validate lint security

ENV ?= dev
TF_DIR := environments/$(ENV)

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
	tflint --init
	tflint --recursive

security:
	tfsec .
	checkov -d .

docs:
	terraform-docs markdown table modules/ > modules/README.md

clean:
	find . -type d -name ".terraform" -exec rm -rf {} +
	find . -name "*.tfplan" -delete
```

---

*Terraform Templates | faion-infrastructure-engineer*
