# Terraform Checklist

Pre-deployment and review checklists for Terraform projects.

---

## Project Setup Checklist

### Initial Configuration

- [ ] Terraform version pinned in `versions.tf` (`required_version = ">= 1.6.0"`)
- [ ] Provider versions pinned with `~>` constraint
- [ ] `.terraform.lock.hcl` committed to version control
- [ ] `.gitignore` includes sensitive files
- [ ] Remote backend configured with encryption
- [ ] State locking enabled (DynamoDB for S3)

### File Structure

- [ ] `main.tf` - Main resources
- [ ] `variables.tf` - All input variables with descriptions
- [ ] `outputs.tf` - All outputs with descriptions
- [ ] `versions.tf` - Terraform and provider versions
- [ ] `providers.tf` - Provider configuration
- [ ] `locals.tf` - Local values
- [ ] `data.tf` - Data sources
- [ ] `terraform.tfvars.example` - Example variable values

### Documentation

- [ ] README.md with usage instructions
- [ ] All variables have descriptions
- [ ] All outputs have descriptions
- [ ] Module inputs/outputs documented
- [ ] Examples provided for complex modules

---

## Code Quality Checklist

### Naming Conventions

- [ ] Resources use snake_case: `aws_instance.web_server`
- [ ] Variables use snake_case: `var.instance_type`
- [ ] Resource names are descriptive
- [ ] Consistent naming pattern: `{project}-{env}-{resource}`

### Code Style

- [ ] Code formatted with `terraform fmt`
- [ ] Configuration validates with `terraform validate`
- [ ] No hardcoded values (use variables)
- [ ] No duplicate code (use modules)
- [ ] Comments for non-obvious logic

### Variables

- [ ] All variables have `description`
- [ ] Type constraints defined
- [ ] Validation rules where appropriate
- [ ] Sensitive variables marked with `sensitive = true`
- [ ] Defaults provided where sensible

### Resource Configuration

- [ ] Tags applied consistently
- [ ] Lifecycle rules configured where needed
- [ ] `depends_on` used only when necessary
- [ ] `count` or `for_each` used appropriately
- [ ] No provisioners (use user_data or config management)

---

## Security Checklist

### Secrets Management

- [ ] No hardcoded secrets in code
- [ ] No secrets in `terraform.tfvars` (use env vars or secret manager)
- [ ] Sensitive outputs marked `sensitive = true`
- [ ] Secret manager integration (AWS SM, Vault, etc.)
- [ ] `.tfvars` files in `.gitignore`

### State Security

- [ ] Remote state with encryption enabled
- [ ] State bucket access restricted
- [ ] State locking enabled
- [ ] Bucket versioning enabled
- [ ] Access logging enabled
- [ ] MFA delete enabled (production)

### IAM & Access

- [ ] IAM roles used instead of users
- [ ] Least privilege permissions
- [ ] No `*` in IAM actions (except read)
- [ ] Resource-level permissions where possible
- [ ] Conditions added to IAM policies

### Network Security

- [ ] Security groups follow least privilege
- [ ] No `0.0.0.0/0` ingress (except public services)
- [ ] Private subnets for databases
- [ ] VPC flow logs enabled
- [ ] Network ACLs configured

### Encryption

- [ ] S3 buckets encrypted
- [ ] EBS volumes encrypted
- [ ] RDS storage encrypted
- [ ] KMS keys rotated
- [ ] Transit encryption enabled

### Compliance

- [ ] Runs `tfsec` without critical issues
- [ ] Runs `checkov` without high severity issues
- [ ] Security scanning in CI/CD pipeline
- [ ] Drift detection scheduled

---

## Module Checklist

### Module Structure

- [ ] `main.tf`, `variables.tf`, `outputs.tf` present
- [ ] `versions.tf` with provider constraints
- [ ] `README.md` with documentation
- [ ] `examples/` directory with usage examples
- [ ] No provider configuration in module (pass from root)

### Module Design

- [ ] Single responsibility (one function per module)
- [ ] Clear input/output interface
- [ ] All inputs documented with descriptions
- [ ] All outputs documented with descriptions
- [ ] Sensible defaults for optional variables
- [ ] Validation rules for inputs

### Module Publishing

- [ ] Semantic versioning used
- [ ] CHANGELOG.md maintained
- [ ] Tags created for releases
- [ ] Module source uses version constraint

---

## Pre-Apply Checklist

### Plan Review

- [ ] Run `terraform plan` and review all changes
- [ ] No unexpected destroys or recreations
- [ ] All changes are intentional
- [ ] Sensitive values not exposed in plan
- [ ] Resource counts are correct

### Environment Verification

- [ ] Correct workspace/environment selected
- [ ] Correct AWS profile/credentials
- [ ] Correct region configured
- [ ] Backend state is current (`terraform init`)
- [ ] No pending changes from others

### Impact Assessment

- [ ] Understand blast radius of changes
- [ ] Identify potential downtime
- [ ] Database changes reviewed carefully
- [ ] Network changes reviewed carefully
- [ ] IAM changes reviewed carefully

---

## Post-Apply Checklist

### Verification

- [ ] Resources created successfully
- [ ] Outputs captured and stored securely
- [ ] Application health checks pass
- [ ] Monitoring/alerting active
- [ ] Logs flowing correctly

### Documentation

- [ ] Changes documented in commit message
- [ ] Significant changes noted in CHANGELOG
- [ ] Architecture diagrams updated if needed
- [ ] Runbook updated if needed

### Cleanup

- [ ] Temporary resources removed
- [ ] Old resources decommissioned
- [ ] Cost implications reviewed

---

## CI/CD Pipeline Checklist

### Pipeline Configuration

- [ ] `terraform fmt -check` in CI
- [ ] `terraform validate` in CI
- [ ] `terraform plan` saved as artifact
- [ ] Security scanning (tfsec, checkov) in CI
- [ ] Plan approval required for apply
- [ ] Apply runs only from main/protected branch

### Credentials

- [ ] OIDC/workload identity for cloud auth
- [ ] No long-lived credentials in CI
- [ ] Credentials rotated regularly
- [ ] Least privilege for CI service account

### State Management

- [ ] State locking prevents concurrent runs
- [ ] Plan output matches apply input
- [ ] State backup before apply
- [ ] Drift detection scheduled

---

## Disaster Recovery Checklist

### State Recovery

- [ ] State bucket versioning enabled
- [ ] State backup procedure documented
- [ ] Recovery procedure tested
- [ ] Cross-region state replication (optional)

### Documentation

- [ ] Resource inventory documented
- [ ] Manual resources documented
- [ ] Import procedures documented
- [ ] Recovery runbook available

---

## Migration Checklist

### State Migration

- [ ] Backup current state
- [ ] Test migration in non-prod first
- [ ] Update backend configuration
- [ ] Run `terraform init -migrate-state`
- [ ] Verify state integrity after migration

### Resource Migration

- [ ] Use `moved` blocks for renames
- [ ] Test `terraform plan` shows no changes
- [ ] Document migration steps
- [ ] Rollback procedure prepared
