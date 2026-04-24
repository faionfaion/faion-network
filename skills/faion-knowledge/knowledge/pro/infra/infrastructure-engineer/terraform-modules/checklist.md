# Terraform Modules Checklist

Pre-flight and review checklists for module development.

---

## Module Creation Checklist

### Structure

- [ ] `main.tf` contains primary resources
- [ ] `variables.tf` defines all inputs with descriptions
- [ ] `outputs.tf` exports necessary values
- [ ] `versions.tf` specifies Terraform and provider constraints
- [ ] `README.md` documents module usage
- [ ] Optional: `locals.tf` for computed values
- [ ] Optional: `data.tf` for data sources

### Variables

- [ ] All variables have descriptions
- [ ] Sensible defaults provided where appropriate
- [ ] Type constraints defined (`string`, `number`, `list`, `map`, `object`)
- [ ] Validation blocks for input constraints
- [ ] Sensitive variables marked with `sensitive = true`
- [ ] Complex types use `object()` with explicit structure

### Outputs

- [ ] Resource IDs exported
- [ ] ARNs exported for AWS resources
- [ ] Connection strings exported (if applicable)
- [ ] All outputs have descriptions
- [ ] Sensitive outputs marked appropriately

### Naming

- [ ] Registry module follows `terraform-<PROVIDER>-<NAME>` convention
- [ ] Resources use consistent naming with `var.name` prefix
- [ ] Tags include standard keys (Name, Environment, ManagedBy)

---

## Code Quality Checklist

### Formatting & Validation

- [ ] `terraform fmt -check` passes
- [ ] `terraform validate` passes
- [ ] No hardcoded values (use variables)
- [ ] No hardcoded secrets
- [ ] Consistent indentation (2 spaces)

### Best Practices

- [ ] Single responsibility (one purpose per module)
- [ ] No provider blocks in child modules
- [ ] Uses `for_each` over `count` where possible
- [ ] Avoids mega-modules (< 500 lines recommended)
- [ ] No tight coupling between modules

### Documentation

- [ ] README includes usage example
- [ ] README lists all inputs/outputs
- [ ] CHANGELOG.md maintained (for published modules)
- [ ] Complex logic commented
- [ ] Generated docs via `terraform-docs`

---

## Security Checklist

### Secrets Management

- [ ] No secrets in `.tf` files
- [ ] No secrets in `.tfvars` committed to Git
- [ ] Secrets referenced from secret managers
- [ ] `.gitignore` excludes `*.tfstate`, `*.tfvars` (if sensitive)

### IAM & Permissions

- [ ] Least privilege principle applied
- [ ] No wildcard (`*`) actions without justification
- [ ] Resource-level permissions where possible
- [ ] IAM policies attached to roles, not users

### Network Security

- [ ] Security groups follow least privilege
- [ ] No `0.0.0.0/0` ingress without justification
- [ ] Private subnets used for databases
- [ ] VPC flow logs enabled (if required)

### Compliance

- [ ] Encryption at rest enabled
- [ ] Encryption in transit enabled
- [ ] Logging enabled for audit trails
- [ ] Tags meet organizational requirements

---

## Testing Checklist

### Pre-Commit

- [ ] `terraform fmt` runs on save
- [ ] `terraform validate` in pre-commit hook
- [ ] `tflint` lint check passes

### Plan Review

- [ ] `terraform plan` shows expected changes
- [ ] No unexpected resource deletions
- [ ] No unexpected resource recreations
- [ ] Cost estimate reviewed (if using Terraform Cloud)

### Automated Testing

- [ ] Unit tests with `terraform test`
- [ ] Integration tests with Terratest (if applicable)
- [ ] Security scan with Checkov/tfsec
- [ ] Policy check with Sentinel/OPA (if applicable)

---

## Release Checklist

### Version Bump

- [ ] Version follows SemVer
- [ ] CHANGELOG.md updated
- [ ] Breaking changes documented
- [ ] Migration guide provided (for major versions)

### Registry Publication

- [ ] Module structure validated
- [ ] README complete with examples
- [ ] Git tag created (`vX.Y.Z`)
- [ ] Registry sync verified

### Notification

- [ ] Team notified of new release
- [ ] Consumer modules updated (if internal)
- [ ] Deprecation notices for removed features

---

## Code Review Checklist

### For Reviewers

- [ ] Module follows single responsibility
- [ ] Variables have descriptions and appropriate defaults
- [ ] Outputs are documented and useful
- [ ] No hardcoded secrets or values
- [ ] Tests pass
- [ ] Security scan clean
- [ ] Documentation updated

### Red Flags

- [ ] Mega-modules (> 500 lines)
- [ ] Provider blocks in child modules
- [ ] Hardcoded AWS account IDs
- [ ] Wildcard IAM permissions
- [ ] Missing encryption settings
- [ ] `0.0.0.0/0` ingress rules

---

## CI/CD Pipeline Checklist

### Pipeline Stages

- [ ] Format check (`terraform fmt -check`)
- [ ] Validation (`terraform validate`)
- [ ] Lint (`tflint`)
- [ ] Security scan (`checkov`, `tfsec`)
- [ ] Plan (`terraform plan`)
- [ ] Apply (with approval for prod)

### Environment Promotion

- [ ] Dev environment tested
- [ ] Staging environment verified
- [ ] Production requires manual approval
- [ ] Rollback procedure documented

---

*Terraform Modules Checklist*
*Part of faion-infrastructure-engineer skill*
