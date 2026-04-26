# Terraform Basics

## Summary

Core Terraform reference: HCL syntax, provider configuration, resources, data sources, variables, outputs, locals, and the standard project file layout. The concrete rule is: always use `for_each` over `count` when resources need unique identifiers; always store state remotely with locking enabled; never commit `*.tfstate*` or actual `terraform.tfvars` files.

## Why

Terraform is the dominant IaC tool for multi-cloud infrastructure. Correct use of lifecycle rules, meta-arguments, and file structure prevents state corruption, accidental resource destruction, and security leaks. Data sources eliminate hardcoded AMI IDs and account details, keeping configurations portable.

## When To Use

- Starting a new Terraform project and scaffolding the file structure
- Configuring providers (AWS, GCP, Azure) with version constraints and default tags
- Writing resources with proper meta-arguments (`count`, `for_each`, `lifecycle`, `depends_on`)
- Looking up built-in function syntax (string, collection, encoding, date functions)
- Setting up remote state backends (S3+DynamoDB, GCS, Azure Blob, Terraform Cloud)

## When NOT To Use

- Advanced state operations (import, mv, rm, moved blocks) — use `terraform-state`
- Production CI/CD pipeline patterns — use `terraform` (advanced methodology)
- Module design and versioning — use `terraform-modules`
- AWS/GCP-specific resource patterns — use the respective cloud methodology

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-concepts.xml` | HCL building blocks table, workflow, lifecycle rules, meta-arguments |
| `content/02-syntax-examples.xml` | Provider config, expressions, for_each, count, dynamic blocks, built-in functions |
| `content/03-checklist.xml` | Project setup, variables, security, code quality, and CI/CD integration rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/versions.tf` | Terraform version constraint + provider requirement block |
| `templates/providers.tf` | AWS/GCP/Azure provider config with default tags |
| `templates/variables.tf` | Variable template with type constraints, validation, sensitive flag |
| `templates/outputs.tf` | Output template with descriptions and sensitive marking |
| `templates/locals.tf` | Name prefix, common tags, AZ slice, CIDR calculations |
| `templates/gitignore` | Terraform-specific .gitignore (state, tfvars, .terraform/) |
| `templates/tfvars-example.tf` | terraform.tfvars.example with safe placeholder values |
