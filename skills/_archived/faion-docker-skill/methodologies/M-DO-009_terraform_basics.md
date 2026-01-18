# M-DO-009: Terraform Basics

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #terraform, #iac, #infrastructure, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Manual infrastructure provisioning is slow, error-prone, and undocumented. Changes made in cloud consoles are hard to track and reproduce.

## Promise

After this methodology, you will manage infrastructure as code with Terraform. Your infrastructure will be version-controlled, reproducible, and automated.

## Overview

Terraform is an Infrastructure as Code (IaC) tool that supports multiple cloud providers. It uses declarative configuration to create, update, and destroy resources.

---

## Framework

### Step 1: Installation

```bash
# macOS
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Ubuntu/Debian
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# Verify
terraform version

# Enable autocomplete
terraform -install-autocomplete
```

### Step 2: Project Structure

```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── production/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ec2/
│   ├── rds/
│   └── lambda/
└── .terraform-version
```

### Step 3: Basic Configuration

```hcl
# main.tf
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "env/dev/terraform.tfstate"
    region         = "us-east-1"
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

```hcl
# variables.tf
variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, production)"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}
```

```hcl
# terraform.tfvars
project     = "my-app"
environment = "dev"
region      = "us-east-1"
vpc_cidr    = "10.0.0.0/16"
```

### Step 4: Resources

```hcl
# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project}-${var.environment}-vpc"
  }
}

# Subnets
resource "aws_subnet" "public" {
  count                   = length(var.availability_zones)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 4, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project}-${var.environment}-public-${count.index + 1}"
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index + 4)
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name = "${var.project}-${var.environment}-private-${count.index + 1}"
    Type = "private"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project}-${var.environment}-igw"
  }
}

# Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project}-${var.environment}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
```

### Step 5: Terraform Commands

```bash
# Initialize
terraform init

# Format code
terraform fmt -recursive

# Validate configuration
terraform validate

# Plan changes
terraform plan
terraform plan -out=tfplan           # Save plan
terraform plan -var="environment=prod"  # Override variable

# Apply changes
terraform apply
terraform apply tfplan               # Apply saved plan
terraform apply -auto-approve        # Skip confirmation

# Destroy resources
terraform destroy
terraform destroy -target=aws_instance.web  # Specific resource

# State management
terraform state list                 # List resources
terraform state show aws_instance.web   # Show resource details
terraform state mv old_name new_name     # Rename resource
terraform state rm resource_name         # Remove from state

# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Output values
terraform output
terraform output vpc_id
```

### Step 6: Outputs

```hcl
# outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "instance_public_ip" {
  description = "EC2 public IP"
  value       = aws_instance.web.public_ip
  sensitive   = false
}
```

---

## Templates

### Module Structure

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support

  tags = merge(
    var.tags,
    {
      Name = var.name
    }
  )
}

# modules/vpc/variables.tf
variable "name" {
  description = "VPC name"
  type        = string
}

variable "cidr_block" {
  description = "VPC CIDR block"
  type        = string
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames"
  type        = bool
  default     = true
}

variable "enable_dns_support" {
  description = "Enable DNS support"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply"
  type        = map(string)
  default     = {}
}

# modules/vpc/outputs.tf
output "vpc_id" {
  value = aws_vpc.this.id
}

output "vpc_cidr_block" {
  value = aws_vpc.this.cidr_block
}
```

```hcl
# Using the module
module "vpc" {
  source = "../../modules/vpc"

  name       = "${var.project}-${var.environment}"
  cidr_block = var.vpc_cidr

  tags = {
    Environment = var.environment
  }
}

# Access outputs
resource "aws_subnet" "public" {
  vpc_id = module.vpc.vpc_id
  # ...
}
```

### Remote State

```hcl
# Backend configuration
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "env/dev/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# Access remote state from another config
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "network/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use outputs from remote state
resource "aws_instance" "web" {
  subnet_id = data.terraform_remote_state.network.outputs.public_subnet_ids[0]
  # ...
}
```

### Data Sources

```hcl
# Get latest Amazon Linux AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

# Get current AWS account
data "aws_caller_identity" "current" {}

# Get availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Use in resources
resource "aws_instance" "web" {
  ami               = data.aws_ami.amazon_linux.id
  availability_zone = data.aws_availability_zones.available.names[0]
}
```

---

## Examples

### Conditional Resources

```hcl
variable "create_bastion" {
  type    = bool
  default = false
}

resource "aws_instance" "bastion" {
  count = var.create_bastion ? 1 : 0

  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"
}

# For each
variable "instances" {
  type = map(object({
    instance_type = string
    ami           = string
  }))
}

resource "aws_instance" "app" {
  for_each = var.instances

  ami           = each.value.ami
  instance_type = each.value.instance_type

  tags = {
    Name = each.key
  }
}
```

### Dynamic Blocks

```hcl
variable "ingress_rules" {
  type = list(object({
    port        = number
    cidr_blocks = list(string)
  }))
  default = [
    { port = 22, cidr_blocks = ["10.0.0.0/8"] },
    { port = 80, cidr_blocks = ["0.0.0.0/0"] },
    { port = 443, cidr_blocks = ["0.0.0.0/0"] },
  ]
}

resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = aws_vpc.main.id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = ingress.value.cidr_blocks
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---

## Common Mistakes

1. **No remote state** - Local state not shared, lost easily
2. **Hardcoded values** - Use variables for flexibility
3. **No state locking** - DynamoDB table for S3 backend
4. **Large state files** - Split into multiple states
5. **No version pinning** - Pin provider and Terraform versions

---

## Checklist

- [ ] Remote backend configured
- [ ] State locking enabled
- [ ] Provider versions pinned
- [ ] Terraform version specified
- [ ] Variables with descriptions
- [ ] Outputs for important values
- [ ] Modules for reusable code
- [ ] terraform fmt before commit

---

## Next Steps

- M-DO-010: Infrastructure Patterns
- M-DO-007: AWS EC2
- M-DO-005: Kubernetes Basics

---

*Methodology M-DO-009 v1.0*
