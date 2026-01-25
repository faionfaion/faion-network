# Terraform Modules

Technical reference for Terraform module development, usage, and best practices.

---

## Module Structure

```
modules/
├── vpc/
│   ├── main.tf           # Resources
│   ├── variables.tf      # Input variables
│   ├── outputs.tf        # Output values
│   ├── versions.tf       # Provider requirements
│   └── README.md         # Documentation
├── ec2/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── rds/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

---

## Module Definition

### modules/vpc/main.tf

```hcl
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

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(var.tags, {
    Name = "${var.name}-igw"
  })
}
```

### modules/vpc/variables.tf

```hcl
variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnets" {
  description = "List of public subnet CIDRs"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
```

### modules/vpc/outputs.tf

```hcl
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}
```

---

## Module Usage

### Local Module

```hcl
module "vpc" {
  source = "./modules/vpc"

  name               = "production"
  vpc_cidr           = "10.0.0.0/16"
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24"]
  availability_zones = ["us-east-1a", "us-east-1b"]

  tags = {
    Environment = "production"
    Project     = "myapp"
  }
}
```

### Registry Module

```hcl
module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 4.0"

  bucket = "my-unique-bucket-name"
  acl    = "private"

  versioning = {
    enabled = true
  }
}
```

### GitHub Module

```hcl
module "network" {
  source = "github.com/org/terraform-modules//network?ref=v1.0.0"

  vpc_cidr = "10.0.0.0/16"
}
```

### Accessing Module Outputs

```hcl
resource "aws_instance" "web" {
  subnet_id = module.vpc.public_subnet_ids[0]
  # ...
}
```

---

## DRY Principles

### Use Modules for Reusable Components

```hcl
module "web_server" {
  source = "./modules/ec2"

  for_each = toset(["web-1", "web-2", "web-3"])

  name          = each.key
  instance_type = var.instance_type
  subnet_id     = module.vpc.public_subnet_ids[0]
}
```

### Use Locals for Repeated Values

```hcl
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Owner       = var.owner
  }
}
```

### Use Variables for Configurable Values

```hcl
variable "environments" {
  type = map(object({
    instance_count = number
    instance_type  = string
    enable_backup  = bool
  }))

  default = {
    dev = {
      instance_count = 1
      instance_type  = "t3.micro"
      enable_backup  = false
    }
    prod = {
      instance_count = 3
      instance_type  = "t3.large"
      enable_backup  = true
    }
  }
}
```

---

## Project Structure

### Recommended Layout

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   │   └── ...
│   └── prod/
│       └── ...
├── modules/
│   ├── vpc/
│   ├── ec2/
│   ├── rds/
│   └── ...
├── global/
│   ├── iam/
│   └── dns/
└── README.md
```

---

## Workspaces

### Workspace Commands

```bash
# List workspaces
terraform workspace list

# Create new workspace
terraform workspace new staging

# Select workspace
terraform workspace select production

# Show current workspace
terraform workspace show

# Delete workspace
terraform workspace delete staging
```

### Workspace-Based Configuration

```hcl
# Use workspace name in configuration
locals {
  environment = terraform.workspace

  instance_count = {
    default     = 1
    development = 1
    staging     = 2
    production  = 4
  }

  instance_type = {
    default     = "t3.micro"
    development = "t3.micro"
    staging     = "t3.small"
    production  = "t3.large"
  }
}

resource "aws_instance" "web" {
  count         = local.instance_count[local.environment]
  instance_type = local.instance_type[local.environment]
  # ...

  tags = {
    Environment = local.environment
  }
}
```

### Environment-Specific Variables

```hcl
# terraform.tfvars (default)
project_name = "myapp"

# dev.tfvars
environment    = "development"
instance_count = 1
instance_type  = "t3.micro"

# prod.tfvars
environment    = "production"
instance_count = 4
instance_type  = "t3.large"
```

```bash
# Apply with specific vars file
terraform apply -var-file="environments/prod.tfvars"
```

---

## Testing and Validation

```bash
# Format check
terraform fmt -check -recursive

# Validate configuration
terraform validate

# Plan with detailed exit codes
terraform plan -detailed-exitcode

# Use checkov for security scanning
checkov -d .

# Use tflint for linting
tflint --init
tflint

# Use terraform-docs for documentation
terraform-docs markdown table . > README.md
```

---

## CI/CD Pipeline Example

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  terraform:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0

      - name: Terraform Format
        run: terraform fmt -check -recursive

      - name: Terraform Init
        run: terraform init

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        run: terraform plan -out=tfplan

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve tfplan
```

---

*Terraform Modules Reference*
*Part of faion-devops-engineer skill*

## Sources

- [Terraform Modules](https://www.terraform.io/language/modules)
- [Module Development](https://www.terraform.io/language/modules/develop)
- [Publishing Modules](https://www.terraform.io/registry/modules/publish)
- [Module Composition](https://www.terraform.io/language/modules/develop/composition)
- [Module Testing](https://www.terraform.io/language/modules/testing-experiment)
