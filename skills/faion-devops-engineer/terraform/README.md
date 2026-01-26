# Terraform Reference

Infrastructure as Code with Terraform: HCL syntax, providers, modules, state management, workspaces, and security.

## Quick Reference

### Commands

| Command | Description |
|---------|-------------|
| `terraform init` | Initialize working directory |
| `terraform plan` | Preview changes |
| `terraform apply` | Apply changes |
| `terraform destroy` | Destroy infrastructure |
| `terraform fmt` | Format configuration |
| `terraform validate` | Validate configuration |
| `terraform output` | Show outputs |
| `terraform console` | Interactive console |
| `terraform state list` | List resources in state |
| `terraform import` | Import existing resources |

### File Structure

```
project/
├── main.tf           # Main resources
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── versions.tf       # Provider versions
├── providers.tf      # Provider configuration
├── locals.tf         # Local values
├── data.tf           # Data sources
├── terraform.tfvars  # Variable values (gitignored)
└── modules/          # Local modules
    └── vpc/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

### Provider Configuration

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "project/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      ManagedBy   = "terraform"
      Project     = var.project_name
      Environment = var.environment
    }
  }
}
```

---

## HCL Syntax

### Variables

```hcl
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"

  validation {
    condition     = can(regex("^t[23]\\.", var.instance_type))
    error_message = "Instance type must be t2 or t3 family."
  }
}

variable "ports" {
  type = list(object({
    port     = number
    protocol = string
  }))
  default = []
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

### Locals

```hcl
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }

  name_prefix = "${var.project_name}-${var.environment}"
}
```

### Outputs

```hcl
output "instance_ip" {
  description = "Public IP of the instance"
  value       = aws_instance.web.public_ip
}

