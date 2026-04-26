# Terraform State

## Summary

Remote state configuration, locking, encryption, import, and migration patterns for Terraform. The concrete rule is: always use a remote backend with locking enabled (S3+DynamoDB for AWS, GCS for GCP); separate state files per environment and per component to minimize blast radius; prefer `import` blocks (Terraform 1.5+) and `moved` blocks over CLI state commands for declarative refactoring.

## Why

Local state blocks team collaboration and has no locking — concurrent `apply` runs corrupt state. State contains sensitive data (passwords, keys) so encryption at rest is mandatory. Import blocks introduced in TF 1.5 replace fragile CLI import commands with reviewable, version-controlled declarations.

## When To Use

- Setting up a remote backend for a new project or migrating from local state
- Importing existing cloud resources into Terraform management
- Refactoring resource names or moving resources between modules
- Recovering from state corruption or lock issues
- Designing multi-environment state isolation strategy

## When NOT To Use

- Basic HCL syntax or provider configuration — use `terraform-basics`
- CI/CD pipeline design — use `terraform` (advanced methodology)
- Module structure design — use `terraform-modules`
- Emergency force-unlock without understanding lock cause — diagnose first, unlock last resort

## Content

| File | What's inside |
|------|---------------|
| `content/01-backends.xml` | Backend options comparison, S3/GCS/Azure/TFC config rules, state security |
| `content/02-operations.xml` | State commands (list, show, mv, rm, pull, push), import/moved blocks, force-replace, unlock |
| `content/03-checklist.xml` | Backend setup, security, import process, migration, disaster recovery, CI/CD checklists |

## Templates

| File | Purpose |
|------|---------|
| `templates/backend-aws.tf` | S3 + DynamoDB backend with KMS and cross-account role |
| `templates/backend-gcs.tf` | GCS backend with service account impersonation |
| `templates/backend-azure.tf` | Azure Blob backend with AAD auth |
| `templates/backend-tfc.tf` | Terraform Cloud backend |
| `templates/state-infra-aws.tf` | Full AWS state infrastructure (S3 + DynamoDB + KMS + IAM policy) |
| `templates/state-infra-gcs.tf` | GCS state bucket + Terraform service account |
| `templates/import-blocks.tf` | Import block templates (single and multi-resource) |
| `templates/moved-blocks.tf` | Moved block templates (rename, move to module, rename module) |
| `templates/remote-state-datasource.tf` | terraform_remote_state data source with usage example |
