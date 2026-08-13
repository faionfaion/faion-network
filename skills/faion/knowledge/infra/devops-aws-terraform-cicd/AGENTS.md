# Terraform Project Structure and GitHub Actions CI/CD for AWS

## Summary

**One-sentence:** Produces a Terraform project layout (per-env dirs + shared modules + S3+DDB backend) + GitHub Actions OIDC CI/CD (plan on PR, sequential apply per env with prod approval).

**One-paragraph:** Terraform projects for AWS need: per-environment directories (dev/staging/prod) to prevent blast-radius incidents from cross-env state sharing; S3 remote state with DynamoDB locking to prevent concurrent corruption; GitHub Actions OIDC authentication (no long-lived AWS keys in secrets); sequential apply with explicit prod approval gate; provider default_tags enforcing cost-allocation tagging on every resource. Output: project skeleton + CI workflow + OIDC role + provider config — ready to plug into a new repo.

**Ефективно для:**

- Новий AWS-проект з Terraform — production-ready structure.
- Додавання CI/CD до існуючого Terraform-репо без long-lived keys.
- Multi-env infra (dev/stage/prod) з isolated state.
- Enforced cost-allocation tagging + provider version pinning.

## Applies If (ALL must hold)

- IaC engine is Terraform (not Pulumi / CDK).
- Multi-environment delivery needed (≥2 envs).
- GitHub Actions is the CI provider (or GitLab / CircleCI with adapter).

## Skip If (ANY kills it)

- Single-env throwaway project — local state + manual apply OK.
- Project uses Terragrunt — directory layout differs.
- Project uses AWS CDK or Pulumi — different deployment model entirely.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Environment list | dev / staging / prod (or similar) | ops |
| AWS account map | one account per env OR sub-accounts | AWS Organizations |
| Tagging policy | Project / Environment / ManagedBy + extras | FinOps |
| OIDC trust policy | IAM role per env trusting GitHub repo | security team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[devops-aws-service-selection]] | Service choices feed the modules |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: per-env-dirs, s3-ddb-backend, oidc-no-secrets, default-tags, sequential-apply-with-prod-approval, skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for project config + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: shared-state-across-envs, long-lived-keys, no-default-tags, parallel-prod-apply | 800 |
| `content/04-procedure.xml` | essential | 6 steps: layout → backend → provider → modules → workflow → branch protect | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on env count + auth model → layout | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-layout` | sonnet | Generate per-env dirs + shared modules. |
| `compose-workflow` | sonnet | Assemble GitHub Actions with OIDC + matrix. |
| `validate-tags` | haiku | Mechanical check that default_tags include required keys. |

## Templates

| File | Purpose |
|------|---------|
| `templates/providers.tf` | Provider config: AWS + default_tags + version pin |
| `templates/backend.tf` | S3 + DynamoDB remote state backend |
| `templates/tf-ci.yml` | GitHub Actions: plan on PR, sequential apply per env after merge with prod approval |
| `templates/_smoke-test.json` | Minimum config used by validate-devops-aws-terraform-cicd.py --self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-aws-terraform-cicd.py` | Validate the config artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[devops-aws-service-selection]]
- [[security-policy-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when standing up Terraform for a new repo or hardening an existing one.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/providers.tf`

```hcl
terraform {
  required_version = "~> 1.7"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.50" }
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Project     = var.project
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
```

### `templates/backend.tf`

```hcl
terraform {
  backend "s3" {
    bucket         = "acme-tfstate-prod"
    key            = "checkout-api/prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "acme-tfstate-lock"
    encrypt        = true
  }
}
```

### `templates/tf-ci.yml`

```yaml
name: terraform
on:
  pull_request:
    paths: ["infrastructure/**"]
  push:
    branches: [main]
    paths: ["infrastructure/**"]

permissions:
  id-token: write   # OIDC
  contents: read
  pull-requests: write

jobs:
  plan:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        environment: [dev, staging, prod]
    environment:
      name: ${{ matrix.environment }}
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_OIDC_ROLE_ARN }}
          aws-region: us-east-1
      - uses: hashicorp/setup-terraform@v3
        with: { terraform_version: 1.7.5 }
      - run: terraform init
        working-directory: infrastructure/environments/${{ matrix.environment }}
      - run: terraform plan -no-color
        working-directory: infrastructure/environments/${{ matrix.environment }}

  apply:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    strategy:
      max-parallel: 1   # sequential
      matrix:
        environment: [dev, staging, prod]
    environment:
      name: ${{ matrix.environment }}   # prod env requires GitHub approval
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_OIDC_ROLE_ARN }}
          aws-region: us-east-1
      - uses: hashicorp/setup-terraform@v3
        with: { terraform_version: 1.7.5 }
      - run: terraform init && terraform apply -auto-approve
        working-directory: infrastructure/environments/${{ matrix.environment }}
```

### `templates/_smoke-test.json`

```json
{
  "layout": "per-env-dirs",
  "envs": [
    "dev",
    "staging",
    "prod"
  ],
  "backend": {
    "type": "s3",
    "lock_table": "acme-tfstate-lock",
    "encrypt": true
  },
  "auth": "oidc",
  "default_tags": [
    "Project",
    "Environment",
    "ManagedBy"
  ],
  "sequential_apply": true,
  "prod_approval": true
}
```
