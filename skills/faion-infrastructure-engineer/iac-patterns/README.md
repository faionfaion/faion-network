# Infrastructure as Code Patterns

## Overview

Patterns and best practices for writing maintainable, reusable, and testable Infrastructure as Code with focus on Terraform, OpenTofu, and Terragrunt.

**Domain:** Infrastructure Engineering
**Parent Skill:** [faion-infrastructure-engineer](../CLAUDE.md)

## Core Principles

| Principle | Description |
|-----------|-------------|
| **DRY** | Don't Repeat Yourself - use modules for reusable components |
| **Single Responsibility** | Each module does one thing well |
| **Composition over Inheritance** | Build complex infrastructure from simple modules |
| **Dependency Inversion** | Pass dependencies into modules, don't hardcode |
| **Immutable Infrastructure** | Replace rather than modify resources |

## Module Hierarchy

```
root-module/
├── main.tf              # Module composition
├── variables.tf         # Input parameters
├── outputs.tf           # Exposed values
├── versions.tf          # Provider constraints
├── locals.tf            # Computed values
└── modules/
    ├── base/            # Foundational resources (VPC, IAM)
    ├── core/            # Core infrastructure (EKS, RDS)
    └── app/             # Application-specific modules
```

## Pattern Categories

### 1. Module Patterns

| Pattern | Use Case |
|---------|----------|
| **Base Module** | Single resource type with sensible defaults |
| **Wrapper Module** | Org-specific defaults wrapping community modules |
| **Facade Module** | Simplified API hiding complex orchestration |
| **Factory Module** | Creates multiple similar resources from config |
| **Composite Module** | Combines multiple modules into a pattern |

### 2. Composition Patterns

| Pattern | Use Case |
|---------|----------|
| **Terramod** | Environment definitions compose from reusable modules |
| **Landing Zone** | Pre-configured environment framework for self-service |
| **Service Catalog** | Vetted patterns for complex multi-resource deployments |
| **Hub-Spoke** | Central shared services with isolated workloads |

### 3. DRY Patterns

| Pattern | Use Case |
|---------|----------|
| **Locals for Derivation** | Compute values from inputs |
| **Module Defaults** | Sensible defaults reduce required inputs |
| **Shared Variables** | Common variable definitions across modules |
| **Terragrunt DRY** | Generate common configurations automatically |

### 4. Testing Patterns

| Level | Tool | Purpose |
|-------|------|---------|
| **Static Analysis** | `terraform validate`, `tflint` | Syntax and structure |
| **Unit Testing** | Native `terraform test` | Module contracts |
| **Integration Testing** | Terratest, Kitchen-Terraform | Real resource validation |
| **Policy Testing** | OPA/Conftest, Sentinel | Compliance enforcement |

## Module Design Guidelines

### Do

- Keep modules focused and single-purpose
- Use semantic versioning (v1.0.0)
- Provide clear documentation and examples
- Pass dependencies as inputs (dependency inversion)
- Set sensible defaults for optional variables
- Expose minimal but sufficient outputs
- Include validation rules for inputs

### Don't

- Create "everything-my-app-needs" modules
- Hardcode environment-specific values
- Mix resources that change at different rates
- Skip output descriptions
- Neglect module versioning
- Copy-paste instead of modularizing

## State Management

| Practice | Implementation |
|----------|----------------|
| Remote State | S3 + DynamoDB (AWS), GCS + locking (GCP) |
| State Isolation | Separate state per environment/component |
| State Locking | Prevent concurrent modifications |
| State Encryption | Enable at-rest encryption |

## CI/CD Integration

```
PR Created → terraform fmt → terraform validate → tflint → plan → review
PR Merged → terraform apply → post-deploy tests → notify
```

## Files in This Reference

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation verification checklist |
| [examples.md](examples.md) | Production-ready code examples |
| [templates.md](templates.md) | Starter templates for common patterns |
| [llm-prompts.md](llm-prompts.md) | AI-assisted IaC development prompts |

## Related References

| Reference | Focus |
|-----------|-------|
| [terraform/](../terraform/) | Terraform basics and configuration |
| [terraform-modules/](../terraform-modules/) | Module development details |
| [terraform-state/](../terraform-state/) | State management patterns |

## Sources

- [HashiCorp Module Creation Pattern](https://developer.hashicorp.com/terraform/tutorials/modules/pattern-module-creation)
- [HashiCorp Module Composition](https://developer.hashicorp.com/terraform/language/modules/develop/composition)
- [HashiCorp Enterprise Patterns](https://developer.hashicorp.com/terraform/tutorials/recommended-patterns)
- [Google Cloud Terraform Testing Best Practices](https://cloud.google.com/docs/terraform/best-practices/testing)
- [Terratest Documentation](https://terratest.gruntwork.io/)
- [Spacelift IaC Architecture Patterns](https://spacelift.io/blog/iac-architecture-patterns-terragrunt)
- [Infrastructure as Code Best Practices 2025](https://articles.mergify.com/infrastructure-as-code-best-practices/)

---

*IaC Patterns Reference | faion-infrastructure-engineer*
