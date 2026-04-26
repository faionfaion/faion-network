# Terraform Modules Examples

Production-ready code examples for module development and usage.

---

## Module Definition Examples

### VPC Module

**modules/vpc/main.tf**

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
  vpc_id = aws_vpc.main.id

  tags = merge(var.tags, {
    Name = "${var.name}-igw"
  })
}

resource "aws_nat_gateway" "main" {
  count         = var.enable_nat_gateway ? 1 : 0
  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public[0].id

  tags = merge(var.tags, {
    Name = "${var.name}-nat"
  })

  depends_on = [aws_internet_gateway.main]
}

resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? 1 : 0
  domain = "vpc"

  tags = merge(var.tags, {
    Name = "${var.name}-nat-eip"
  })
}
```

**modules/vpc/variables.tf**

```hcl
variable "name" {
  description = "Name prefix for all resources"
  type        = string

  validation {
    condition     = length(var.name) <= 32
    error_message = "Name must be 32 characters or less."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be a valid CIDR block."
  }
}

variable "public_subnets" {
  description = "List of public subnet CIDRs"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnets" {
  description = "List of private subnet CIDRs"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
```

**modules/vpc/outputs.tf**

```hcl
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

output "nat_gateway_id" {
  description = "ID of the NAT Gateway"
  value       = var.enable_nat_gateway ? aws_nat_gateway.main[0].id : null
}
```

**modules/vpc/versions.tf**

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

---

## Module Usage Examples

### Local Module

```hcl
module "vpc" {
  source = "./modules/vpc"

  name               = "production"
  vpc_cidr           = "10.0.0.0/16"
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets    = ["10.0.10.0/24", "10.0.11.0/24"]
  availability_zones = ["us-east-1a", "us-east-1b"]
  enable_nat_gateway = true

  tags = {
    Environment = "production"
    Project     = "myapp"
    ManagedBy   = "terraform"
  }
}
```

### Registry Module

```hcl
module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 4.0"

  bucket = "my-unique-bucket-name"

  versioning = {
    enabled = true
  }

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

### GitHub Module

```hcl
module "network" {
  source = "github.com/org/terraform-modules//network?ref=v1.2.3"

  vpc_cidr           = "10.0.0.0/16"
  environment        = "production"
  availability_zones = ["us-east-1a", "us-east-1b"]
}
```

---

## Composition Patterns

### Factory Pattern with for_each

```hcl
variable "services" {
  type = map(object({
    image    = string
    cpu      = number
    memory   = number
    replicas = number
    port     = number
  }))
}

module "ecs_services" {
  source   = "./modules/ecs-service"
  for_each = var.services

  name       = each.key
  cluster_id = module.ecs_cluster.id
  image      = each.value.image
  cpu        = each.value.cpu
  memory     = each.value.memory
  replicas   = each.value.replicas
  port       = each.value.port

  subnet_ids         = module.vpc.private_subnet_ids
  security_group_ids = [module.security_groups.ecs_tasks_sg_id]
}
```

**Usage:**

```hcl
services = {
  api = {
    image    = "myapp/api:latest"
    cpu      = 256
    memory   = 512
    replicas = 2
    port     = 8080
  }
  worker = {
    image    = "myapp/worker:latest"
    cpu      = 512
    memory   = 1024
    replicas = 3
    port     = 8081
  }
}
```

### Hierarchical Composition

```hcl
# modules/app-stack/main.tf
module "network" {
  source = "../network"

  name               = var.name
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
}

module "database" {
  source = "../rds"

  name              = var.name
  subnet_ids        = module.network.private_subnet_ids
  security_group_id = module.network.database_sg_id
  engine            = "postgres"
  engine_version    = "15.4"
}

module "compute" {
  source = "../ecs"

  name       = var.name
  subnet_ids = module.network.private_subnet_ids
  database_url = module.database.connection_string
}
```

---

## DRY Patterns

### Locals for Common Tags

```hcl
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Owner       = var.owner
    CostCenter  = var.cost_center
  }
}

resource "aws_instance" "web" {
  # ...
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-web"
    Role = "webserver"
  })
}
```

### Environment Configuration Map

```hcl
variable "environment" {
  type = string
}

locals {
  env_config = {
    dev = {
      instance_count = 1
      instance_type  = "t3.micro"
      enable_backup  = false
      multi_az       = false
    }
    staging = {
      instance_count = 2
      instance_type  = "t3.small"
      enable_backup  = true
      multi_az       = false
    }
    prod = {
      instance_count = 4
      instance_type  = "t3.large"
      enable_backup  = true
      multi_az       = true
    }
  }

  config = local.env_config[var.environment]
}

resource "aws_instance" "web" {
  count         = local.config.instance_count
  instance_type = local.config.instance_type
  # ...
}
```

---

## Workspace-Based Configuration

```hcl
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

  tags = {
    Environment = local.environment
  }
}
```

---

## Testing Examples

### terraform test (Native)

**tests/vpc.tftest.hcl**

```hcl
run "vpc_creation" {
  command = plan

  variables {
    name               = "test"
    vpc_cidr           = "10.0.0.0/16"
    availability_zones = ["us-east-1a", "us-east-1b"]
  }

  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR block is incorrect"
  }

  assert {
    condition     = length(aws_subnet.public) == 2
    error_message = "Expected 2 public subnets"
  }
}

run "vpc_validation" {
  command = plan

  variables {
    name               = "test"
    vpc_cidr           = "invalid"
    availability_zones = ["us-east-1a"]
  }

  expect_failures = [var.vpc_cidr]
}
```

---

## CI/CD Pipeline

**.github/workflows/terraform.yml**

```yaml
name: Terraform

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0

      - name: Format Check
        run: terraform fmt -check -recursive

      - name: Init
        run: terraform init -backend=false

      - name: Validate
        run: terraform validate

      - name: TFLint
        uses: terraform-linters/setup-tflint@v4
      - run: tflint --init && tflint

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Checkov
        uses: bridgecrewio/checkov-action@v12
        with:
          directory: .
          framework: terraform

  plan:
    needs: [validate, security]
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform plan -out=tfplan
      - uses: actions/upload-artifact@v4
        with:
          name: tfplan
          path: tfplan

  apply:
    needs: [validate, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform apply -auto-approve
```

---

*Terraform Modules Examples*
*Part of faion-infrastructure-engineer skill*
