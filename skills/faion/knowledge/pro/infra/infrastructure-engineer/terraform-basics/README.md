# Terraform Basics

Technical reference for Terraform fundamentals: HCL syntax, providers, resources, data sources, and core concepts.

## Overview

Terraform is an Infrastructure as Code (IaC) tool that uses a declarative language to describe desired infrastructure state. It manages the full lifecycle: create, update, and delete resources across multiple cloud providers.

## Core Concepts

### Infrastructure as Code (IaC)

| Concept | Description |
|---------|-------------|
| Declarative | Describe desired end-state, Terraform determines how to achieve it |
| State | Terraform tracks infrastructure state in `terraform.tfstate` |
| Idempotent | Same configuration applied multiple times produces same result |
| Plan | Preview changes before applying |

### HCL Building Blocks

| Block Type | Purpose | Example |
|------------|---------|---------|
| `terraform` | Version constraints, backend config | `required_version = ">= 1.5.0"` |
| `provider` | Cloud provider configuration | AWS, GCP, Azure |
| `resource` | Infrastructure to create/manage | EC2 instance, S3 bucket |
| `data` | Read-only data sources | AMI lookup, AZ list |
| `variable` | Input parameters | Instance type, region |
| `output` | Exported values | Instance IP, DNS name |
| `locals` | Computed local values | Common tags, naming |
| `module` | Reusable configuration groups | VPC module, app module |

### Terraform Workflow

```
terraform init    →  Initialize, download providers
terraform plan    →  Preview changes (dry run)
terraform apply   →  Execute changes
terraform destroy →  Remove all resources
```

## Provider Configuration

Providers are plugins that interact with cloud platforms and services.

### Version Constraints

| Constraint | Meaning | Example |
|------------|---------|---------|
| `= 5.0.0` | Exact version | Only 5.0.0 |
| `>= 5.0` | Minimum version | 5.0 or higher |
| `~> 5.0` | Pessimistic constraint | 5.x but not 6.0 |
| `>= 5.0, < 6.0` | Range | Between 5.0 and 6.0 |

### Multi-Provider Setup

Use provider aliases for multi-region or multi-account deployments:
- Primary provider (no alias) for main resources
- Aliased providers for secondary regions/accounts
- Reference with `provider = aws.alias_name`

## Resources

Resources are the most important element in Terraform. Each resource block describes infrastructure objects.

### Meta-Arguments

| Argument | Purpose |
|----------|---------|
| `count` | Create multiple identical resources |
| `for_each` | Create resources from map/set |
| `depends_on` | Explicit dependency declaration |
| `provider` | Select non-default provider |
| `lifecycle` | Customize resource behavior |

### Lifecycle Rules

| Rule | Effect |
|------|--------|
| `create_before_destroy` | Create replacement before destroying |
| `prevent_destroy` | Block destruction (safety) |
| `ignore_changes` | Ignore external changes to attributes |
| `precondition` | Validate before creation |
| `postcondition` | Validate after creation |

## Data Sources

Data sources allow Terraform to read information from external sources without managing them.

### Common Use Cases

- Look up latest AMI ID
- Get available availability zones
- Read secrets from secret managers
- Query existing infrastructure

## State Management

State is critical for Terraform operation. Best practices:

| Practice | Description |
|----------|-------------|
| Remote backend | Store state in S3, GCS, or Terraform Cloud |
| State locking | Prevent concurrent modifications |
| Encryption | Encrypt state at rest (contains secrets) |
| Never commit | Add `*.tfstate*` to `.gitignore` |

## File Structure

Standard Terraform project organization:

```
project/
  versions.tf     # Terraform and provider versions
  providers.tf    # Provider configuration
  variables.tf    # Input variable definitions
  main.tf         # Main resource definitions
  outputs.tf      # Output value definitions
  locals.tf       # Local value computations
  data.tf         # Data source queries
  terraform.tfvars # Variable values (gitignored)
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `terraform init` | Initialize working directory |
| `terraform plan` | Preview changes |
| `terraform apply` | Apply changes |
| `terraform destroy` | Destroy infrastructure |
| `terraform fmt` | Format configuration files |
| `terraform validate` | Validate configuration |
| `terraform output` | Show output values |
| `terraform console` | Interactive expression evaluation |
| `terraform graph` | Generate dependency graph |
| `terraform state` | State manipulation commands |
| `terraform import` | Import existing resources |

## Related Methodologies

| Methodology | Focus |
|-------------|-------|
| [terraform-modules/](../terraform-modules/) | Module development, versioning |
| [terraform-state/](../terraform-state/) | Remote state, locking, import |
| [terraform/](../terraform/) | Advanced patterns, workspaces |
| [iac-basics/](../iac-basics/) | IaC principles, tool comparison |


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| HCL syntax review | haiku | Syntax checking |
| Provider configuration | haiku | Setup automation |
| Resource creation | sonnet | Infrastructure patterns |

## Sources

- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Language](https://www.terraform.io/language)
- [Terraform CLI](https://www.terraform.io/cli)
- [Terraform Registry](https://registry.terraform.io/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [HashiCorp Developer](https://developer.hashicorp.com/terraform)
- [Google Cloud Terraform Best Practices](https://cloud.google.com/docs/terraform/best-practices/general-style-structure)
- [AWS Terraform Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-aws-provider-best-practices/structure.html)

---

*Terraform Basics | Part of faion-infrastructure-engineer skill*
