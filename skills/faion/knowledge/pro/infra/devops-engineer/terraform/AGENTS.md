# Terraform

## Summary

Infrastructure as Code with HashiCorp Terraform: HCL syntax, provider/module/state management, workspaces, and security. Pin `required_version` and all provider versions in every project; never commit `.tfvars` files containing secrets.

## Why

Terraform codifies infrastructure changes in version-controlled HCL, enabling reproducible environments, drift detection, and auditable change history. Remote state with locking (S3 + DynamoDB) prevents concurrent-apply corruption.

## When To Use

- Provisioning or modifying cloud resources on AWS, GCP, or Azure
- Managing multi-environment infrastructure (dev/staging/prod) from one codebase
- Building reusable infrastructure modules shared across projects
- Setting up CI/CD pipelines that automate `terraform plan` and `apply`
- Migrating existing resources into Terraform management via `import`

## When NOT To Use

- Kubernetes workloads — use Helm or Kustomize; Terraform's K8s provider is awkward for app config
- Simple one-off scripts — shell or cloud CLI is faster for ephemeral resources
- Secrets management — use Vault, AWS Secrets Manager, or similar; never store secrets in state
- Config management inside VMs — that's Ansible/Chef/Puppet territory

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-concepts.xml` | HCL syntax, variables, locals, outputs, expressions, built-in functions |
| `content/02-state-and-modules.xml` | Remote backend setup, state commands, module structure and design principles |
| `content/03-security-checklist.xml` | Secrets management, IAM best practices, state file security, CI/CD checklist rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/versions.tf` | Minimal versions.tf pinning Terraform and AWS provider |
| `templates/variables.tf` | Project variables template with validation examples |
| `templates/locals.tf` | locals.tf with name_prefix and env_config pattern |
| `templates/backend.tf` | S3 backend with DynamoDB locking |
| `templates/prompt-generate-module.txt` | LLM prompt to generate a Terraform module |
| `templates/prompt-security-review.txt` | LLM prompt for Terraform security review |
