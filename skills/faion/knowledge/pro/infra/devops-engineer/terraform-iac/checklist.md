# Terraform Checklists

## New Project Setup Checklist

### 1. Repository Structure

- [ ] Create `infrastructure/` directory
- [ ] Create `environments/{dev,staging,prod}/` directories
- [ ] Create `modules/` directory for reusable modules
- [ ] Create `tests/` directory for `.tftest.hcl` files
- [ ] Add `.gitignore` for Terraform files
- [ ] Add `README.md` with setup instructions

### 2. Backend Configuration

- [ ] Create remote state bucket (S3/GCS/Azure Blob)
- [ ] Enable versioning on state bucket
- [ ] Enable encryption on state bucket
- [ ] Configure state locking (S3: `use_lockfile = true`)
- [ ] Restrict bucket access via IAM
- [ ] Create `backend.tf` in each environment

### 3. Provider Configuration

- [ ] Define `required_providers` with version constraints
- [ ] Set `required_version` for Terraform
- [ ] Configure provider authentication (env vars, not hardcoded)
- [ ] Set up `default_tags` for resource tagging
- [ ] Create `providers.tf` or include in `main.tf`

### 4. CI/CD Pipeline

- [ ] Add `terraform fmt -check` step
- [ ] Add `terraform validate` step
- [ ] Add `terraform plan` with saved plan file
- [ ] Configure plan output as PR comment
- [ ] Add `terraform apply` with approval gate (prod)
- [ ] Add `terraform test` step for modules
- [ ] Configure secrets via CI/CD secrets manager

### 5. Security Baseline

- [ ] No credentials in code (use env vars or IAM roles)
- [ ] State file encryption enabled
- [ ] Commit `.terraform.lock.hcl` to version control
- [ ] Add `sensitive = true` to sensitive outputs
- [ ] Configure least-privilege IAM for Terraform
- [ ] Enable deletion protection on critical resources

---

## Module Development Checklist

### 1. Module Structure

- [ ] `main.tf` - Primary resource definitions
- [ ] `variables.tf` - Input variables with descriptions
- [ ] `outputs.tf` - Output values with descriptions
- [ ] `versions.tf` - Provider version constraints
- [ ] `README.md` - Usage documentation
- [ ] `examples/` - Example configurations

### 2. Variable Design

- [ ] All variables have `description`
- [ ] Appropriate `type` constraints defined
- [ ] Sensible `default` values where applicable
- [ ] `validation` blocks for input validation
- [ ] Sensitive variables marked `sensitive = true`
- [ ] No hardcoded environment-specific values

### 3. Output Design

- [ ] Every managed resource has at least one output
- [ ] Outputs have meaningful `description`
- [ ] Sensitive outputs marked `sensitive = true`
- [ ] Outputs enable dependency inference

### 4. Testing

- [ ] Unit tests in `tests/*.tftest.hcl`
- [ ] Tests cover happy path
- [ ] Tests cover error conditions
- [ ] Tests use mocking where appropriate
- [ ] CI runs tests on PR

### 5. Documentation

- [ ] README includes module purpose
- [ ] README includes usage example
- [ ] README includes input/output tables
- [ ] README includes requirements
- [ ] CHANGELOG maintained for versions

---

## Pre-Apply Checklist

### 1. Plan Review

- [ ] Review `terraform plan` output completely
- [ ] Verify no unexpected destroys
- [ ] Verify no unexpected recreates (`-/+`)
- [ ] Check resource counts match expectations
- [ ] Review changes to sensitive resources
- [ ] Verify correct environment targeted

### 2. State Verification

- [ ] State backend accessible
- [ ] State lock can be acquired
- [ ] No concurrent operations in progress
- [ ] State version matches expected

### 3. Dependencies

- [ ] External dependencies available (APIs, services)
- [ ] Dependent resources exist
- [ ] Network connectivity verified
- [ ] Credentials valid and not expired

### 4. Rollback Plan

- [ ] Previous state version available
- [ ] Rollback procedure documented
- [ ] Team notified of changes
- [ ] Maintenance window if required

---

## State Management Checklist

### State Migration

- [ ] Backup current state: `terraform state pull > backup.tfstate`
- [ ] Plan migration approach
- [ ] Test migration in non-prod first
- [ ] Run `terraform init -migrate-state`
- [ ] Verify state after migration: `terraform state list`
- [ ] Verify plan shows no changes

### State Manipulation

- [ ] Document reason for state manipulation
- [ ] Backup state before changes
- [ ] Use `terraform state mv` for refactoring
- [ ] Use `terraform state rm` for removal
- [ ] Use `terraform import` for existing resources
- [ ] Run `terraform plan` to verify no drift

### State Recovery

- [ ] Identify last known good state version
- [ ] Download state from versioned backend
- [ ] Restore state: `terraform state push`
- [ ] Verify with `terraform plan`
- [ ] Document incident and resolution

---

## Production Deployment Checklist

### Pre-Deployment

- [ ] Code reviewed and approved
- [ ] All tests passing
- [ ] Plan reviewed by second person
- [ ] Change documented in change log
- [ ] Stakeholders notified
- [ ] Rollback plan prepared

### Deployment

- [ ] Maintenance window confirmed (if required)
- [ ] Monitoring dashboards open
- [ ] Apply using saved plan file
- [ ] Monitor apply output for errors
- [ ] Verify resources created correctly

### Post-Deployment

- [ ] Run smoke tests
- [ ] Verify application health
- [ ] Check monitoring for anomalies
- [ ] Update documentation if needed
- [ ] Close change request
- [ ] Notify stakeholders of completion

---

## Security Audit Checklist

### Configuration Security

- [ ] No secrets in `.tf` files
- [ ] No secrets in `.tfvars` files (committed)
- [ ] State encryption enabled
- [ ] State access restricted
- [ ] Provider credentials via env vars or IAM

### Resource Security

- [ ] Security groups follow least privilege
- [ ] Encryption enabled on storage resources
- [ ] Encryption enabled on databases
- [ ] Public access disabled where not needed
- [ ] Deletion protection on critical resources

### Access Control

- [ ] IAM roles use least privilege
- [ ] Cross-account access documented
- [ ] Service accounts properly scoped
- [ ] MFA required for console access
- [ ] Audit logging enabled

### Compliance

- [ ] Resources tagged per policy
- [ ] Data residency requirements met
- [ ] Backup requirements met
- [ ] Retention policies configured
- [ ] Policy-as-code rules passing (Sentinel/OPA)

---

## Troubleshooting Checklist

### Common Issues

| Issue | Check |
|-------|-------|
| State lock error | Is another process running? Check lock in backend |
| Provider auth failure | Are credentials expired? Check env vars |
| Resource already exists | Import existing resource or rename |
| Dependency cycle | Review `depends_on`, refactor resources |
| Version mismatch | Check `.terraform.lock.hcl`, run `init -upgrade` |

### Debug Steps

1. [ ] Enable debug logging: `TF_LOG=DEBUG terraform plan`
2. [ ] Check provider documentation for error
3. [ ] Verify resource in cloud console
4. [ ] Check IAM permissions
5. [ ] Review recent state changes
6. [ ] Check for concurrent operations
