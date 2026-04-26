# Terraform IaC

## Summary

Terraform manages cloud infrastructure declaratively using HCL, tracking state in a remote backend and applying changes via the plan-apply workflow. The module tree must stay flat (prefer composition over deep nesting), modules must be sized to one logical component (e.g., VPC with subnets/NAT/routing — not single security group rules, not entire application stacks). State must always use a remote backend with encryption, locking, and per-environment isolation.

## Why

Terraform's plan step produces a diff against current state before any mutation, making infrastructure changes reviewable and reversible. Remote state with locking prevents concurrent apply conflicts. Provider version pinning and `.terraform.lock.hcl` committed to git ensure reproducible runs across machines and CI. The testing framework (Terraform 1.6+) enables unit and integration tests against modules without full infra spins.

## When To Use

- Multi-cloud or cloud-agnostic infrastructure provisioning.
- Team environments where concurrent applies must be serialized (state locking).
- Infrastructure that needs policy-as-code gates (Sentinel, OPA).
- GitOps-style infra where plan output becomes a PR comment.

## When NOT To Use

- AWS-only shops already deep in CloudFormation — migration cost may not justify switch.
- Teams preferring general-purpose languages — use Pulumi (TypeScript/Python/Go).
- Pure Kubernetes resource management — Crossplane or Helm is more native.
- Single-developer local prototyping with throwaway infra — local state is acceptable.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-concepts.xml` | Providers, resources, modules, state, backends, workspace; workflow commands; module sizing rules |
| `content/02-checklists.xml` | New project setup, module development, pre-apply, state management, security, production deployment checklists |

## Templates

| File | Purpose |
|------|---------|
| `templates/backend-s3.tf` | S3 backend with native locking (Terraform 1.10+), provider config, default tags |
| `templates/variables.tf` | Variable definitions with validation blocks (environment, region, CIDR, EKS node groups) |
| `templates/modules-vpc.tf` | VPC module: main.tf + variables.tf + outputs.tf |
| `templates/github-actions.yml` | Full Terraform CI/CD pipeline: fmt-check, validate, test, plan-as-PR-comment, apply-on-merge |
