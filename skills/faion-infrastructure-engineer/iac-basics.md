---
id: iac-basics
name: "Terraform IaC Basics"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Terraform IaC Basics

## Overview

Terraform is an Infrastructure as Code (IaC) tool that enables declarative provisioning of cloud resources across multiple providers. It uses HashiCorp Configuration Language (HCL) to define infrastructure, tracks state, and applies changes through a plan-apply workflow.

## When to Use

- Provisioning cloud infrastructure (AWS, GCP, Azure)
- Managing multi-cloud or hybrid environments
- Creating reproducible infrastructure
- Implementing GitOps for infrastructure
- Managing Kubernetes cluster infrastructure

## Key Concepts

| Concept | Description |
|---------|-------------|
| Provider | Plugin for interacting with APIs (AWS, GCP, etc.) |
| Resource | Infrastructure object managed by Terraform |
| Data Source | Read-only reference to existing infrastructure |
| Module | Reusable collection of resources |
| State | Mapping between config and real-world resources |
| Backend | Storage location for state file |
| Workspace | Named state environments |

### Terraform Workflow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Write   │ →  │   Plan   │ →  │  Apply   │ →  │  Manage  │
│   HCL    │    │  Review  │    │  Create  │    │  Update  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

## Implementation

### Project Structure

```
infrastructure/
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
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks/
│   ├── rds/
│   └── s3/
└── shared/
    └── providers.tf
```

### Backend Configuration (backend.tf)

```hcl
terraform {
  required_version = ">= 1.5.0"

  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "environments/prod/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"

    # Role assumption for cross-account access
    # role_arn = "arn:aws:iam::123456789012:role/TerraformRole"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
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

### Variables (variables.tf)

```hcl
variable "environment" {
  description = "Environment name (dev, staging, prod)"
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
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
}

variable "eks_cluster_version" {
  description = "Kubernetes version for EKS cluster"
  type        = string
  default     = "1.28"
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

variable "rds_config" {
  description = "RDS configuration"
  type = object({
    engine_version    = string
    instance_class    = string
    allocated_storage = number
    multi_az          = bool
  })
  default = {
    engine_version    = "16.1"
    instance_class    = "db.t3.medium"
    allocated_storage = 100
    multi_az          = true
  }
}
```

### Outputs (outputs.tf)

```hcl
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
  sensitive   = true
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.db_endpoint
}

output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.app_data.id
}

output "kubeconfig_command" {
  description = "Command to update kubeconfig"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}"
}
```

### Terraform Commands

```bash
# Initialize
terraform init

# Initialize with backend migration
terraform init -migrate-state

# Format code
terraform fmt -recursive

# Validate configuration
terraform validate

# Plan changes
terraform plan -out=tfplan

# Plan for specific environment
terraform plan -var-file=terraform.tfvars -out=tfplan

# Apply changes
terraform apply tfplan

# Apply with auto-approve (CI/CD)
terraform apply -auto-approve -var-file=terraform.tfvars

# Destroy infrastructure
terraform destroy

# Import existing resource
terraform import aws_s3_bucket.example bucket-name

# State management
terraform state list
terraform state show aws_s3_bucket.app_data
terraform state mv aws_s3_bucket.old aws_s3_bucket.new
terraform state rm aws_s3_bucket.removed

# Workspace management
terraform workspace list
terraform workspace new staging
terraform workspace select prod

# Output values
terraform output
terraform output -json > outputs.json
```

## Best Practices

1. **Use remote state** - Store state in S3/GCS with locking (DynamoDB/GCS)
2. **Organize with modules** - Create reusable, tested modules
3. **Use workspaces or directories** - Separate environments properly
4. **Lock provider versions** - Pin exact versions in production
5. **Validate input variables** - Use validation blocks for inputs
6. **Use data sources** - Reference existing resources safely
7. **Enable encryption** - Encrypt state and all storage resources
8. **Tag all resources** - Use default_tags and consistent naming
9. **Plan before apply** - Always review plan output
10. **Version control everything** - Treat infrastructure as code

## Common Pitfalls

1. **Local state files** - State contains secrets and must be stored securely in remote backend with encryption.

2. **No state locking** - Concurrent applies can corrupt state. Always use locking mechanism.

3. **Hardcoded values** - Everything should be parameterized through variables.

4. **Large monolithic configs** - Break down into modules for maintainability and reusability.

5. **Missing depends_on** - Some implicit dependencies aren't detected. Use explicit depends_on when needed.

6. **No deletion protection** - Critical resources (RDS, S3) should have deletion protection in production.

## References

- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Terraform Module Registry](https://registry.terraform.io/)

## Sources

- [Infrastructure as Code Principles](https://www.hashicorp.com/resources/what-is-infrastructure-as-code)
- [Terraform Documentation](https://www.terraform.io/docs)
- [AWS CloudFormation](https://docs.aws.amazon.com/cloudformation/)
- [Pulumi Documentation](https://www.pulumi.com/docs/)
- [Ansible Documentation](https://docs.ansible.com/)