output "database_endpoint" {
  description = "Database connection endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}
```

### Expressions

```hcl
# Conditional
instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"

# For expression (list)
instance_ids = [for i in aws_instance.web : i.id]

# For expression (map)
instance_map = {for i in aws_instance.web : i.tags.Name => i.id}

# Splat expression
all_ips = aws_instance.web[*].public_ip

# Dynamic blocks
dynamic "ingress" {
  for_each = var.ingress_rules
  content {
    from_port   = ingress.value.from_port
    to_port     = ingress.value.to_port
    protocol    = ingress.value.protocol
    cidr_blocks = ingress.value.cidr_blocks
  }
}
```

### Built-in Functions

| Category | Functions |
|----------|-----------|
| String | `upper`, `lower`, `replace`, `split`, `join`, `format`, `trimspace` |
| Collection | `length`, `element`, `lookup`, `merge`, `concat`, `flatten`, `distinct`, `contains`, `keys`, `values` |
| Filesystem | `file`, `fileexists`, `templatefile`, `basename`, `dirname` |
| Numeric | `max`, `min`, `ceil`, `floor`, `abs` |
| Encoding | `base64encode`, `base64decode`, `jsonencode`, `jsondecode`, `yamlencode`, `yamldecode` |
| Hash | `md5`, `sha256`, `uuid` |
| Date/Time | `timestamp`, `formatdate` |

---

## Module Structure

### Standard Layout (HashiCorp Recommended)

```
modules/
└── vpc/
    ├── main.tf           # Primary resources
    ├── variables.tf      # Input variables
    ├── outputs.tf        # Output values
    ├── versions.tf       # Provider constraints
    ├── README.md         # Documentation
    ├── examples/         # Usage examples
    │   └── complete/
    │       └── main.tf
    └── modules/          # Nested modules
        └── subnets/
            ├── main.tf
            ├── variables.tf
            └── outputs.tf
```

### Module Design Principles

| Principle | Description |
|-----------|-------------|
| Single Responsibility | Each module performs one function well |
| Loose Coupling | Modules can evolve independently |
| Clear Interfaces | Well-defined inputs/outputs |
| No Hardcoding | All values configurable via variables |
| Documentation | README with examples |

### Module Call

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${local.name_prefix}-vpc"
  cidr = var.vpc_cidr

  azs             = data.aws_availability_zones.available.names
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway = true
  single_nat_gateway = var.environment != "prod"

  tags = local.common_tags
}
```

---

## State Management

### Remote Backend (S3)

```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "project/env/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### State Locking

| Backend | Locking Mechanism |
|---------|-------------------|
| S3 | DynamoDB table |
| GCS | Built-in |
| Azure Blob | Built-in |
| Terraform Cloud | Built-in |

### State Commands

```bash
# List resources
terraform state list

# Show resource details
terraform state show aws_instance.web

# Move resource (rename)
terraform state mv aws_instance.web aws_instance.app

# Remove from state (without destroying)
terraform state rm aws_instance.web

# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Pull remote state locally
terraform state pull > terraform.tfstate.backup
```

### State Isolation Strategy

| Strategy | Use Case |
|----------|----------|
| Per Environment | `envs/dev/`, `envs/staging/`, `envs/prod/` |
| Per Component | `network/`, `compute/`, `database/` |
| Per Region | `us-east-1/`, `eu-west-1/` |

---

## Workspaces

### Basic Usage

```bash
# List workspaces
terraform workspace list

# Create workspace
terraform workspace new dev

# Select workspace
terraform workspace select prod

# Show current workspace
terraform workspace show

# Delete workspace
terraform workspace delete dev
```

### Workspace-Aware Configuration

```hcl
locals {
  environment = terraform.workspace

  instance_count = {
    dev     = 1
    staging = 2
    prod    = 3
  }
}

resource "aws_instance" "web" {
  count         = local.instance_count[local.environment]
  instance_type = local.environment == "prod" ? "t3.large" : "t3.micro"

  tags = {
    Environment = local.environment
  }
}
```

### Workspace Limitations

| Limitation | Solution |
|------------|----------|
| Shared backend config | Use separate directories per environment |
| No visual distinction | Implement naming conventions |
| State drift between workspaces | Regular drift detection |
| Not suitable for prod isolation | Use separate state files |

---

## Security

### Secrets Management

```hcl
# AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "myapp/database/password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}

# HashiCorp Vault
data "vault_generic_secret" "db" {
  path = "secret/database"
}

resource "aws_db_instance" "main" {
  password = data.vault_generic_secret.db.data["password"]
}
```

### IAM Best Practices

```hcl
# Use IAM roles, not users
resource "aws_iam_role" "terraform" {
  name = "terraform-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

# Least privilege policy
resource "aws_iam_role_policy" "terraform" {
  role = aws_iam_role.terraform.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "ec2:Describe*",
        "ec2:CreateTags",
        "ec2:RunInstances",
        "ec2:TerminateInstances"
      ]
      Resource = "*"
      Condition = {
        StringEquals = {
          "aws:RequestedRegion" = var.allowed_regions
        }
      }
    }]
  })
}
```

### Security Scanning Tools

| Tool | Purpose |
|------|---------|
| tfsec | Static analysis for Terraform |
| Checkov | Policy-as-code scanning |
| Terrascan | Compliance scanning |
| Snyk IaC | Vulnerability scanning |

### State File Security

| Practice | Implementation |
|----------|----------------|
| Encryption at rest | S3 SSE, GCS encryption |
| Encryption in transit | HTTPS only |
| Access control | IAM policies, bucket policies |
| Audit logging | S3 access logs, CloudTrail |
| No secrets in state | Use external secret managers |

---

## Related Files

| File | Content |
|------|---------|
| [checklist.md](checklist.md) | Pre-deployment checklist |
| [examples.md](examples.md) | Code examples |
| [templates.md](templates.md) | Project templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for Terraform |

## Sources

- [Terraform Documentation](https://developer.hashicorp.com/terraform)
- [Standard Module Structure](https://developer.hashicorp.com/terraform/language/modules/develop/structure)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [AWS Terraform Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-aws-provider-best-practices/)
- [Google Cloud Terraform Best Practices](https://cloud.google.com/docs/terraform/best-practices/)
- [Spacelift Terraform Security](https://spacelift.io/blog/terraform-security)
- [Spacelift State Management](https://spacelift.io/blog/terraform-state)
