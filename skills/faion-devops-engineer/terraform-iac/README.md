# Terraform Infrastructure as Code

## Overview

Terraform is HashiCorp's Infrastructure as Code (IaC) tool for declarative cloud resource provisioning. Uses HCL (HashiCorp Configuration Language), tracks state, and applies changes via plan-apply workflow.

**Terraform Version:** 1.10+ recommended (S3 native locking, enhanced testing)

## When to Use

| Scenario | Recommendation |
|----------|----------------|
| Multi-cloud infrastructure | Terraform (provider ecosystem) |
| AWS-only, CloudFormation familiar | CloudFormation or Terraform |
| Programming language preference | Pulumi (TypeScript, Python, Go) |
| GitOps with Kubernetes | Crossplane or Terraform |
| Quick prototyping | Terraform with local state |

## Core Concepts

| Concept | Description |
|---------|-------------|
| Provider | Plugin for API interaction (AWS, GCP, Azure) |
| Resource | Infrastructure object managed by Terraform |
| Data Source | Read-only reference to existing infrastructure |
| Module | Reusable collection of resources |
| State | Mapping between config and real-world resources |
| Backend | Storage location for state file |
| Workspace | Named state environments |

## Workflow

```
Write HCL → terraform init → terraform plan → terraform apply → Manage/Update
```

| Phase | Command | Purpose |
|-------|---------|---------|
| Initialize | `terraform init` | Download providers, configure backend |
| Validate | `terraform validate` | Check syntax and configuration |
| Format | `terraform fmt` | Standardize code formatting |
| Plan | `terraform plan -out=tfplan` | Preview changes |
| Apply | `terraform apply tfplan` | Execute changes |
| Destroy | `terraform destroy` | Remove infrastructure |

## Project Structure

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
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── eks/
│   ├── rds/
│   └── s3/
├── tests/
│   └── vpc.tftest.hcl
└── shared/
    └── providers.tf
```

## Module Patterns

### Module Types

| Type | Purpose | Provider Config |
|------|---------|-----------------|
| Root Module | Direct `terraform apply` | Contains provider config |
| Child Module | Reusable building blocks | No provider config |
| Nested Module | Internal submodules | Inherits from parent |

### Module Sizing Guidelines

| Size | Example | Recommendation |
|------|---------|----------------|
| Too granular | Single security group rule | Avoid |
| Right size | VPC with subnets, NAT, routing | Preferred |
| Too large | Entire application stack | Split into components |

**Key Principle:** Keep module tree flat, prefer composition over deep nesting.

## State Management

### Backend Options

| Backend | Locking | Encryption | Best For |
|---------|---------|------------|----------|
| S3 + S3 Native Lock | `use_lockfile = true` | SSE-S3/SSE-KMS | AWS teams |
| S3 + DynamoDB | DynamoDB table | SSE-S3/SSE-KMS | Legacy (deprecated) |
| GCS | Built-in | Default + CMEK | GCP teams |
| Azure Blob | Built-in | Default | Azure teams |
| Terraform Cloud | Built-in | Built-in | Enterprise, SaaS |

### State Security Checklist

- [ ] Remote backend configured (never local for teams)
- [ ] Encryption at rest enabled
- [ ] State locking enabled
- [ ] Versioning enabled on storage
- [ ] Access restricted via IAM
- [ ] Separate state per environment

## Testing Framework

### Test Types (Terraform 1.6+)

| Type | Tool | Purpose |
|------|------|---------|
| Static | `terraform validate`, tflint | Syntax, best practices |
| Unit | `terraform test` (HCL) | Module logic validation |
| Integration | `terraform test` with real resources | End-to-end validation |
| Contract | Terratest (Go) | Complex assertions |
| Policy | Sentinel, OPA | Governance compliance |

### Test File Structure

```
tests/
├── vpc.tftest.hcl      # VPC module tests
├── eks.tftest.hcl      # EKS module tests
└── setup/              # Helper modules for tests
    └── main.tf
```

## Best Practices Summary

### Code Quality

1. **Format consistently** - `terraform fmt -recursive`
2. **Validate always** - `terraform validate` in CI
3. **Lock provider versions** - Pin in `required_providers`
4. **Use variable validation** - `validation` blocks
5. **Document modules** - README.md with examples

### Security

1. **Remote state only** - Never commit state files
2. **Encrypt state** - Enable encryption at rest
3. **Minimal IAM** - Least-privilege for Terraform
4. **No hardcoded secrets** - Use Secrets Manager/Vault
5. **Lock .terraform.lock.hcl** - Commit to version control

### Operations

1. **Plan before apply** - Always review plan output
2. **Use saved plans** - `terraform plan -out=tfplan`
3. **Separate environments** - Directory per environment
4. **Enable deletion protection** - Critical resources
5. **Drift detection** - Scheduled plan in CI/CD

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklists |
| [examples.md](examples.md) | Code examples |
| [templates.md](templates.md) | Starter templates |
| [llm-prompts.md](llm-prompts.md) | AI assistant prompts |

## References

- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Terraform Module Registry](https://registry.terraform.io/)
- [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

## Sources

- [Terraform IaC Best Practices 2025](https://www.elysiate.com/blog/terraform-best-practices-infrastructure-as-code-2025)
- [Terraform Modules Best Practices](https://americanchase.com/terraform-modules-best-practices/)
- [State Management Best Practices](https://www.firefly.ai/academy/state-management-in-iac-best-practices-for-handling-terraform-state-files)
- [Terraform Testing Framework](https://developer.hashicorp.com/terraform/language/tests)
- [Module Composition](https://developer.hashicorp.com/terraform/language/modules/develop/composition)
- [S3 Backend Configuration](https://developer.hashicorp.com/terraform/language/backend/s3)
