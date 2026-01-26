# Terraform Infrastructure

**Production-Grade Infrastructure as Code (2025-2026)**

---

## Overview

Terraform enables declarative infrastructure management across multi-cloud environments. This skill covers production-grade Terraform: HCL syntax, state management, modules, workspaces, security, and CI/CD integration.

---

## Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Production readiness and security checklists |
| [examples.md](examples.md) | State backends, modules, workspaces, CI/CD patterns |
| [templates.md](templates.md) | Production-ready configurations and module structures |
| [llm-prompts.md](llm-prompts.md) | AI prompts for Terraform infrastructure tasks |

---

## Core Concepts

| Concept | Description |
|---------|-------------|
| **State** | Source of truth mapping config to real infrastructure |
| **Provider** | Plugin for cloud/service API (AWS, GCP, Azure, K8s) |
| **Resource** | Infrastructure component to create/manage |
| **Module** | Reusable, encapsulated configuration package |
| **Workspace** | Isolated state environment (dev, staging, prod) |
| **Backend** | Remote state storage (S3, GCS, Terraform Cloud) |

---

## State Management (2025-2026)

### Remote State Architecture

```
                    Terraform Configuration
                            |
                    [terraform apply]
                            |
            +---------------+---------------+
            |                               |
    [Remote Backend]               [State Locking]
    (S3, GCS, Azure,               (DynamoDB, GCS,
     Terraform Cloud)               Terraform Cloud)
            |                               |
            +---------------+---------------+
                            |
                    [terraform.tfstate]
                            |
                    [Real Infrastructure]
```

### State Best Practices

| Practice | Description |
|----------|-------------|
| **Remote storage** | Never use local state in production |
| **State locking** | Prevent concurrent modifications (DynamoDB, GCS) |
| **Encryption** | Always encrypt state at rest and in transit |
| **Versioning** | Enable bucket versioning for state recovery |
| **Separate states** | Split by environment and component for blast radius |
| **Access control** | Restrict state access with IAM policies |
| **No secrets in code** | Mark sensitive values, use external secret managers |

---

## Module Design (2025-2026)

### Module Structure

```
modules/
├── networking/
│   ├── main.tf           # Resources
│   ├── variables.tf      # Input variables
│   ├── outputs.tf        # Output values
│   ├── versions.tf       # Provider requirements
│   ├── README.md         # Documentation
│   └── examples/         # Usage examples
├── compute/
│   └── ...
└── database/
    └── ...
```

### Module Principles

| Principle | Description |
|-----------|-------------|
| **Single responsibility** | One module = one logical component |
| **Small blast radius** | Limit resources per module |
| **Versioned** | Tag releases, use semantic versioning |
| **Documented** | README with inputs, outputs, examples |
| **Tested** | Validate with terraform test or Terratest |
| **No hardcoded values** | Parameterize everything via variables |

---

## Workspaces (2025-2026)

### Workspace Strategies

| Strategy | Use Case | Isolation |
|----------|----------|-----------|
| **CLI Workspaces** | Simple environments, same backend | Low |
| **Directory per env** | Strong isolation, different backends | High |
| **Terraform Cloud** | Enterprise, policy enforcement | High |

### Workspace Limitations

- Workspaces share the same backend configuration
- Not suitable for system decomposition
- Use separate directories for true isolation
- Prefer for environment variants (dev/staging/prod) of same infra

---

## CI/CD Integration (2025-2026)

### Pipeline Stages

```
[Commit] → [Lint] → [Validate] → [Plan] → [Review] → [Apply] → [Verify]
              |          |           |          |          |
           tflint    terraform   terraform   Human    terraform   Drift
          hadolint   validate      plan     approval    apply    detection
           checkov                                               monitoring
```

### CI/CD Best Practices

| Practice | Description |
|----------|-------------|
| **Version control** | All IaC in git, never edit state manually |
| **Pin versions** | Lock provider and module versions |
| **Lock file** | Commit .terraform.lock.hcl for reproducibility |
| **Automated formatting** | terraform fmt -check in CI |
| **Security scanning** | tfsec, Checkov, Trivy before apply |
| **Plan artifacts** | Save plans, apply exact plan in production |
| **Human review** | Require approval before production apply |
| **Drift detection** | Schedule regular plan runs to detect drift |
| **Rollback strategy** | Version state, maintain previous configs |

