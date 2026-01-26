# Terraform Templates

## Project Initialization

### .gitignore

```gitignore
# Terraform
.terraform/
*.tfstate
*.tfstate.*
crash.log
crash.*.log
*.tfvars
!example.tfvars
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Keep lock file
!.terraform.lock.hcl

# IDE
.idea/
*.swp
*.swo
.vscode/

# OS
.DS_Store
Thumbs.db

# Secrets
*.pem
*.key
.env
.env.*
```

### Directory Structure Generator

```bash
#!/bin/bash
# setup-terraform-project.sh

PROJECT_NAME=${1:-"infrastructure"}
ENVIRONMENTS=${2:-"dev staging prod"}

mkdir -p "${PROJECT_NAME}"/{environments,modules,tests,shared}

for env in $ENVIRONMENTS; do
  mkdir -p "${PROJECT_NAME}/environments/${env}"

  # Create skeleton files
  touch "${PROJECT_NAME}/environments/${env}"/{main.tf,variables.tf,outputs.tf,backend.tf}
  echo "# ${env^} Environment" > "${PROJECT_NAME}/environments/${env}/README.md"
done

# Shared providers
cat > "${PROJECT_NAME}/shared/providers.tf" << 'EOF'
# Shared provider configurations
# Import this in each environment
EOF

# Create module template
mkdir -p "${PROJECT_NAME}/modules/example"
touch "${PROJECT_NAME}/modules/example"/{main.tf,variables.tf,outputs.tf,versions.tf,README.md}

echo "Created project structure in ${PROJECT_NAME}/"
tree "${PROJECT_NAME}"
```

---

## Backend Templates

