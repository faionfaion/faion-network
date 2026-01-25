---
name: faion-terraform-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(terraform:*, ls:*, mkdir:*, cat:*)
---

# Terraform Skill

Technical skill for Infrastructure as Code with Terraform.

## Purpose

Provides comprehensive knowledge and patterns for Terraform infrastructure management, including HCL syntax, multi-cloud providers, modules, state management, and production best practices.

## Reference Files

| File | Content | Lines |
|------|---------|-------|
| [terraform-basics.md](terraform-basics.md) | HCL syntax, providers, resources, data sources, commands | ~650 |
| [terraform-modules.md](terraform-modules.md) | Module structure, usage, workspaces, testing | ~380 |
| [terraform-state.md](terraform-state.md) | State backends, operations, locking, remote state | ~230 |

**Total:** 3 focused files, ~1260 lines (was 1090 lines in single file)

---

## Quick Start

### Basic Commands

```bash
# Initialize and apply
terraform init
terraform plan
terraform apply

# Format and validate
terraform fmt -recursive
terraform validate

# State operations
terraform state list
terraform state show <resource>

# Workspace management
terraform workspace list
terraform workspace select prod
```

### Example Configuration

```hcl
# main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  tags = {
    Name = "web-server"
  }
}
```

---

## Detailed References

For comprehensive documentation, see:

- [terraform-basics.md](terraform-basics.md) - HCL syntax, providers, resources
- [terraform-modules.md](terraform-modules.md) - Module development and usage
- [terraform-state.md](terraform-state.md) - State management and backends

---

## Tool Selection

| Tool | Use Case |
|------|----------|
| Terraform | Multi-cloud IaC, complex infrastructure |
| Pulumi | IaC with programming languages (Python, TypeScript) |
| CloudFormation | AWS-only infrastructure |
| Ansible | Configuration management, simpler tasks |

---

## Integration

### Used By Agents

- `faion-devops-agent` - Infrastructure automation

### Related Skills

- `faion-aws-cli-skill` - AWS operations
- `faion-k8s-cli-skill` - Kubernetes management
- `faion-docker-skill` - Container operations

---

*Terraform Skill v1.1*
*Technical Skill (Layer 3)*
*Infrastructure as Code*

## Sources

- [Terraform Documentation](https://www.terraform.io/docs)
- [HashiCorp Learn - Terraform](https://learn.hashicorp.com/terraform)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
