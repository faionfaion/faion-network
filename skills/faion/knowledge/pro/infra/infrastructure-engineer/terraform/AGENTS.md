# Terraform (Advanced)

## Summary

Production-grade Terraform: state architecture, module design, workspace strategies, CI/CD integration, security scanning, and compliance. The concrete rule is: always save plan to file (`-out=tfplan`) and apply the exact saved plan in CI; always run `tfsec`/`checkov` before apply; separate state by environment AND by component for minimal blast radius; use directory-per-environment over workspaces for true isolation.

## Why

Applying a re-generated plan (not the saved plan) in CI allows race conditions where infrastructure changes between plan and apply. Without policy-as-code scanning, insecure defaults (public S3, unencrypted RDS) reach production. Workspace-based isolation shares backend config and is insufficient for production blast-radius separation.

## When To Use

- Designing multi-environment Terraform project layout (environments/dev|staging|prod + modules/)
- Setting up CI/CD pipelines (GitHub Actions, GitLab CI, Atlantis) with plan-then-apply gates
- Implementing security scanning (tfsec, Checkov) in the pipeline
- Using workspaces vs directory isolation — deciding and implementing
- Running native `terraform test` or Terratest for infrastructure testing
- Drift detection and compliance (tagging policy, audit logging)

## When NOT To Use

- HCL syntax basics or first Terraform project — use `terraform-basics`
- State backend configuration and import operations — use `terraform-state`
- Module development and versioning patterns — use `terraform-modules`
- GCP-specific or AWS-specific resource patterns — use the respective cloud methodology

## Content

| File | What's inside |
|------|---------------|
| `content/01-project-structure.xml` | Directory layout, file naming convention, workspace strategies and their limitations |
| `content/02-cicd-patterns.xml` | Pipeline stages, saved plan rule, security scanning, OIDC authentication, Atlantis config |
| `content/03-checklist.xml` | State, module, workspace, CI/CD, security hardening, production deployment, compliance checklists |

## Templates

| File | Purpose |
|------|---------|
| `templates/github-actions.yml` | Full GitHub Actions pipeline: lint, security scan, plan, apply with OIDC |
| `templates/gitlab-ci.yml` | GitLab CI pipeline with validate, security scan, plan, manual apply |
| `templates/atlantis.yaml` | Atlantis config with per-project autoplan and apply requirements |
| `templates/vpc-module-main.tf` | VPC module: subnets, IGW, NAT gateways, EIPs with for_each |
| `templates/vpc-module-variables.tf` | VPC module variables with CIDR validation |
| `templates/vpc-module-outputs.tf` | VPC module outputs |