---

## Security (2025-2026)

### State Security

| Control | Implementation |
|---------|----------------|
| Encryption at rest | S3 SSE-KMS, GCS encryption |
| Encryption in transit | HTTPS only |
| Access control | IAM policies, least privilege |
| Audit logging | CloudTrail, Cloud Audit Logs |
| No secrets in state | Mark sensitive, use vault/secrets manager |

### Code Security

| Control | Implementation |
|---------|----------------|
| No hardcoded secrets | Use variables with sensitive = true |
| Secret management | AWS Secrets Manager, HashiCorp Vault |
| Policy as code | Sentinel, OPA/Conftest |
| SAST scanning | tfsec, Checkov, Trivy |
| Signed modules | Terraform Registry, private registry |

---

## Quick Commands

```bash
# Initialize
terraform init
terraform init -upgrade  # Upgrade providers

# Format and validate
terraform fmt -recursive
terraform validate

# Plan and apply
terraform plan -out=tfplan
terraform apply tfplan
terraform apply -auto-approve  # CI only

# State operations
terraform state list
terraform state show aws_instance.web
terraform state mv aws_instance.old aws_instance.new
terraform import aws_instance.web i-1234567890abcdef0

# Workspaces
terraform workspace list
terraform workspace new staging
terraform workspace select production

# Destroy (careful!)
terraform destroy
terraform destroy -target=aws_instance.web

# Debug
TF_LOG=DEBUG terraform plan
terraform console
terraform graph | dot -Tpng > graph.png
```

---

## Project Structure (2025-2026)

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
│   ├── networking/
│   ├── compute/
│   ├── database/
│   └── ...
├── global/
│   ├── iam/
│   └── dns/
└── README.md
```

### File Naming Convention

| File | Content |
|------|---------|
| `versions.tf` | Terraform and provider version constraints |
| `providers.tf` | Provider configuration |
| `main.tf` | Main resources |
| `variables.tf` | Input variables |
| `outputs.tf` | Output values |
| `locals.tf` | Local values |
| `data.tf` | Data sources |
| `backend.tf` | Backend configuration |

---

## Tools (2025-2026)

| Tool | Purpose |
|------|---------|
| [tfsec](https://github.com/aquasecurity/tfsec) | Static security scanner |
| [Checkov](https://github.com/bridgecrewio/checkov) | Policy-as-code scanner |
| [tflint](https://github.com/terraform-linters/tflint) | Linter with provider rules |
| [terraform-docs](https://github.com/terraform-docs/terraform-docs) | Documentation generator |
| [Terratest](https://github.com/gruntwork-io/terratest) | Infrastructure testing in Go |
| [Infracost](https://github.com/infracost/infracost) | Cost estimation in CI |
| [Terragrunt](https://github.com/gruntwork-io/terragrunt) | DRY wrapper for Terraform |
| [Atlantis](https://www.runatlantis.io/) | Pull request automation |
| [Spacelift](https://spacelift.io/) | Enterprise Terraform platform |

---

## Related Files

| File | Location |
|------|----------|
| Terraform Basics | [terraform-basics.md](../terraform-basics.md) |
| Terraform Modules | [terraform-modules.md](../terraform-modules.md) |
| Terraform State | [terraform-state.md](../terraform-state.md) |
| AWS Infrastructure | [aws/](../aws/) |
| GCP Infrastructure | [gcp/](../gcp/) |

---

## Sources

- [Terraform Documentation](https://developer.hashicorp.com/terraform)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Terraform State Management Best Practices](https://spacelift.io/blog/terraform-state)
- [Terraform Modules Best Practices 2025](https://americanchase.com/terraform-modules-best-practices/)
- [Terraform CI/CD Best Practices](https://terrateam.io/blog/terraform-best-practices-ci-cd)
- [Terraform Workspaces Best Practices](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/best-practices)
- [Terraform State at Scale](https://www.stackguardian.io/post/terraform-state-management-at-scale-strategies-for-enterprise-environments)
- [Terraform Backend Configuration Guide 2025](https://scalr.com/learning-center/terraform-backend-configuration-guide-choosing-the-right-state-management-solution/)

---

*Terraform Infrastructure | faion-infrastructure-engineer*
