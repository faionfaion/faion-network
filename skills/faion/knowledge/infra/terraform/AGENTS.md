# Terraform

## Summary

**One-sentence:** Terraform spec: HCL modules, remote state (S3 + DynamoDB or Terraform Cloud), explicit provider version pinning, plan-review-apply gate, drift detection, secret-free state hygiene.

**One-paragraph:** Terraform codifies infrastructure changes in version-controlled HCL, enabling reproducible environments, drift detection, and auditable change history. The wins come from discipline: pinned provider versions, remote state with locking, plan-review-apply in CI (no terraform apply from a laptop), modules over copy-paste, and secret-free state. The losses come from skipping any of those: drifted state, secrets in plaintext state files, modules forked into N copies. This methodology pins the rules + the bootstrap pattern + the audit hooks.

**Ефективно для:**

- Reproducible infra: HCL → identical envs (dev / staging / prod).
- Drift detection через terraform plan в CI на щотижневому cron.
- Plan review в PR замість apply-from-laptop.
- Module reuse через terraform-aws-modules + private registry.

## Applies If (ALL must hold)

- Multi-cloud or single-cloud infra that needs to be reproducible across envs
- Team of >=2 engineers touching infra (state locking needed)
- Compliance requires change history + plan review
- Drift detection needed (manual console changes happen)

## Skip If (ANY kills it)

- Single dev laptop with one EC2 instance — overhead exceeds value
- All resources provisioned via cloud-provider-specific GUI tooling and no automation needed
- Pulumi / CDK already in place and team prefers programming-language IaC — pick one, don't run both

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cloud account + IAM role for Terraform | credentials | platform team |
| Remote state backend (S3 + DynamoDB / TF Cloud) | backend config | platform team |
| CI runner with terraform binary + creds via OIDC | GitHub Actions / GitLab | DevOps lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[secrets-management]] | Secrets injected via env / vault, not state file |
| [[security-as-code]] | Policy gates on plan output |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `module_extraction` | sonnet | HCL refactor with judgement on interface |
| `plan_review` | opus | Cross-resource impact analysis |
| `backend_config_fill` | haiku | Template fill |

## Templates

| File | Purpose |
|------|---------|
| `templates/backend.tf` | Backend template |
| `templates/locals.tf` | Locals template |
| `templates/prompt-generate-module.txt` | Prompt generate module template |
| `templates/prompt-security-review.txt` | Prompt security review template |
| `templates/variables.tf` | Variables template |
| `templates/versions.tf` | Versions template |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-terraform.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[terraform-iac]]
- [[drift-classification-taxonomy]]
- [[security-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/backend.tf`

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "project/environment/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
# Replace bucket, key, and dynamodb_table with actual values.
# Do not use variable interpolation here — backend config is resolved before variables.
# Use -backend-config flag or a partial backend config file per environment.
```

### `templates/locals.tf`

```hcl
locals {
  name_prefix = "${var.project_name}-${var.environment}"

  env_config = {
    dev = {
      instance_type = "t3.micro"
      min_size      = 1
      max_size      = 2
    }
    staging = {
      instance_type = "t3.small"
      min_size      = 1
      max_size      = 3
    }
    prod = {
      instance_type = "t3.medium"
      min_size      = 2
      max_size      = 10
    }
  }

  config = local.env_config[var.environment]
}
```

### `templates/prompt-generate-module.txt`

```text
Generate a Terraform module for: [DESCRIBE THE RESOURCE OR COMPONENT]

Requirements:
- Target cloud provider: [AWS | GCP | Azure]
- Environment support: dev / staging / prod with per-environment sizing via locals
- Input variables with validation blocks for all required inputs
- Outputs for all resource IDs and ARNs that callers will need
- Remote state backend with S3 + DynamoDB locking
- Secrets via AWS Secrets Manager data source — no secrets in variables or tfvars
- Resource tags: Environment, Project, ManagedBy=terraform

Module structure:
  versions.tf   — required_version and required_providers with pinned versions
  variables.tf  — all inputs with descriptions and validation
  locals.tf     — computed values, env-specific config map
  main.tf       — resources (reference locals.config[var.environment] for sizing)
  outputs.tf    — all outputs callers need

Security requirements:
- IAM roles, not users. No wildcard actions for mutating operations
- Encryption at rest enabled on all data stores
- No sensitive = false on output values containing ARNs or IDs that expose account info
- Add aws:RequestedRegion condition to IAM policies where applicable

CI/CD integration:
- Add a GitHub Actions workflow snippet that runs: fmt -check, validate, tfsec, plan on PR; apply on merge to main using OIDC (no stored credentials)

Output the module files as separate code blocks labeled with their filename.
```

### `templates/prompt-security-review.txt`

````text
Review the following Terraform code for security issues:

```hcl
[PASTE TERRAFORM CODE HERE]
```

Check for:

1. Secrets management
   - Hardcoded secrets or passwords in resource arguments or variable defaults
   - Secrets in tfvars files that should use data sources (aws_secretsmanager_secret_version, vault_generic_secret)

2. IAM least-privilege
   - Wildcard actions (* in Action) for mutating operations
   - Missing resource-level conditions (aws:RequestTag, aws:RequestedRegion)
   - Long-lived IAM user access keys instead of roles

3. State file security
   - Backend encryption enabled (encrypt = true)
   - DynamoDB locking configured
   - MFA delete on state S3 bucket for prod

4. Network security
   - Security groups with 0.0.0.0/0 ingress on non-HTTP ports
   - S3 buckets with public access enabled
   - RDS instances with publicly_accessible = true

5. Encryption at rest
   - storage_encrypted = true on RDS
   - encrypted = true on EBS volumes
   - SSE enabled on S3 buckets

For each finding: state the file/resource, explain the risk, and provide the corrected HCL.
````

### `templates/variables.tf`

```hcl
variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
  default     = "us-east-1"

  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-[0-9]$", var.aws_region))
    error_message = "Must be a valid AWS region code (e.g. us-east-1)."
  }
}

variable "environment" {
  description = "Deployment environment: dev, staging, or prod"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be one of: dev, staging, prod."
  }
}

variable "project_name" {
  description = "Project name used in resource tags and name prefixes"
  type        = string
}
```

### `templates/versions.tf`

```hcl
terraform {
  required_version = ">= 1.9.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
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