### AWS S3 Backend (Terraform 1.10+)

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket       = "COMPANY-terraform-state"
    key          = "ENVIRONMENT/terraform.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true  # S3 native locking
  }
}
```

### AWS S3 Backend (Legacy with DynamoDB)

```hcl
# backend.tf - For Terraform < 1.10
terraform {
  backend "s3" {
    bucket         = "COMPANY-terraform-state"
    key            = "ENVIRONMENT/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### GCS Backend

```hcl
# backend.tf
terraform {
  backend "gcs" {
    bucket = "COMPANY-terraform-state"
    prefix = "ENVIRONMENT"
  }
}
```

### Azure Backend

```hcl
# backend.tf
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstate${lower(var.environment)}"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
```

---

## Provider Templates

### AWS Provider

```hcl
# versions.tf
terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# providers.tf
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
      Project     = var.project_name
      Owner       = var.team_name
    }
  }
}

# For multi-region
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
      Project     = var.project_name
    }
  }
}
```

### GCP Provider

```hcl
# versions.tf
terraform {
  required_version = ">= 1.10.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }
}

# providers.tf
provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}
```

### Multi-Provider (AWS + Kubernetes)

```hcl
# versions.tf
terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.25"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.12"
    }
  }
}

# providers.tf
provider "aws" {
  region = var.aws_region
}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_name
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_name
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.cluster.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
    token                  = data.aws_eks_cluster_auth.cluster.token
  }
}
```

---

## Module Templates

### Standard Module Structure

```
modules/MODULE_NAME/
├── main.tf           # Resources
├── variables.tf      # Inputs
├── outputs.tf        # Outputs
├── versions.tf       # Provider requirements
├── locals.tf         # Local values (optional)
├── data.tf           # Data sources (optional)
├── README.md         # Documentation
└── examples/
    └── basic/
        ├── main.tf
        └── README.md
```

### Module README Template

```markdown
# MODULE_NAME

Brief description of what this module creates.

## Usage

\`\`\`hcl
module "example" {
  source = "../../modules/MODULE_NAME"

  project_name = "myproject"
  environment  = "prod"
  # ... other variables
}
\`\`\`

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.10.0 |
| aws | ~> 5.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| project_name | Project name for resource naming | string | - | yes |
| environment | Environment name | string | - | yes |

## Outputs

| Name | Description |
|------|-------------|
| resource_id | ID of the created resource |
| resource_arn | ARN of the created resource |

## Resources Created

- Resource 1
- Resource 2

## Examples

See [examples/](examples/) directory.
```

### Module versions.tf Template

```hcl
# versions.tf
terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}
```

### Module variables.tf Template

```hcl
# variables.tf

# Required variables
variable "project_name" {
  description = "Project name for resource naming"
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,20}$", var.project_name))
    error_message = "Project name must be lowercase, start with letter, 3-21 chars."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# Optional variables with defaults
variable "tags" {
  description = "Additional tags to apply to resources"
  type        = map(string)
  default     = {}
}

variable "enable_feature" {
  description = "Enable optional feature"
  type        = bool
  default     = false
}
```

### Module outputs.tf Template

```hcl
# outputs.tf

output "id" {
  description = "Resource ID"
  value       = aws_resource.main.id
}

output "arn" {
  description = "Resource ARN"
  value       = aws_resource.main.arn
}

output "endpoint" {
  description = "Resource endpoint"
  value       = aws_resource.main.endpoint
  sensitive   = true
}
```

---

## Test Templates

### Basic Test File

```hcl
# tests/module.tftest.hcl

variables {
  project_name = "test"
  environment  = "dev"
}

run "validate_inputs" {
  command = plan

  assert {
    condition     = var.project_name == "test"
    error_message = "Project name not set correctly"
  }
}

run "create_resources" {
  command = apply

  assert {
    condition     = output.id != ""
    error_message = "Resource ID should not be empty"
  }

  assert {
    condition     = can(regex("^arn:aws:", output.arn))
    error_message = "Resource ARN should be valid AWS ARN"
  }
}
```

### Test with Variables Override

```hcl
# tests/environments.tftest.hcl

run "dev_environment" {
  command = plan

  variables {
    project_name = "test"
    environment  = "dev"
  }

  assert {
    condition     = length(aws_nat_gateway.main) == 0
    error_message = "Dev should not have NAT gateway"
  }
}

run "prod_environment" {
  command = plan

  variables {
    project_name = "test"
    environment  = "prod"
  }

  assert {
    condition     = length(aws_nat_gateway.main) == 1
    error_message = "Prod should have NAT gateway"
  }
}
```

### Test with Helper Module

```hcl
# tests/with_helper.tftest.hcl

run "setup" {
  module {
    source = "./tests/setup"
  }
}

run "test_with_dependencies" {
  command = apply

  variables {
    vpc_id = run.setup.vpc_id
  }

  assert {
    condition     = output.security_group_id != ""
    error_message = "Security group should be created"
  }
}
```

---

## Environment Templates

### terraform.tfvars Template

```hcl
# terraform.tfvars - Environment-specific values
# DO NOT commit sensitive values

# Project
project_name = "myproject"
environment  = "prod"
team_name    = "platform"

# AWS
aws_region         = "eu-central-1"
availability_zones = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]

# Network
vpc_cidr = "10.0.0.0/16"

# EKS
eks_cluster_version = "1.29"
eks_node_groups = {
  general = {
    instance_types = ["t3.medium", "t3.large"]
    min_size       = 2
    max_size       = 10
    desired_size   = 3
    disk_size      = 50
    labels         = {}
    taints         = []
  }
  spot = {
    instance_types = ["t3.medium", "t3.large", "t3.xlarge"]
    min_size       = 0
    max_size       = 20
    desired_size   = 0
    disk_size      = 50
    labels = {
      "node-type" = "spot"
    }
    taints = [{
      key    = "spot"
      value  = "true"
      effect = "NO_SCHEDULE"
    }]
  }
}

# RDS
rds_config = {
  engine_version    = "16.1"
  instance_class    = "db.r6g.large"
  allocated_storage = 100
  multi_az          = true
}
```

### Main.tf Template for Environment

```hcl
# main.tf - Environment root module

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

  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.private_subnet_ids
  cluster_version    = var.eks_cluster_version
  node_groups        = var.eks_node_groups

  depends_on = [module.vpc]
}

module "rds" {
  source = "../../modules/rds"

  project_name   = var.project_name
  environment    = var.environment
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids
  engine_version = var.rds_config.engine_version
  instance_class = var.rds_config.instance_class
  multi_az       = var.rds_config.multi_az
  password       = var.rds_password

  depends_on = [module.vpc]
}
```

---

## Makefile Template

```makefile
# Makefile for Terraform operations

ENVIRONMENT ?= dev
TF_DIR = infrastructure/environments/$(ENVIRONMENT)

.PHONY: init plan apply destroy fmt validate test clean

init:
	cd $(TF_DIR) && terraform init

plan:
	cd $(TF_DIR) && terraform plan -out=tfplan

apply:
	cd $(TF_DIR) && terraform apply tfplan

destroy:
	cd $(TF_DIR) && terraform destroy

fmt:
	terraform fmt -recursive infrastructure/

validate:
	cd $(TF_DIR) && terraform validate

test:
	cd infrastructure/modules && find . -name "*.tftest.hcl" -execdir terraform test \;

clean:
	find . -type d -name ".terraform" -exec rm -rf {} +
	find . -name "*.tfplan" -delete
	find . -name "tfplan" -delete

# Environment-specific targets
dev:
	$(MAKE) ENVIRONMENT=dev plan

staging:
	$(MAKE) ENVIRONMENT=staging plan

prod:
	$(MAKE) ENVIRONMENT=prod plan

# Shortcuts
p: plan
a: apply
d: destroy
```
