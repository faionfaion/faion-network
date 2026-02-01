# Terraform Modules

Technical reference for Terraform module development, versioning, composition patterns, and best practices.

---

## Overview

Terraform modules are self-contained packages of Terraform configurations that encapsulate reusable infrastructure components. Well-designed modules reduce code duplication, improve maintainability, and enable team collaboration at scale.

**Key Principles:**
- Single responsibility (one module = one purpose)
- Clear inputs/outputs contract
- Semantic versioning
- Comprehensive documentation
- Testability

---

## Module Structure

### Standard Layout

```
modules/
├── vpc/
│   ├── main.tf           # Resources
│   ├── variables.tf      # Input variables
│   ├── outputs.tf        # Output values
│   ├── versions.tf       # Provider requirements
│   ├── locals.tf         # Local values (optional)
│   ├── data.tf           # Data sources (optional)
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

### File Responsibilities

| File | Purpose |
|------|---------|
| `main.tf` | Primary resources and logic |
| `variables.tf` | Input variable definitions |
| `outputs.tf` | Output value definitions |
| `versions.tf` | Terraform and provider version constraints |
| `locals.tf` | Computed local values |
| `data.tf` | Data source lookups |
| `README.md` | Module documentation |

---

## Module Types

### Root Module
The main working directory where `terraform apply` runs. Calls child modules.

### Child Module
Reusable module called by root or other modules. Located in `modules/` directory or external registry.

### Published Module
Module shared via Terraform Registry, GitHub, or private registry. Follows naming convention: `terraform-<PROVIDER>-<NAME>`.

---

## Versioning

### Semantic Versioning (SemVer)

| Version | Meaning |
|---------|---------|
| Major (X.0.0) | Breaking changes requiring consumer updates |
| Minor (0.X.0) | New features, backward-compatible |
| Patch (0.0.X) | Bug fixes, no behavior changes |

### Version Constraints

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"      # >= 5.0.0, < 6.0.0 (recommended)
}

module "s3" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = ">= 4.0, < 5.0"  # Explicit range
}

module "network" {
  source = "github.com/org/terraform-modules//network?ref=v1.2.3"
}
```

### CHANGELOG.md

Maintain changelog documenting all version changes:

```markdown
# Changelog

## [2.1.0] - 2025-01-15
### Added
- Support for IPv6 CIDR blocks
- New output `ipv6_cidr_block`

### Changed
- Default instance type updated to t3.medium

## [2.0.0] - 2024-11-01
### Breaking Changes
- Renamed variable `enable_nat` to `nat_gateway_enabled`
- Removed deprecated `single_nat_gateway` variable
```

---

## Composition Patterns

### Flat Composition
Direct module calls from root, suitable for simple architectures.

```hcl
module "vpc"      { source = "./modules/vpc" }
module "ec2"      { source = "./modules/ec2" }
module "rds"      { source = "./modules/rds" }
```

### Hierarchical Composition
Modules calling other modules, creating layers of abstraction.

```hcl
# modules/app-stack/main.tf
module "network" { source = "../network" }
module "compute" { source = "../compute" }
module "database" { source = "../database" }
```

### Factory Pattern
Dynamic module instantiation using `for_each`.

```hcl
module "microservices" {
  source   = "./modules/ecs-service"
  for_each = var.services

  name        = each.key
  image       = each.value.image
  cpu         = each.value.cpu
  memory      = each.value.memory
  replicas    = each.value.replicas
}
```

---

## Best Practices

### Design Principles

1. **Single Responsibility** - One module, one purpose (VPC, not VPC+ECS+RDS)
2. **Avoid Mega-Modules** - Smaller modules reduce blast radius
3. **Loose Coupling** - Modules should evolve independently
4. **Explicit Dependencies** - Use outputs/inputs, not implicit references

### Variable Guidelines

- Provide sensible defaults where possible
- Use validation blocks for input constraints
- Document all variables with descriptions
- Use `sensitive = true` for secrets

### Output Guidelines

- Export IDs, ARNs, and connection strings
- Document all outputs
- Use `sensitive = true` for secret outputs

### Testing

- Run `terraform validate` on every change
- Use `terraform plan` to verify expected changes
- Implement automated tests with `terraform test` or Terratest
- Add pre-commit hooks for `terraform fmt`

### Security

- Never hardcode secrets in modules
- Use secret managers (Vault, AWS Secrets Manager)
- Implement policy-as-code (Sentinel, OPA)
- Run security scanners (Checkov, tfsec)

---

## Project Layout

### Recommended Structure

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
│   └── prod/
├── modules/
│   ├── vpc/
│   ├── ec2/
│   ├── rds/
│   └── ecs/
├── global/
│   ├── iam/
│   └── dns/
└── README.md
```

### Environment Separation

Use `.tfvars` files or workspaces for environment differences:

```bash
terraform apply -var-file="environments/prod.tfvars"
```

---

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Module development checklist |
| [examples.md](examples.md) | Code examples |
| [templates.md](templates.md) | Module templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for module generation |

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Module interface design | opus | Architecture decision |
| Module versioning strategy | sonnet | Release management |
| Input validation | sonnet | Pattern implementation |

## Sources

- [HashiCorp: Module Creation Pattern](https://developer.hashicorp.com/terraform/tutorials/modules/pattern-module-creation)
- [HashiCorp: How to Write and Rightsize Modules](https://www.hashicorp.com/en/blog/how-to-write-and-rightsize-terraform-modules)
- [Google Cloud: Terraform Best Practices](https://docs.cloud.google.com/docs/terraform/best-practices/general-style-structure)
- [Spacelift: Terraform Modules at Scale](https://spacelift.io/blog/terraform-modules-at-scale)
- [DevOpsCube: Module Best Practices](https://devopscube.com/terraform-module-best-practices/)
- [AWS: Terraform Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-aws-provider-best-practices/structure.html)

---

*Terraform Modules Reference*
*Part of faion-infrastructure-engineer skill*
